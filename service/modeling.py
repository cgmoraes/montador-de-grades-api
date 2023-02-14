import os
import pandas as pd

from google.cloud import storage

class Modeling():

    def __init__(self):
        # Nome do bucket e nome dos arquivos que serão baixados do GCP
        bucket_name = 'arquivos-api'
        file_name = 'ucs.csv'

        # Instanciando cliente do GCP
        client = storage.Client()

        # Recuperando o bucket do GCP pelo nome e baixando os arquivos especificados
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(file_name)

        # Lendo os arquivos csv como dataframe do pandas e atribuindo-os ao objeto
        self.ucs = pd.DataFrame(pd.read_csv("ucs.csv", encoding="utf-8", sep=";"))

    # Método privado para converter um dataframe para um dicionário de registros
    def _df_to_dict(df):
        return df.to_dict("records")

    # Método privado para agrupar os dados pela chave ID, NOME, TURMA e PROFESSORES, e juntar as listas de dias e horários
    def _group_by(df):
        return df.groupby(["ID", "NOME", "TURMA", "PROFESSORES"], as_index=False).\
        agg({"DIA":lambda x: list(x), "HORARIO":lambda x: list(x)})

    def get_ucs(self):
        # Retorna um dicionário gerado a partir de self.ucs agrupado por ID, NOME, TURMA e PROFESSORES, 
        # e juntar as listas de dias e horários
        return Modeling._df_to_dict(Modeling._group_by(self.ucs))

    def uc_analizer(self, data):
        # Se não houver dados, retorna a lista completa de UCs em self.ucs
        if not len(data): pre_result = self.ucs
        else:
            # Seleciona as UCs presentes em data
            data = list(self.ucs.loc[self.ucs["ID"].isin(data), "NOME"].unique())
            # Seleciona os dias e horários de cada UC em data
            sub_ucs = self.ucs.loc[self.ucs["NOME"].isin(data), ["DIA", "HORARIO"]]
            
            # Combina sub_ucs com self.ucs pelos IDs das UCs, preservando todas as linhas
            sub_ucs = self.ucs.merge(sub_ucs, how='outer', indicator=True)
            
            # Seleciona a lista de IDs de UCs presentes em sub_ucs e não presentes em data
            list_result = sub_ucs.loc[sub_ucs["_merge"] == "both", "ID"].unique()
            # Filtra self.ucs pelos IDs que não estão em list_result
            pre_result = self.ucs[~self.ucs["ID"].isin(list_result)]
        
        # Retorna o resultado agrupado como dicionário aplicada em pre_result
        return Modeling._df_to_dict(Modeling._group_by(pre_result))
