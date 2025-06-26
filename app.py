from flask import Flask, render_template, jsonify, send_file
from sniffer import start_sniffing, get_recent_packets
from fpdf import FPDF
from io import BytesIO, StringIO
import csv
import threading

app = Flask(__name__)

# Start packet sniffer in a background thread
threading.Thread(target=start_sniffing, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/packets")
def packets():
    return jsonify(get_recent_packets())

@app.route("/export/pdf")
def export_pdf():
    packets = get_recent_packets()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Network Packet Sniffer Report", ln=True, align="C")

    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    for pkt in packets:
        line = f"{pkt['time']} | {pkt['protocol']} | {pkt['src']} -> {pkt['dst']} | {pkt['alert']}"
        pdf.cell(200, 8, txt=line, ln=True)

    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="packet_report.pdf", mimetype='application/pdf')

@app.route("/export/csv")
def export_csv():
    packets = get_recent_packets()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Time", "Protocol", "Source IP", "Destination IP", "Alert"])
    for pkt in packets:
        writer.writerow([pkt["time"], pkt["protocol"], pkt["src"], pkt["dst"], pkt["alert"]])
    output = BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', download_name="packets.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
