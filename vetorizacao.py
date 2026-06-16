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

for registro in registros:

    id_chunk = registro[0]
    documento = registro[1]
    indice = registro[2]
    tamanho = registro[3]
    texto = registro[4]

    print(f"Vetorizando chunk {id_chunk} - {documento}")
    embeddings = model.encode(
    lista_textos,
    batch_size=32,
    show_progress_bar=True
)

    client.upsert(
        collection_name="documentos",
        points=[
            PointStruct(
                id=id_chunk,
                vector=embedding.tolist(),
                payload={
                    "documento": documento,
                    "chunk_index": indice,
                    "tamanho": tamanho,
                    "texto": texto
                }
            )
        ]
    )
print("Vetorização concluída!")