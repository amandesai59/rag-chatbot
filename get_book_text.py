import os
import sys
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ File not found: {pdf_path}")

    book_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)
    txt_file = os.path.join(output_dir, f"{book_name}.txt")

    print(f"📖 Extracting text from: {pdf_path}")
    doc = fitz.open(pdf_path)

    with open(txt_file, "w", encoding="utf-8") as f:
        for page in doc:
            text = page.get_text()
            if text.strip():  # skip blank pages
                f.write(text.strip() + "\n\n")

    print(f"✅ Text saved to: {txt_file}")
    return txt_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_book_text.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"❌ Error: {e}")
