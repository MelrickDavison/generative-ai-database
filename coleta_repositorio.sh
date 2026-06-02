#!/bin/bash

URL="$1"

REPO=$(basename "$URL" .git)

if [ ! -d "$REPO" ]; then
    git clone "$URL"
fi

find "./$REPO" -type f -name "*.txt" | while read -r file
do
    echo "Enviando: $file"
    ./coleta.sh "$file"
done