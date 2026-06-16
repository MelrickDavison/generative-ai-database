from minio import Minio
from dotenv import load_dotenv
import psycopg2
import os
load_dotenv()

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False
)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

def limpar_texto(texto):
    return (
        texto
        .replace('\x00', '')
        .replace('\ufeff', '')
    )

def create_chunks(text, chunk_size=1200, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


print("Lendo arquivos da Silver...\n")

for obj in client.list_objects("silver"):

    print(f"Processando: {obj.object_name}")

    response = client.get_object(
        "silver",
        obj.object_name
    )

    texto = response.read().decode("utf-8")

    texto = limpar_texto(texto)
    
    chunks = create_chunks(texto)

    nome_base = obj.object_name.replace(".md", "")

    print(f"Total de chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):

        nome_chunk = f"{nome_base}_chunk_{i}.txt"

        dados = chunk.encode("utf-8")

        cursor.execute(
            """
            INSERT INTO chunks
            (
                documento,
                chunk_index,
                tamanho,
                conteudo
            )
            VALUES (%s,%s,%s,%s)
            """,
            (nome_base, i, len(chunk), chunk)
        )

conn.commit()
cursor.close()
conn.close()

print("Chunking concluído!")