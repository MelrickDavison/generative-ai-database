from bs4 import BeautifulSoup
from markdownify import markdownify
import fitz

fitz.TOOLS.mupdf_display_errors(False)


def transformar_html(html: str) -> str:

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    markdown = markdownify(str(soup))

    return markdown


def transformar_pdf(pdf_bytes: bytes) -> str:

    texto = ""

    with fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as pdf:

        for pagina in pdf:
            texto += pagina.get_text()

    return texto