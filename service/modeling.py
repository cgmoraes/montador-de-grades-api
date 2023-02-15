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
        self.ucs = pd.DataFrame(pd.read_csv(file_name, encoding="utf-8", sep=";", keep_default_na=False))

    # Método privado para agrupar os dados pela chave ID, NOME, TURMA e PROFESSORES, e juntar as listas de dias e horários
    def __group_by(self, df):
        return df.groupby(["ID", "NOME", "TURMA", "PROFESSORES"], as_index=False).\
        agg({"DIA":list, "HORARIO":list})

    def get_ucs(self):
        # Retorna um dicionário gerado a partir de self.ucs agrupado por ID, NOME, TURMA e PROFESSORES, 
        # e juntar as listas de dias e horários
        return (self.__group_by(self.ucs)).to_dict("records")

    def uc_analyzer(self, data):
        # Se não houver dados, retorna a lista completa de UCs em self.ucs
        if not len(data): pre_result = self.ucs
        else:
            # Seleciona as UCs presentes em data
            sub_ucs = self.ucs.loc[self.ucs["ID"].isin(data), ["NOME", "DIA", "HORARIO"]]
            # Gera uma lista com nome das UCs em data
            uc_names = list(sub_ucs["NOME"].unique())

            # Combina sub_ucs com self.ucs pelos DIA e HORARIO das UCs, trazendo todas as disciplinas
            # que apresentam conflito de dia e horário com as UCs selecionadas em data
            sub_ucs = self.ucs.merge(sub_ucs[["DIA", "HORARIO"]], how='outer', indicator=True)

            # Cria uma lista com os IDs das UCs selecionadas em data
            list_result = list(sub_ucs.loc[sub_ucs["NOME"].isin(uc_names), "ID"].unique())

            # Adiciona à lista os IDs das UCs que tiveram os conflitos mencionados
            list_result += list(sub_ucs.loc[sub_ucs["_merge"] == "both", "ID"].unique())

            # Filtra self.ucs pelos IDs que não estão em list_result
            pre_result = self.ucs[~self.ucs["ID"].isin(list_result)]
        
        # Retorna o resultado agrupado como dicionário aplicado em pre_result
        return (self.__group_by(pre_result)).to_dict("records")
