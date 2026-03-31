from fpdf import FPDF

def generar_pdf_servicios(servicios):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Reporte de Servicios", ln=True, align='C')
    pdf.ln(10)

    for s in servicios:
        pdf.cell(200, 10, txt=f"ID: {s[0]} - {s[1]} - ${s[3]}", ln=True)

    pdf.output("reporte_servicios.pdf")