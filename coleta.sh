#!/bin/bash

ENTRADA="$1"

MC="/c/Users/davis/Documents/Faculdade/Orion GE-UFAL/projeto-ed2/mc.exe"

if [ -z "$ENTRADA" ]; then
    echo "Uso: ./coleta.sh <url ou arquivo>"
    exit 1
fi

if [ -f "$ENTRADA" ]; then
    ARQUIVO=$(basename "$ENTRADA")

    echo "Enviando arquivo local $ARQUIVO..."

    "$MC" cp "$ENTRADA" local/bronze/

    exit 0
fi

ARQUIVO="$(basename "$ENTRADA").html"

echo "Baixando e enviando $ARQUIVO..."

HTML=$(curl -L -s "$ENTRADA")

echo "$HTML" | "$MC" pipe local/bronze/"$ARQUIVO"


BASE_URL=$(echo "$ENTRADA" | grep -oE '^https?://[^/]+')
PDFS=$(echo "$HTML" |
grep -oE 'href="[^"]+\.pdf(/view)?"' |
sed 's/href="//' |
sed 's/"//')

if [ -z "$PDFS" ]; then
    echo "Nenhum PDF encontrado na página."
    exit 0
fi

for pdf in $PDFS
do
    echo "PDF encontrado: $pdf"
    pdf_url="${pdf%/view}"

    if [[ ! "$pdf_url" =~ ^https?:// ]]; then
        if [[ ! "$pdf_url" =~ ^/ ]]; then
            pdf_url="/$pdf_url"
        fi
        pdf_url="${BASE_URL}${pdf_url}"
    fi

    NOME_PDF=$(basename "${pdf_url%%\?*}")

    curl -L "$pdf_url" |
    "$MC" pipe local/bronze/"$NOME_PDF"
done

echo "Coleta concluída!"