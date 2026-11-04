import argparse
import io
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable, Image, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--student-name", default="Buntong Anupheap")
parser.add_argument("--student-id", default="P20250055")
parser.add_argument("--class-group", default="I2-Group A (AIECS)")
options = parser.parse_args()
evidence = json.loads((ROOT / "output/report/evidence/runs.json").read_text(encoding="utf-8"))
destination = ROOT / "output/pdf/Lab4_Report.pdf"
destination.parent.mkdir(parents=True, exist_ok=True)
WIDTH, HEIGHT = A4
CONTENT = WIDTH - 92
styles = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=18, leading=23, spaceAfter=14),
    "heading": ParagraphStyle("heading", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=10),
    "subheading": ParagraphStyle("subheading", fontName="Helvetica-Bold", fontSize=11, leading=15, spaceBefore=8, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=10),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=8, leading=10, spaceAfter=10),
}
for style in styles.values():
    style.textColor = colors.black

algorithms = {
    "Exercise1": ["START", "OPEN LuckyNumber.csv for writing", "REPEAT 500 times",
                  "    GENERATE an integer from 1 to 100", "    WRITE the integer to the file",
                  "END REPEAT", "CLOSE the writer", "READ and DISPLAY every saved integer",
                  "DISPLAY the count of 500 numbers", "END"],
    "Exercise2": ["START", "READ a positive file count n", "FOR i = 1 TO n",
                  "    CREATE Ex2LuckyNumber/filei.csv", "    WRITE 500 random integers from 1 to 100",
                  "END FOR", "READ all n files into an ArrayList", "DISPLAY the minimum and maximum", "END"],
    "Exercise3": ["START", "CREATE an empty ArrayList of Students", "REPEAT 3 times",
                  "    READ nonblank name, ID, and gender", "    CREATE and ADD a Student object",
                  "END REPEAT", "WRITE the header and escaped CSV records", "SAVE Ex3StudentData.csv", "END"],
    "Exercise4": ["START", "SELECT StudentData.csv or Ex3StudentData.csv", "READ and validate the CSV header",
                  "CREATE an empty ArrayList", "FOR EACH student record",
                  "    PARSE fields and ADD a Student object", "END FOR", "DISPLAY each Student object", "END"],
    "Exercise5": ["START", "LOAD the saved students into an ArrayList", "READ and ADD three more Students",
                  "SORT by name A-Z, ignoring case", "WRITE the sorted list to StudentData.csv",
                  "DISPLAY the sorted list", "END"],
    "Exercise6": ["START", "READ the CSV and locate the actual header", "PARSE and validate candidate records",
                  "COUNT all candidates and gender percentages", "FILTER average scores >= 90 and summarize gender",
                  "COUNT scores >= 85 in each subject", "COUNT candidates with all three scores >= 85",
                  "GROUP candidates and calculate group percentages", "DISPLAY all answers", "END"],
    "Exercise7": ["START", "READ candidates and GROUP them by group name", "ENSURE groups A, B, C, and D exist",
                  "FOR EACH group, including group E when present", "    WRITE the header and original candidate records",
                  "    APPEND total students and male/female percentages", "    DISPLAY the group statistics",
                  "END FOR", "DISPLAY the number of exported candidates", "END"],
    "BonusExercise": ["START", "LOAD the original Student objects", "SERIALIZE the objects to BonusStudents.csv",
                      "DESERIALIZE the CSV into new Student objects", "DISPLAY the restored objects",
                      "COMPARE the original and restored lists", "IF equal THEN DISPLAY round-trip verified",
                      "ELSE REPORT a round-trip error", "END"],
}
flows = {
    "Exercise1": ["Generate and write 500 integers", "Close LuckyNumber.csv", "Read and display every saved value"],
    "Exercise2": ["Read and validate positive n", "Create n files with 500 numbers each", "Read the files; display minimum and maximum"],
    "Exercise3": ["Read three students", "Create Student objects in an ArrayList", "Write the header and escaped CSV records"],
    "Exercise4": ["Choose the student CSV", "Parse records into an ArrayList of Students", "Display the objects in the ArrayList"],
    "Exercise5": ["Load students and add three more", "Sort names A-Z", "Save StudentData.csv and display the list"],
    "Exercise6": ["Read and validate the candidate CSV", "Calculate totals and score-threshold statistics", "Calculate and display each group's statistics"],
    "Exercise7": ["Read candidates and form groups", "Write records and summary rows to each group CSV", "Display group statistics and the export count"],
    "BonusExercise": ["Read and serialize Student objects", "Deserialize and display restored objects", "Compare the original and restored lists"],
}


class Flowchart(Flowable):
    def __init__(self, labels):
        Flowable.__init__(self)
        self.labels = ["START", *labels, "END"]
        self.width = CONTENT
        self.height = len(self.labels) * 32 + (len(self.labels) - 1) * 14

    def draw(self):
        pdf = self.canv
        center = self.width / 2
        pdf.setStrokeColor(colors.HexColor("#444444"))
        pdf.setLineWidth(0.7)
        for i, label in enumerate(self.labels):
            y = self.height - i * 46 - 32
            width = 100 if i in (0, len(self.labels) - 1) else 360
            pdf.setFillColor(colors.HexColor("#f5f5f5"))
            if i in (0, len(self.labels) - 1):
                pdf.roundRect(center - width / 2, y, width, 32, 16, stroke=1, fill=1)
            else:
                pdf.rect(center - width / 2, y, width, 32, stroke=1, fill=1)
            pdf.setFillColor(colors.black)
            pdf.setFont("Helvetica", 9)
            pdf.drawCentredString(center, y + 12, label)
            if i < len(self.labels) - 1:
                pdf.line(center, y, center, y - 10)
                arrow = pdf.beginPath()
                arrow.moveTo(center - 2.5, y - 9)
                arrow.lineTo(center, y - 14)
                arrow.lineTo(center + 2.5, y - 9)
                pdf.drawPath(arrow)


story = []


def text(value, style="body"):
    story.append(Paragraph(value, styles[style]))


def source(filename, title):
    image = PILImage.open(ROOT / "output/report/codesnap" / filename.replace(".java", ".png")).convert("RGB")
    image = image.crop((130, 130, image.width - 130, image.height - 130))
    scale = CONTENT / image.width
    parts = math.ceil(image.height * scale / 680)
    offset = 0
    for part in range(parts):
        story.append(PageBreak())
        text(escape(title + (" - continued" if offset else "")), "heading")
        text(escape(filename))
        remaining = image.height - offset
        take = remaining if part == parts - 1 else math.ceil(remaining / (parts - part))
        if part < parts - 1:
            boundary = 238 + math.floor((offset + take + 130 - 238) / 36) * 36
            take = boundary - 130 - offset
        segment = image.crop((0, offset, image.width, offset + take))
        buffer = io.BytesIO()
        segment.save(buffer, format="PNG")
        buffer.seek(0)
        story.append(Image(buffer, width=CONTENT, height=segment.height * scale))
        offset += take
    return segment.height * scale


for index, run in enumerate(evidence["runs"]):
    if index:
        story.append(PageBreak())
    else:
        text("Lab 04 - File I/O in Java", "title")
        for label, value in [("Student name", options.student_name), ("Student ID", options.student_id),
                             ("Class / Group", options.class_group)]:
            text(f"<b>{label}:</b> {escape(value) if value else '____________________________'}")
    name = run["class"]
    text(escape(run["title"].replace(" - ", ": ", 1)), "heading")
    text(escape(run["description"]))
    if name in ("Exercise3", "Exercise5"):
        text("The sample student details are fictional.")
    if name == "Exercise7":
        text("The supplied dataset includes group E, so five files preserve all 958 candidates.")
    text("Pseudocode", "subheading")
    story.append(Preformatted("\n".join(algorithms[name]), styles["code"]))
    text("Flowchart", "subheading")
    story.append(Flowchart(flows[name]))
    last_image_height = source(name + ".java", run["title"].split(" - ")[0] + " - Source code")
    lines = ["Command: " + run["command"], ""]
    if run["stdin"]:
        lines.extend(["Sample input:", *run["stdin"].rstrip().splitlines(), ""])
    lines.extend(["Program output:", *run["stdout"].rstrip().splitlines()])
    required = sum(max(1, math.ceil(len(line) / 101)) for line in lines) * 10 + 40
    if required > 696 - last_image_height:
        story.append(PageBreak())
    else:
        story.append(Spacer(1, 12))
    text("Sample input and output", "subheading")
    story.append(Preformatted("\n".join(lines), styles["code"], maxLineLength=101))

for filename in ["ConsoleInput.java", "Csv.java", "Student.java", "StudentData.java",
                 "Candidate.java", "CandidateData.java", "CandidateStatistics.java"]:
    source(filename, "Shared source code")

story.append(PageBreak())
text("Verification", "heading")
text("Compiled for Java 17 and checked against independent CSV calculations. Candidate records "
     "and group exports stay local. The report contains aggregate candidate results.")
text("Code images were generated with the CodeSnap RS 0.3.0 adapter from "
     "anupheap/codesnap-rs-vscode, installed in VS Code.")
story.append(Preformatted(evidence["verification"].rstrip(), styles["code"], maxLineLength=101))
text('<b>Git repository:</b> <link href="https://github.com/anupheap/PDI-Lab4" '
     'color="black">https://github.com/anupheap/PDI-Lab4</link>')


def footer(pdf, document):
    pdf.saveState()
    pdf.setStrokeColor(colors.HexColor("#cccccc"))
    pdf.setLineWidth(0.5)
    pdf.line(40, 29, WIDTH - 40, 29)
    pdf.setFillColor(colors.HexColor("#555555"))
    pdf.setFont("Helvetica", 8)
    label = "Lab 04" + (" - " + options.student_name if options.student_name else " - File I/O in Java")
    pdf.drawString(40, 17, label)
    pdf.drawRightString(WIDTH - 40, 17, f"Page {document.page}")
    pdf.restoreState()


document = SimpleDocTemplate(str(destination), pagesize=A4, leftMargin=40, rightMargin=40,
                             topMargin=42, bottomMargin=36, title="Lab 04 - File I/O in Java")
document.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Created {destination}")
