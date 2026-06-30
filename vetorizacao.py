import os
import psycopg2

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

load_dotenv()

model = SentenceTransformer(
    "BAAI/bge-m3"
)

client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    port=os.getenv("QDRANT_PORT")
)

if not client.collection_exists("documentos"):

    client.create_collection(
        collection_name="documentos",
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )


def vetorizar_chunks(ids_chunks):

    if not ids_chunks:
        print("Nenhum chunk novo para vetorizar.")
        return

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            documento,
            chunk_index,
            tamanho,
            conteudo
        FROM chunks
        WHERE id = ANY(%s)
        """,
        (ids_chunks,)
    )

    registros = cursor.fetchall()
    print(f"Vetorizando {len(registros)} chunks...")

    textos = [r[4] for r in registros]

    embeddings = model.encode(
        textos,
        batch_size=32
    )

    points = []

    for registro, embedding in zip(
        registros,
        embeddings
    ):

        points.append(
            PointStruct(
                id=registro[0],
                vector=embedding.tolist(),
                payload={
                    "documento": registro[1],
                    "chunk_index": registro[2],
                    "tamanho": registro[3],
                    "texto": registro[4]
                }
            )
        )

    client.upsert(
        collection_name="documentos",
        points=points
    )

    print(f"{len(points)} vetores enviados ao Qdrant.")

    cursor.executemany(
        """
        UPDATE chunks
        SET vetorizado = TRUE
        WHERE id = %s
        """,
        [(id_chunk,) for id_chunk in ids_chunks]
    )
    
    print("Chunks marcados como vetorizados.")

    conn.commit()

    cursor.close()
    conn.close()