import mammoth
import sys

class DocxToHtmlConverter:
    def __init__(self, docx_file_1, docx_file_2, output_file):
        self.docx_file_1 = docx_file_1
        self.docx_file_2 = docx_file_2
        self.output_file = output_file

    def convert_docx_to_html(self, docx_path):
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            return result.value

    def create_html(self):
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
        with open(self.output_file, "w") as output_file:
            output_file.write(full_html)

def main():
    if len(sys.argv) != 3:
        print("Usage: python concatenate.py <given1.docx> <given2.docx>")
        sys.exit(1)

    docx_file_1 = sys.argv[1]
    docx_file_2 = sys.argv[2]
    output_file = "output.html"

    # Create an instance of the converter class
    converter = DocxToHtmlConverter(docx_file_1, docx_file_2, output_file)
    converter.create_html()
    print(f"HTML file created: {output_file}")

if __name__ == "__main__":
    main()
