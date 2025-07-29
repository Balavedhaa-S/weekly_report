import markdown2
import pdfkit
import os

PDF_OUTPUT_DIR = "generated_reports"
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)

# Path to wkhtmltopdf.exe (placed manually in your project root)
WKHTMLTOPDF_PATH = os.path.join(os.getcwd(), "wkhtmltopdf.exe")
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def generate_pdf_from_markdown(markdown_text: str, filename: str) -> str:
    try:
        html = markdown2.markdown(markdown_text)

        # Debug: Save HTML to file
        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(html)

        file_path = os.path.join(PDF_OUTPUT_DIR, f"{filename}.pdf")

        print(f"📄 Saving PDF to: {file_path}")
        print(f"🔧 Using wkhtmltopdf from: {WKHTMLTOPDF_PATH}")

        pdfkit.from_string(html, file_path, configuration=config)

        if os.path.exists(file_path):
            print("✅ PDF successfully created.")
        else:
            print("❌ PDF generation failed: file not found.")

        return file_path

    except Exception as e:
        print("❌ Exception during PDF generation:", str(e))
        return ""
