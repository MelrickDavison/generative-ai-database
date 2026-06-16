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

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    documento,
    chunk_index,
    tamanho,
    conteudo
FROM chunks
""")

registros = cursor.fetchall()
print(f"Total de registros encontrados: {len(registros)}")

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

batch_size = 100

for i in range(0, len(registros), batch_size):

    lote = registros[i:i+batch_size]

    textos = [r[4] for r in lote]

    print(
        f"Processando lote "
        f"{i//batch_size + 1} "
        f"de {(len(registros)-1)//batch_size + 1}"
    )

    embeddings = model.encode(
        textos,
        batch_size=32,
        show_progress_bar=False
    )

    points = []

    for registro, embedding in zip(lote, embeddings):

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

    print(f"{len(points)} vetores enviados.")

cursor.close()
conn.close()