import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


class ReportGenerator:
    """
    A class to generate a PDF report from a markdown-like string.
    """

    def __init__(self, output_filename="output.pdf"):
        self.output_filename = output_filename
        self.styles = getSampleStyleSheet()
        self.heading_styles = {
            1: ParagraphStyle(
                name="Heading1",
                parent=self.styles["Heading1"],
                fontSize=24,
                leading=28,
                alignment=TA_CENTER,
                spaceAfter=20,
                textColor="black"
            ),
            2: ParagraphStyle(
                name="Heading2",
                parent=self.styles["Heading2"],
                fontSize=22,
                leading=26,
                spaceAfter=18
            ),
            3: ParagraphStyle(
                name="Heading3",
                parent=self.styles["Heading3"],
                fontSize=20,
                leading=24,
                spaceAfter=16
            ),
            4: ParagraphStyle(
                name="Heading4",
                parent=self.styles["Heading4"],
                fontSize=18,
                leading=22,
                spaceAfter=14
            ),
            5: ParagraphStyle(
                name="Heading5",
                parent=self.styles["Heading5"],
                fontSize=16,
                leading=20,
                spaceAfter=12
            ),
            6: ParagraphStyle(
                name="Heading6",
                parent=self.styles["Heading6"],
                fontSize=14,
                leading=18,
                spaceAfter=10
            ),
        }

        self.normal_style = ParagraphStyle(
            name="Normal",
            parent=self.styles["Normal"],
            fontSize=12,
            leading=15,
            spaceAfter=5
        )

    def markdown_to_paragraphs(self, md_text):
        """
        Converts a markdown-like string into a list of ReportLab Flowable objects.

        Args:
            md_text (str): The markdown-formatted text.

        Returns:
            list: A list of ReportLab Flowable objects (Paragraphs and Spacers).
        """
        html_text = re.sub('\*\*(.*?)\*\*', '<b>\1</b>', md_text)
        html_text = re.sub('\[(https?://[^(\]]+)(\(Published:[^\]]+)\]',
                           '<a href="\1"><font color="blue"><u>link</u></font></a>\2', html_text)

        html_text = re.sub('\[[^\]]+\]\((https?://[^\)]+)\)', '<a href="\1"><font color="blue"><u>link</u></font></a>',
                           html_text)

        html_text = re.sub('\[(https?://[^\]]+)\]', '<a href="\1"><font color="blue"><u>link</u></font></a>', html_text)

        lines = html_text.split('\n')
        flowables = []
        for line in lines:
            line = line.strip()
            if not line:
                flowables.append(Spacer(1, 0.2 * inch))
                continue
            if line.startswith("#"):
                if match := re.match('^(#+)\s*(.*)', line):
                    level = len(match[1])
                    text = match[2]
                    style = self.heading_styles.get(level, self.heading_styles[6])
                    flowables.append(Paragraph(text, style))
                    continue
            flowables.append(Paragraph(line, self.normal_style))
        return flowables

    def create_pdf(self, md_text, output_filename=None):
        """
        Generates a PDF from a markdown-like string.

        Args:
            md_text (str): The markdown-formatted input string.
            output_filename (str, optional): The filename for the generated PDF.
                                             Defaults to the output_filename provided during instantiation.
        """
        if output_filename is None:
            output_filename = self.output_filename
        doc = SimpleDocTemplate(output_filename)
        story = self.markdown_to_paragraphs(md_text)
        doc.build(story)
        print(f"PDF '{output_filename}' generated successfully.")


if __name__ == '__main__':
    input_str = "Sample"
    output_pdf = "financial_risk_report.pdf"
    generator = ReportGenerator(output_filename=output_pdf)
    generator.create_pdf(input_str)
