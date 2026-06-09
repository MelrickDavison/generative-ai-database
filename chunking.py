from minio import Minio
from io import BytesIO

client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="admin123",
    secure=False
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

    chunks = create_chunks(texto)

    nome_base = obj.object_name.replace(".md", "")

    print(f"Total de chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):

        nome_chunk = f"{nome_base}_chunk_{i}.txt"

        dados = chunk.encode("utf-8")

        client.put_object(
            "chuncks",
            nome_chunk,
            BytesIO(dados),
            length=len(dados),
            content_type="text/plain"
        )

        print(f"  -> {nome_chunk}")

    print()

print("Chunking concluído!")