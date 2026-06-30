from flask import Flask, request, jsonify
from transformacao import transformar_html, transformar_pdf
from chunking import salvar_chunks
from vetorizacao import vetorizar_chunks

import requests
from minio import Minio
from io import BytesIO
import os

app = Flask(__name__)

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False
)

for bucket in ["bronze", "silver"]:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


@app.get("/")
def home():
    return "Pipeline online"


@app.post("/site")
def receber_site():

    dados = request.json
    url = dados["url"]

    resposta = requests.get(url)

    nome = url.split("/")[-1] + ".html"

    client.put_object(
        "bronze",
        nome,
        BytesIO(resposta.content),
        len(resposta.content),
        content_type="text/html"
    )

    markdown = transformar_html(resposta.text)

    nome_md = nome.replace(".html", ".md")

    client.put_object(
        "silver",
        nome_md,
        BytesIO(markdown.encode("utf-8")),
        len(markdown.encode("utf-8")),
        content_type="text/markdown"
    )

    ids = salvar_chunks(
        documento=nome_md.replace(".md", ""),
        texto=markdown
    )

    if ids:
        vetorizar_chunks(ids)

    return jsonify({
        "status": "ok",
        "documento": nome_md
    })


@app.post("/pdf")
def receber_pdf():

    dados = request.json
    url = dados["url"]

    resposta = requests.get(url)

    nome = url.split("/")[-1].split("?")[0]

    client.put_object(
        "bronze",
        nome,
        BytesIO(resposta.content),
        len(resposta.content),
        content_type="application/pdf"
    )

    texto = transformar_pdf(resposta.content)

    nome_txt = nome.replace(".pdf", ".txt")

    client.put_object(
        "silver",
        nome_txt,
        BytesIO(texto.encode("utf-8")),
        len(texto.encode("utf-8")),
        content_type="text/plain"
    )

    ids = salvar_chunks(
        documento=nome_txt.replace(".txt", ""),
        texto=texto
    )

    vetorizar_chunks(ids)

    return jsonify({
        "status": "ok",
        "documento": nome_txt
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )