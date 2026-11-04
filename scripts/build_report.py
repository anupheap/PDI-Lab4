"""Build a screenshot-based PDF from captured source files and genuine run output."""
import argparse
import json
import pathlib
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--date", default="2026-11-04")
options = parser.parse_args()
evidence = json.loads((ROOT / "output/report/evidence/runs.json").read_text(encoding="utf-8"))
screenshots = json.loads((ROOT / "output/report/screenshots.json").read_text(encoding="utf-8"))
destination = ROOT / "output/pdf/Lab4_Report.pdf"
destination.parent.mkdir(parents=True, exist_ok=True)
width, height = landscape(A4)
pdf = canvas.Canvas(str(destination), pagesize=(width, height))
pdf.setTitle("PDI Lab 4 - File I/O in Java: solutions and verified output")
pdf.setAuthor("anupheap")
navy = colors.HexColor("#142434")
teal = colors.HexColor("#126575")
muted = colors.HexColor("#52677a")
style = ParagraphStyle("body", fontName="Helvetica", fontSize=10.5, leading=15, textColor=navy)


def paragraph(text, x, top, available_width, paragraph_style=style):
    item = Paragraph(text, paragraph_style)
    _, h = item.wrap(available_width, height)
    item.drawOn(pdf, x, top - h)
    return top - h


def frame(title, subtitle, number):
    pdf.setFillColor(teal)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(36, height - 29, "PROGRAMMING DESIGN AND IMPLEMENTATION / LAB 04")
    pdf.setFillColor(navy)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(36, height - 65, title)
    paragraph(escape(subtitle), 36, height - 79, width - 72)
    pdf.setStrokeColor(colors.HexColor("#d3dce4"))
    pdf.line(36, 32, width - 36, 32)
    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(36, 19, f"PDI Lab 4 | {options.date} | Source revision {evidence['source_revision'][:7]}")
    pdf.drawRightString(width - 36, 19, f"{number} / {len(screenshots) + 1}")


frame("File I/O in Java", "Seven exercises, the bonus, and verified program output", 1)
left, right = 36, 434
top = height - 125
pdf.setFont("Helvetica-Bold", 14)
pdf.setFillColor(teal)
pdf.drawString(left, top, "Completed solutions")
y = top - 15
for label in ["1. Generate and reread 500 random numbers.",
              "2. Create n CSV files and find minimum / maximum.",
              "3. Save three team members as CSV.",
              "4. Read students into an ArrayList and display them.",
              "5. Add three students, sort A-Z, and save.",
              "6. Analyze candidate scores and gender statistics.",
              "7. Export groups with summary footer rows.",
              "Bonus. Serialize and deserialize Student objects."]:
    y = paragraph(escape(label), left, y, 360) - 8
y -= 6
y = paragraph("<b>Execution:</b> Java 17 runtime; Eclipse ECJ 3.40.0 compiler targeting Java 17. "
              "The source requires JDK 17 or newer and no external Java libraries.", left, y, 360) - 12
y = paragraph("<b>Evidence:</b> Browser screenshots render the repository source and genuine "
              "captured standard output. Interactive inputs are listed separately. Random values "
              "differ on each run. All student names and IDs in the demonstrations are fictional.", left, y, 360)

pdf.setFillColor(teal)
pdf.setFont("Helvetica-Bold", 14)
pdf.drawString(right, top, "Supplied dataset - verified aggregates")
table_data = [["Population", "Total", "Male", "Female"]]
for row in evidence["summary"]:
    n = row["total"]
    male = 100 * row["male"] / n if n else 0
    female = 100 * row["female"] / n if n else 0
    table_data.append([row["label"], str(n), f"{row['male']} ({male:.2f}%)", f"{row['female']} ({female:.2f}%)"])
table = Table(table_data, colWidths=[106, 40, 95, 95], rowHeights=27)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), navy), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.8), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#eff4f7"), colors.white]),
    ("LINEBELOW", (0, 0), (-1, 0), 1, teal), ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
table.wrapOn(pdf, 336, 300)
table.drawOn(pdf, right, top - 24 - 27 * len(table_data))
y = top - 24 - 27 * len(table_data) - 16
y = paragraph("<b>Assignment details resolved:</b> Exercises 4-5 accept the exercise 3 filename "
              "as a fallback. Exercise 7 also exports group E, preserving all 958 candidates. "
              "Gender percentages use each displayed population as the denominator.", right, y, 336) - 12
y = paragraph("<b>Local dataset:</b> Individual candidate records and group exports remain local. "
              "Only aggregate results appear in this report.", right, y, 336) - 12
paragraph('<b>Repository:</b> <link href="https://github.com/anupheap/PDI-Lab4" color="#126575">'
          'github.com/anupheap/PDI-Lab4</link>', right, y, 336)
pdf.showPage()

for number, item in enumerate(screenshots, 2):
    caption = ("Source screenshot" if item["kind"] == "source" else "Program output screenshot")
    if item["count"] > 1:
        caption += f" - part {item['part']} of {item['count']}"
    frame(item["title"], f"{caption}. {item['description']}", number)
    image = ImageReader(str(ROOT / item["file"]))
    iw, ih = image.getSize()
    available_width, available_height = width - 72, height - 156
    scale = min(available_width / iw, available_height / ih)
    draw_width, draw_height = iw * scale, ih * scale
    x = (width - draw_width) / 2
    y = 46 + (available_height - draw_height) / 2
    pdf.drawImage(image, x, y, width=draw_width, height=draw_height, mask="auto")
    if item["kind"] == "source":
        pdf.linkURL(f"https://github.com/anupheap/PDI-Lab4/blob/{evidence['source_revision']}/{item['source']}",
                    (x, y, x + draw_width, y + draw_height), relative=0)
    pdf.showPage()
pdf.save()
print(f"Created {destination} ({len(screenshots) + 1} pages)")
