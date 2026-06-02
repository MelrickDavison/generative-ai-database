#!/bin/bash

ENTRADA="$1"

MC="/c/Users/davis/Documents/Faculdade/Orion GE-UFAL/projeto-ed2/mc.exe"

if [ -f "$ENTRADA" ]; then
    ARQUIVO=$(basename "$ENTRADA")

    echo "Enviando arquivo local $ARQUIVO..."

    "$MC" cp "$ENTRADA" local/bronze/

else
    ARQUIVO="$(basename "$ENTRADA").html"

    if [ -z "$ENTRADA" ]; then
        echo "Uso: ./coleta.sh <url>"
        exit 1
    fi

    echo "Baixando e enviando $ARQUIVO..."

    curl -L "$ENTRADA" | "$MC" pipe local/bronze/"$ARQUIVO"

    if [ $? -eq 0 ]; then
        echo "Upload concluído!"
    else
        echo "Erro no upload!"
    fi
fi