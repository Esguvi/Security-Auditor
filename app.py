from flask import Flask, render_template, request, send_file, session
from config import APP_NAME
from services.local_audit import run_local_audit
from services.remote_audit import run_remote_audit

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

@app.route("/", methods=["GET", "POST"])
def dashboard():
    report = None

    if request.method == "POST":
        target = request.form.get("target", "").strip()
        if not target:
            return render_template("dashboard.html", app_name=APP_NAME)

        if target in ["localhost", "127.0.0.1"]:
            report = run_local_audit(target)
        else:
            report = run_remote_audit(target)

        # Guardamos solo lo necesario para el PDF
        session["last_report"] = report

    return render_template(
        "dashboard.html",
        app_name=APP_NAME,
        report=report
    )

@app.route("/export_pdf", methods=["GET"])
def export_pdf():
    report = session.get("last_report")

    if not report:
        return "No report available", 400

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=60,
        title="Security Audit Report",
        author="ESGUVI"
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---- Custom styles ----
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=1
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        spaceAfter=10
    )

    elements.append(Paragraph("Esguvi - Security Audit Report", title_style))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Executive Summary", section_style))
    elements.append(Paragraph(
        "This report provides a high-level security assessment of the target system. "
        "The analysis covers exposed network services, missing HTTP security headers, "
        "and TLS configuration to identify potential security risks.",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Target:</b> {report['target']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Risk Score:</b> {report['score']}/100", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Open Ports", section_style))
    table_data = [["Port", "Service", "Risk"]]

    for p in report.get("ports", []):
        risk = p["risk"]
        color = colors.green if risk == "LOW" else colors.orange if risk == "MEDIUM" else colors.red
        table_data.append([
            str(p["port"]),
            p["service"],
            Paragraph(f'<font color="{color.hexval()}"><b>{risk}</b></font>', styles["Normal"])
        ])

    ports_table = Table(table_data, colWidths=[80, 220, 100])
    ports_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(ports_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Security Headers Issues", section_style))
    headers = report.get("headers", [])
    if headers:
        for h in headers:
            elements.append(Paragraph(f"- {h}", styles["Normal"]))
    else:
        elements.append(Paragraph("No missing security headers detected.", styles["Normal"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("TLS Information", section_style))
    elements.append(Paragraph(report.get("tls", "Not available"), styles["Normal"]))
    elements.append(Spacer(1, 20))

    def draw_footer(canvas, doc):
        width, _ = letter
        footer_text = "Informe generado y diseñado por ESGUVI"
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(width / 2, 30, footer_text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="security_audit_report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
