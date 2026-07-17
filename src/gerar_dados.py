import csv
import os


PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_RAW = os.path.join(PASTA_PROJETO, "data", "raw")

COLUNAS = [
    "id_venda",
    "data_venda",
    "id_cliente",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
    "vendedor",
    "regiao",
]

ARQUIVOS_VENDAS = {
    "vendas_janeiro.csv": [
        ["V001", "05/01/2026", "C001", "Notebook", "Eletrônicos", "1", "3500,00", "Ana Souza", "Sudeste"],
        ["V002", "10/01/2026", "C002", "Mouse", "Acessórios", "2", "85,50", "Carlos Lima", "Sul"],
        ["V003", "15/01/2026", "C003", "Teclado", "Acessórios", "1", "150,00", "Mariana Alves", "Sudeste"],
        ["V004", "20/01/2026", "C004", "Monitor", "Eletrônicos", "2", "1200,00", "João Santos", "Nordeste"],
        ["V005", "25/01/2026", "C005", "Cadeira Gamer", "Móveis", "1", "950,00", "Ana Souza", "Centro-Oeste"],
    ],
    "vendas_fevereiro.csv": [
        ["V006", "2026-02-03", "C006", "Webcam", "Acessórios", "1", "320.00", "Carlos Lima", "Sul"],
        ["V007", "2026-02-08", "C007", "Headset", "Acessórios", "2", "210.50", "Mariana Alves", "Sudeste"],
        ["V008", "2026-02-14", "C008", "Impressora", "Eletrônicos", "1", "780.00", "João Santos", "Nordeste"],
        ["V009", "2026-02-19", "C009", "Mesa Escritório", "Móveis", "1", "650.00", " Ana Souza ", "Centro-Oeste"],
        ["V010", "2026-02-25", "C010", "Notebook", "ELETRÔNICOS", "1", "4200.00", "Carlos Lima", "Sul"],
    ],
    "vendas_marco.csv": [
        ["V011", "03-03-2026", "C011", "Mouse", "acessórios", "3", "90,00", "Mariana Alves", "sudeste"],
        ["V012", "09-03-2026", "C012", "Monitor", "Eletrônicos", "1", "1350,00", "João Santos", "NORDESTE"],
        ["V013", "15-03-2026", "C013", "Cadeira Gamer", "Móveis", "", "1100,00", "Ana Souza", "Centro-Oeste"],
        ["V014", "21-03-2026", "", "Teclado", "Acessórios", "2", "175,00", "Carlos Lima", "Sul"],
        ["V015", "28-03-2026", "C015", "Webcam", "Acessórios", "1", "", "Mariana Alves", "Sudeste"],
    ],
    "vendas_abril.csv": [
        ["V016", "04/05/2026", "C016", "Impressora", "Eletrônicos", "1 unidade", "820,00", "João Santos", "Nordeste"],
        ["V017", "10/04/2026", "C017", "Mesa Escritório", "Móveis", "2", "700,00", "Ana Souza", "Centro-Oeste"],
        ["V018", "18/04/2026", "C018", "Headset", "Acessórios", "dois", "230,00", "Carlos Lima", "Sul"],
        ["V019", "23/04/2026", "C019", " Notebook ", "Eletrônicos", "1", "3900,00", "Mariana Alves", "Sudeste"],
        ["V020", "30/04/2026", "C020", "Mouse", "Acessórios", "4", "95,00", "", "Sul"],
    ],
    "vendas_maio.csv": [
        ["V021", "2026/05/05", "C021", "Monitor", "eletrônicos", "1", "1450.00", "João Santos", "Nordeste"],
        ["V022", "2026/05/11", "C022", "Teclado", "ACESSÓRIOS", "2", "180.00", "Ana Souza", "Centro-Oeste"],
        ["V023", "2026/05/17", "C023", "Webcam", "Acessórios", "1", "350.00", "Carlos Lima", "Sul"],
        ["V024", "2026/05/22", "C024", "Cadeira Gamer", "Móveis", "1", "1250.00", "Mariana Alves", "Sudeste"],
        ["V025", "2026/05/29", "C025", "Impressora", "Eletrônicos", "1", "900.00", "João Santos", "Nordeste"],
        ["V010", "2026-02-25", "C010", "Notebook", "ELETRÔNICOS", "1", "4200.00", "Carlos Lima", "Sul"],
    ],
}


def criar_arquivos_csv():
    os.makedirs(PASTA_RAW, exist_ok=True)

    for nome_arquivo, registros in ARQUIVOS_VENDAS.items():
        caminho_arquivo = os.path.join(PASTA_RAW, nome_arquivo)

        with open(
            caminho_arquivo,
            mode="w",
            newline="",
            encoding="utf-8-sig",
        ) as arquivo_csv:
            escritor = csv.writer(arquivo_csv, delimiter=";")
            escritor.writerow(COLUNAS)
            escritor.writerows(registros)

        print(f"Arquivo criado: {nome_arquivo}")

    print("\n5 arquivos CSV criados com sucesso.")
    print(f"Local: {PASTA_RAW}")


if __name__ == "__main__":
    criar_arquivos_csv()