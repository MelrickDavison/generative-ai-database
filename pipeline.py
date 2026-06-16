import subprocess

print("=== Transformação ===", flush=True)
subprocess.run(["python", "-u", "transformacao.py"], check=True)

print("=== Chunking ===", flush=True)
subprocess.run(["python", "-u", "chunking.py"], check=True)

print("=== Vetorização ===", flush=True)
subprocess.run(["python", "-u", "vetorizacao.py"], check=True)

print("Pipeline concluído!", flush=True)