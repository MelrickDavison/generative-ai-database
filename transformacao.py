from minio import Minio
from bs4 import BeautifulSoup
from markdownify import markdownify
from io import BytesIO
from dotenv import load_dotenv
import fitz
import os

load_dotenv()

fitz.TOOLS.mupdf_display_errors(False)

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False
)

def enviar_dados(nome_saida, dados_saida):

    try:
        client.stat_object("silver", nome_saida)

        print(f"{nome_saida} já existe na Silver.")
        return

    except:
        pass

    client.put_object(
        "silver",
        nome_saida,
        BytesIO(dados_saida),
        length=len(dados_saida),
        content_type=content_type
    )

    print(f"Arquivo enviado: {nome_saida}")

def pdf_para_texto(pdf_bytes):
    texto = ""

    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        for pagina in pdf:
            texto += pagina.get_text()

    return texto

for objeto in client.list_objects("bronze"):

    nome = objeto.object_name
    resposta = client.get_object(
            "bronze",
            nome
        )

    if nome.endswith(".html"):
        html = resposta.read().decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        markdown = markdownify(str(soup))

        nome_saida = nome.replace(".html", ".md")
        dados_saida = markdown.encode("utf-8")
        content_type = "text/markdown"

        enviar_dados(nome_saida, dados_saida, content_type)

    elif nome.endswith(".pdf"):
        dados_pdf = resposta.read()
        texto = pdf_para_texto(dados_pdf)
        
        nome_saida = nome.replace(".pdf", ".txt")
        dados_saida = texto.encode("utf-8")
        content_type = "text/plain"

        enviar_dados(nome_saida, dados_saida, content_type)   