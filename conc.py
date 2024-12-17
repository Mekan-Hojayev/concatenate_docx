import sys
from docx import Document
from html import escape

class DocxToHtmlConverter:
    def __init__(self, docx_file_1, docx_file_2, output_file):
        self.docx_file_1 = docx_file_1
        self.docx_file_2 = docx_file_2
        self.output_file = output_file

    def style_run_to_html(self, run):
        """
        Convert a single run of text into styled HTML.
        """
        text = escape(run.text)

        if not text.strip():  # Skip empty runs
            return ""

        # Initialize style container
        styles = []

        # Check for various styles and apply corresponding HTML
        if run.bold:
            styles.append("font-weight: bold;")
        if run.italic:
            styles.append("font-style: italic;")
        if run.underline:
            styles.append("text-decoration: underline;")
        if run.font.strike:
            styles.append("text-decoration: line-through;")
        if run.font.color and run.font.color.rgb:
            styles.append(f"color: #{run.font.color.rgb};")
        if run.font.highlight_color:
            # Highlight colors
            highlight_color = run.font.highlight_color
            if highlight_color:
                styles.append(f"background-color: yellow;")  # Defaults to yellow

        # Build the style attribute for inline CSS
        style_attr = f' style="{" ".join(styles)}"' if styles else ""

        return f"<span{style_attr}>{text}</span>"

    def convert_docx_to_html(self, docx_path):
        """
        Convert a DOCX file to HTML while preserving formatting.
        """
        document = Document(docx_path)
        html_content = ""

        for paragraph in document.paragraphs:
            paragraph_html = ""
            for run in paragraph.runs:
                paragraph_html += self.style_run_to_html(run)

            html_content += f"<p>{paragraph_html}</p>"

        return html_content

    def create_html(self):
        """
        Create a combined HTML file with two columns.
        """
        # Convert both docx files to HTML
        html_content_1 = self.convert_docx_to_html(self.docx_file_1)
        html_content_2 = self.convert_docx_to_html(self.docx_file_2)

        # Create HTML structure with two columns
        full_html = f"""
        <html>
        <head>
            <style>
                .container {{
                    display: flex;
                    width: 100%;
                    height: 100vh;
                }}
                .left-pane {{
                    width: 50%;
                    padding: 20px;
                    overflow-y: scroll;
                    border-right: 1px solid #ccc;
                }}
                .right-pane {{
                    width: 50%;
                    padding: 20px;
                    overflow-y: scroll;
                }}
                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                }}
                p {{
                    margin: 10px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="left-pane">
                    {html_content_1}
                </div>
                <div class="right-pane">
                    {html_content_2}
                </div>
            </div>
        </body>
        </html>
        """

        # Write the HTML output to the file
        with open(self.output_file, "w", encoding="utf-8") as output_file:
            output_file.write(full_html)

def main():
    if len(sys.argv) != 3:
        print("Usage: python concatenate.py <given1.docx> <given2.docx>")
        sys.exit(1)

    docx_file_1 = sys.argv[1]
    docx_file_2 = sys.argv[2]
    output_file = "reg_duma.html"

    # Create an instance of the converter class
    converter = DocxToHtmlConverter(docx_file_1, docx_file_2, output_file)
    converter.create_html()
    print(f"HTML file created: {output_file}")

if __name__ == "__main__":
    main()