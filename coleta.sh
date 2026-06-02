#!/bin/bash

URL="$1"

if [ -z "$URL" ]; then
    echo "Uso: ./coleta.sh <url>"
    exit 1
fi

mkdir -p dados

ARQUIVO=$(basename "$URL").html

echo "Baixando $URL..."

curl -L "$URL" -o "dados/$ARQUIVO"

echo "Enviando para o MinIO..."

MC="/c/Users/davis/Documents/Faculdade/Orion GE-UFAL/projeto-ed2/mc.exe"

"$MC" cp "dados/$ARQUIVO" local/bronze/

if [ $? -eq 0 ]; then
    echo "Upload concluído!"
else
    echo "Erro no upload!"
fi