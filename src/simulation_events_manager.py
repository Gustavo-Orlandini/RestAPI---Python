from fastapi import HTTPException
import pandas as pd

class SimulationEventsManager: 
    def __init__(self, df_default: pd.DataFrame):
        self.df_default = df_default

    def validate_required_columns(self, df: pd.DataFrame):
        required_columns = ['SIGLA X', 'TIPO DE ID', 'DATA', 'ID DO ATIVO', 'SIGLA Y', 'VALOR']
        missing_values_columns = [col for col in required_columns if any(df[col].isnull())]

        if missing_values_columns:
            raise HTTPException(status_code=400, detail=f"As seguintes colunas obrigatórias estão com campos vazios: {', '.join(missing_values_columns)}. Preencha todos os campos obrigatórios e tente novamente.")

    def validate_sigla_x(self, df: pd.DataFrame):
        invalid_sigla_x_values = df.loc[~df['SIGLA X'].isin(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']), 'SIGLA X']

        if not invalid_sigla_x_values.empty:
            error_detail = f"Valores incorretos na coluna SIGLA X nas linhas {', '.join(map(str, invalid_sigla_x_values.index))}: {', '.join(invalid_sigla_x_values)}"
            raise HTTPException(status_code=400, detail=error_detail)

    def validate_id_ativo(self, df: pd.DataFrame):
        invalid_id_ativo_values = df.loc[~df['ID DO ATIVO'].isin([1, 2, 3, 4, 5, 6, 7, 8]), 'ID DO ATIVO']
        print(invalid_id_ativo_values)

        if not invalid_id_ativo_values.empty:
            invalid_rows = [index + 2 for index in invalid_id_ativo_values.index]
            error_detail = f"Valores incorretos na coluna ID DO ATIVO nas linhas {', '.join(map(str, invalid_rows))}: {', '.join(map(str, invalid_id_ativo_values))}"
            raise HTTPException(status_code=400, detail=error_detail)

    def process_simulator_events(self, df: pd.DataFrame, cur, conn):
        expected_columns = ['SIGLA X', 'TIPO DE ID', 'DATA', 'ID DO ATIVO', 'DESCRICAO', 'SIGLA Y', 'VALOR']

        for _, row in df[expected_columns].iterrows():
            parsed_data = pd.to_datetime(row['DATA'], dayfirst=True).strftime('%Y-%m-%d')
            descricao = row['DESCRICAO'] if pd.notnull(row['DESCRICAO']) else None

            insert_query = "INSERT INTO fato_eventos_simulacao (sigla_x, id_tipo, data, id_ativo, descricao, sigla_y, valor, id_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query, (row['SIGLA X'], row['TIPO DE ID'], parsed_data, row['ID DO ATIVO'], descricao, row['SIGLA Y'], row['VALOR'], "Gustavo_teste"))
            conn.commit()

    def process_simulation_file(self, cur, conn):
        if self.df_default.empty:
            raise HTTPException(status_code=400, detail="A planilha está vazia. Por favor, preencha os dados e tente novamente.")
        
        self.validate_required_columns(self.df_default)
        self.validate_sigla_x(self.df_default)
        self.validate_id_ativo(self.df_default)
        self.process_simulator_events(self.df_default, cur, conn)

        return {"message": "Salvo com sucesso"}

