from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(df, out_path='report.pdf'):
    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, height - 40, 'Auto-Insight Agent Pro - Report')
    c.setFont('Helvetica', 10)
    c.drawString(40, height - 70, f'Dataset rows: {df.shape[0]}, columns: {df.shape[1]}')
    y = height - 100
    for col in df.columns[:6]:
        try:
            stats = df[col].describe().to_dict()
            c.drawString(40, y, f'{col}: {stats}')
            y -= 40
            if y < 80:
                c.showPage()
                y = height - 40
        except Exception:
            pass
    c.save()
    return out_path
