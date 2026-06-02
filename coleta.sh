#!/bin/bash

URL="$1"

if [ -z "$URL" ]; then
    echo "Uso: ./coleta.sh <url>"
    exit 1
fi

ARQUIVO=$(basename "$URL").html

MC="/c/Users/davis/Documents/Faculdade/Orion GE-UFAL/projeto-ed2/mc.exe"

echo "Baixando e enviando..."

curl -L "$URL" | "$MC" pipe local/bronze/"$ARQUIVO"

if [ $? -eq 0 ]; then
    echo "Upload concluído!"
else
    echo "Erro no upload!"
fi