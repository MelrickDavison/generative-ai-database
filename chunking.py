import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()


def limpar_texto(texto):

    return (
        texto
        .replace('\x00', '')
        .replace('\ufeff', '')
    )


def create_chunks(
    text,
    chunk_size=1200,
    overlap=200
):

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def salvar_chunks(
    documento,
    texto
):

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cursor = conn.cursor()

    texto = limpar_texto(texto)
    chunks = create_chunks(texto)

    ids_chunks = []

    for i, chunk in enumerate(chunks, start=1):

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
            RETURNING id
            """,
            (
                documento,
                i,
                len(chunk),
                chunk
            )
        )

        id_chunk = cursor.fetchone()[0]

        ids_chunks.append(id_chunk)

    conn.commit()

    cursor.close()
    conn.close()

    return ids_chunks