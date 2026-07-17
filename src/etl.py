import os
from datetime import datetime

import pandas as pd


# Leitura dos arquivos
# =====================================================

def listar_arquivos_csv():
    pasta_projeto = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    pasta_raw = os.path.join(
        pasta_projeto,
        "data",
        "raw"
    )

    arquivos_csv = [
        arquivo
        for arquivo in os.listdir(pasta_raw)
        if arquivo.endswith(".csv")
    ]

    arquivos_csv.sort()

    return pasta_projeto, pasta_raw, arquivos_csv


def ler_arquivo_csv(caminho_arquivo):
    return pd.read_csv(
        caminho_arquivo,
        sep=";"
    )


def ler_todos_arquivos(pasta_raw, arquivos):
    dataframes = []

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(
            pasta_raw,
            arquivo
        )

        dataframe = ler_arquivo_csv(caminho_arquivo)
        dataframes.append(dataframe)

    return dataframes


# Consolidação dos dados
# =====================================================

def consolidar_dataframes(dataframes):
    return pd.concat(
        dataframes,
        ignore_index=True
    )


# Validação da estrutura
# =====================================================

def validar_colunas(df):
    colunas_esperadas = [
        "id_venda",
        "data_venda",
        "id_cliente",
        "produto",
        "categoria",
        "quantidade",
        "preco_unitario",
        "vendedor",
        "regiao"
    ]

    colunas_encontradas = list(df.columns)

    if colunas_encontradas != colunas_esperadas:
        raise ValueError(
            "Estrutura de colunas inválida.\n"
            f"Colunas esperadas: {colunas_esperadas}\n"
            f"Colunas encontradas: {colunas_encontradas}"
        )


# Padronização dos dados
# =====================================================

def padronizar_datas(df):
    def converter_data(valor):
        texto_data = str(valor).strip()

        if len(texto_data) >= 4 and texto_data[:4].isdigit():
            return pd.to_datetime(
                texto_data,
                yearfirst=True,
                errors="coerce"
            )

        return pd.to_datetime(
            texto_data,
            dayfirst=True,
            errors="coerce"
        )

    df["data_venda"] = df["data_venda"].apply(
        converter_data
    )

    return df


def padronizar_quantidade(df):
    mapa_quantidade = {
        "um": "1",
        "uma": "1",
        "dois": "2",
        "duas": "2",
        "três": "3",
        "tres": "3",
        "quatro": "4",
        "cinco": "5"
    }

    df["quantidade"] = (
        df["quantidade"]
        .astype(str)
        .str.lower()
        .str.strip()
        .replace(mapa_quantidade)
        .str.extract(r"(\d+)", expand=False)
    )

    df["quantidade"] = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    ).astype("Int64")

    return df


def padronizar_preco(df):
    df["preco_unitario"] = (
        df["preco_unitario"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    df["preco_unitario"] = pd.to_numeric(
        df["preco_unitario"],
        errors="coerce"
    )

    return df


def padronizar_textos(df):
    colunas_texto = [
        "id_venda",
        "id_cliente",
        "produto",
        "categoria",
        "vendedor",
        "regiao"
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    df["produto"] = df["produto"].str.title()
    df["categoria"] = df["categoria"].str.title()
    df["vendedor"] = df["vendedor"].str.title()
    df["regiao"] = df["regiao"].str.title()

    return df


# Tratamento dos dados
# =====================================================

def tratar_valores_nulos(df):
    df["id_cliente"] = df["id_cliente"].fillna(
        "CLIENTE_NAO_INFORMADO"
    )

    df["vendedor"] = df["vendedor"].fillna(
        "NAO_INFORMADO"
    )

    df = df.dropna(
        subset=[
            "data_venda",
            "quantidade",
            "preco_unitario"
        ]
    )

    return df


def remover_duplicados(df):
    quantidade_antes = len(df)

    df = df.drop_duplicates()

    duplicados_removidos = (
        quantidade_antes - len(df)
    )

    return df, duplicados_removidos


# Criação das colunas calculadas
# =====================================================

def criar_colunas_calculadas(df):
    df["faturamento"] = (
        df["quantidade"]
        * df["preco_unitario"]
    )

    df["ano_mes"] = (
        df["data_venda"]
        .dt.strftime("%Y-%m")
    )

    return df


# Exportação dos resultados
# =====================================================

def exportar_dataset(df, pasta_projeto):
    caminho_saida = os.path.join(
        pasta_projeto,
        "data",
        "processed",
        "vendas_consolidadas.csv"
    )

    df.to_csv(
        caminho_saida,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    return caminho_saida


def gerar_log(
    pasta_projeto,
    arquivos_processados,
    registros_importados,
    duplicados_removidos,
    valores_nulos_tratados,
    registros_finais
):
    caminho_log = os.path.join(
        pasta_projeto,
        "logs",
        "processamento.log"
    )

    data_hora = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    resumo = (
        f"Data e hora: {data_hora}\n"
        f"Arquivos processados: {arquivos_processados}\n"
        f"Registros importados: {registros_importados}\n"
        f"Duplicados removidos: {duplicados_removidos}\n"
        f"Valores nulos tratados: {valores_nulos_tratados}\n"
        f"Registros finais: {registros_finais}\n"
        f"{'-' * 40}\n"
    )

    with open(
        caminho_log,
        mode="a",
        encoding="utf-8"
    ) as arquivo_log:
        arquivo_log.write(resumo)

    return caminho_log


# Execução principal do ETL
# =====================================================

def main():
    print("=" * 45)
    print("ETL DE VENDAS COM PYTHON E PANDAS")
    print("=" * 45)

    # Leitura dos arquivos
    # =====================================================

    pasta_projeto, pasta_raw, arquivos = listar_arquivos_csv()

    if not arquivos:
        raise FileNotFoundError(
            "Nenhum arquivo CSV foi encontrado em data/raw."
        )

    dataframes = ler_todos_arquivos(
        pasta_raw,
        arquivos
    )

    registros_importados = sum(
        len(dataframe)
        for dataframe in dataframes
    )

    # Consolidação dos dados
    # =====================================================

    df_consolidado = consolidar_dataframes(
        dataframes
    )

    # Validação da estrutura
    # =====================================================

    validar_colunas(df_consolidado)

    # Padronização dos dados
    # =====================================================

    df_consolidado = padronizar_datas(
        df_consolidado
    )

    df_consolidado = padronizar_quantidade(
        df_consolidado
    )

    df_consolidado = padronizar_preco(
        df_consolidado
    )

    df_consolidado = padronizar_textos(
        df_consolidado
    )

    # Tratamento dos dados
    # =====================================================

    valores_nulos_antes = int(
        df_consolidado
        .isnull()
        .sum()
        .sum()
    )

    df_consolidado = tratar_valores_nulos(
        df_consolidado
    )

    df_consolidado, duplicados_removidos = remover_duplicados(
        df_consolidado
    )

    # Criação das colunas calculadas
    # =====================================================

    df_consolidado = criar_colunas_calculadas(
        df_consolidado
    )

    # Exportação dos resultados
    # =====================================================

    caminho_saida = exportar_dataset(
        df_consolidado,
        pasta_projeto
    )

    caminho_log = gerar_log(
        pasta_projeto=pasta_projeto,
        arquivos_processados=len(arquivos),
        registros_importados=registros_importados,
        duplicados_removidos=duplicados_removidos,
        valores_nulos_tratados=valores_nulos_antes,
        registros_finais=len(df_consolidado)
    )

    # Resumo do processamento
    # =====================================================

    print(f"\nArquivos processados: {len(arquivos)}")
    print(f"Registros importados: {registros_importados}")
    print(f"Duplicados removidos: {duplicados_removidos}")
    print(f"Valores nulos tratados: {valores_nulos_antes}")
    print(f"Registros finais: {len(df_consolidado)}")

    print("\nArquivo exportado com sucesso:")
    print(caminho_saida)

    print("\nLog gerado em:")
    print(caminho_log)


if __name__ == "__main__":
    main()