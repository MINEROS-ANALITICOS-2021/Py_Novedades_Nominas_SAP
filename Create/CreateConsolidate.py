import pandas as pd
import os

class Consolidate:

    def __init__(self, filequery1, filequery2, pathdirectory):
        self.filequery1 = filequery1
        self.filequery2 = filequery2
        self.pathdirectory = pathdirectory


    def merge_csv_files(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.filequery1)
        df2 = pd.read_csv(self.filequery2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Sociedad',
                             right_on='Descripcion de Sociedad',
                             how='left')

        merged_df.drop(columns=['Poblacion'], inplace=True)
        merged_df.drop(columns=['Moneda'], inplace=True)
        # guardar CSV
        merged_df.to_csv(os.path.join(self.pathdirectory, "002_Consolidate_FLEXI_PARAMETRICAS.csv"), index=False)

        return "ok"

    def consolidate_end(self) -> str:

        # Leer archivos CSV
        df1 = pd.read_excel(self.filequery1)
        # Leer archivos CSV
        df2= pd.read_csv(self.filequery2)


        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='Número de personal',
                             how='left')

        # guardar CSV
        merged_df.to_csv(os.path.join(self.pathdirectory, "004_Consolidate_END.csv"), index=False)

        return "ok"

    def consolidate_param_posicion(self) -> str:

        # Leer archivos CSV
        df1 = pd.read_csv(self.filequery1)
        # Leer archivos CSV
        df2= pd.read_csv(self.filequery2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Posición',
                             right_on='Posicion',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Posicion', 'Área de personal', 'Sociedad_y', 'Area', 'Descripcion de Sociedad'], inplace=True)


        # guardar CSV
        merged_df.to_csv(os.path.join(self.pathdirectory, "003_Consolidate_POSICION_PARAM.csv"), index=False)

        return "ok"

    def merge_AVG_GNR(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.filequery1)
        df2 = pd.read_csv(self.filequery2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Persona',
                             right_on='No.Empl.',
                             how='inner')

        merged_df.drop(columns=['No.Empl.'], inplace=True)

        # guardar CSV
        merged_df.to_csv(os.path.join(self.pathdirectory, "Consolidate_AVG_GNR.csv"), index=False)

        return "ok"

    def merge_ROWS_PROCESS(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.filequery1)
        df2 = pd.read_csv(self.filequery2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Codigo',
                             right_on='Persona',
                             how='inner')

        merged_df.drop(columns=['Persona', 'Unindad', 'formatted_quantity','variante_code', 'position_code',
                                'description_id', 'formatted_Descrip'], inplace=True)

        # guardar CSV
        merged_df.to_csv(os.path.join(self.pathdirectory, "Consolidate_TOTAL.csv"), index=False)

        return "ok"

    def merge_change_amount(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.filequery1)
        df2 = pd.read_csv(self.filequery2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Codigo',
                             right_on='Codigo',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Posicion_y', 'Sociedad_y',
                                'Variante_y', 'Cantidad_y', 'Val_Posicion_y',
                                'group_valid_y', 'Promedio(3)_y', 'NOMBRE_y'], inplace=True)

        # guardar CSV
        merged_df.to_csv(os.path.join(self.pathdirectory, "007_Consolidate_Add_Change_Amount.csv"), index=False)

        return "ok"
