from minio import Minio
from bs4 import BeautifulSoup
from markdownify import markdownify
from io import BytesIO
from dotenv import load_dotenv
import os
load_dotenv()

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False
)

for objeto in client.list_objects("bronze"):

    resposta = client.get_object(
        "bronze",
        objeto.object_name
    )

    html = resposta.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    markdown = markdownify(str(soup))

    nome_md = objeto.object_name.replace(".html", ".md")

    dados = markdown.encode("utf-8")

    client.put_object(
        "silver",
        nome_md,
        BytesIO(dados),
        length=len(dados),
        content_type="text/markdown"
    )

    print(f"{objeto.object_name} -> {nome_md}")