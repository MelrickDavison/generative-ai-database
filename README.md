# Banco de Dados para IA Generativa

Projeto desenvolvido para o grupo de estudos de Engenharia de Dados do ORION com o objetivo de construir um pipeline completo para coleta, processamento, armazenamento e recuperação de conhecimento utilizando técnicas de Inteligência Artificial Generativa.

## Visão Geral

O projeto consiste na criação de uma base de conhecimento capaz de:

* Coletar informações de fontes externas.
* Armazenar os dados brutos em um Data Lake.
* Processar e limpar os dados.
* Dividir o conteúdo em chunks.
* Gerar embeddings vetoriais.
* Armazenar textos e vetores em bancos especializados.
* Permitir consultas futuras para aplicações de IA Generativa.

## Arquitetura do Projeto

```text
                 ┌─────────────────┐
                 │   Fontes Web    │
                 └────────┬────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Coleta de Dados  │
                │ Bash + Curl      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Data Lake Bronze │
                │      MinIO       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Transformação    │
                │ Limpeza HTML     │
                │ Markdown/Texto   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Chunking         │
                │ Overlap          │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Embeddings       │
                │ BGE-M3           │
                └───────┬──────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌─────────────────┐           ┌─────────────────┐
│ PostgreSQL      │           │ Qdrant          │
│ Dados Textuais  │           │ Vetores         │
└─────────────────┘           └─────────────────┘
```

## Tecnologias Utilizadas

### Infraestrutura

* Docker
* MinIO

### Coleta de Dados

* Bash
* Curl

### Processamento

* Python
* Markdown
* Chunking

### Armazenamento

* PostgreSQL
* Qdrant

### Inteligência Artificial

* BGE-M3

---

# Cronograma de Desenvolvimento

## Entrega 1 — Coleta e Armazenamento Bronze ✅

## Entrega 2 — Transformação

## Entrega 3 — Chunking

## Entrega 4 — Vetorização

## Entrega 5 — Persistência

---

# Estrutura Atual

```text
.
├── docker-compose.yml
├── coleta.sh
├── dados/
├── README.md
└── docs/
```

---

# Executando a Primeira Entrega

Iniciar os serviços:

```bash
docker compose up -d
```

Executar a coleta:

```bash
./coleta.sh https://pt.wikipedia.org/wiki/Universidade_Federal_de_Alagoas
```

O arquivo coletado será armazenado no bucket Bronze do MinIO.

---
