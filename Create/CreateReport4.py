import os
import re
import pandas as pd
from io import StringIO

class Reports4:
    def __init__(self, input_file1, input_file2, output_folder):
        self.input_file1 = input_file1
        self.input_file2 = input_file2
        self.output_folder = output_folder

    def arreglo_comparison_file_HANA(self) -> str:
        def is_valid_line(line, seen_document):
            """
            Determina si una línea es válida según los criterios especificados:
            - Contiene 10 dígitos seguidos.
            - Contiene las frases específicas: "El documento ya ha sido anulado",
              "Anulado con documento", "Nº documento", "PRESUPUESTO", "Imposible anular:".
            """
            has_10_digits = bool(re.search(r'\d{10}', line))
            contains_phrase = any(phrase in line for phrase in [
                "El documento ya ha sido anulado",
                "Anulado con documento",
                "PRESUPUESTO",
                "Imposible anular:"
            ])
            if "Nº documento" in line:
                if seen_document[0]:
                    return False
                else:
                    seen_document[0] = True
                    return True
            return has_10_digits or contains_phrase

        archivo_inicial = self.input_file1
        archivo_anulado = self.input_file2
        nombre_hoja = 'Base_principal'

        # Leer el archivo de texto
        with open(archivo_anulado, 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()

        # Filtrar solo las líneas válidas
        seen_document = [False]
        valid_lines = [line for line in lines if is_valid_line(line, seen_document)]

        # Unir las líneas válidas en un único DataFrame
        data = ''.join(valid_lines)
        df = pd.read_csv(StringIO(data), sep='\t', header=None)  # Usar header=None si las tablas no tienen encabezados

        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header
        df.reset_index(drop=True, inplace=True)

        # Procesar el archivo Excel
        df_1 = pd.read_excel(archivo_inicial, sheet_name=nombre_hoja)
        df_1_filter = df_1[df_1['Valorsoc.'] > 0]

        # Determinar las columnas a eliminar
        columnas_d = df.columns
        numero_columnas = len(columnas_d)
        if numero_columnas == 9:
            columnas_a_eliminar = [0, 2, 4, 5, 6, 7, 8]
        else:
            columnas_a_eliminar = [0, 3, 4, 5, 6, 7]

        # Eliminar columnas y añadir índices
        df_3 = df.drop(df.columns[columnas_a_eliminar], axis=1)
        df_3['Doc_Ind'] = df_3.index
        df_3['NumeroDoc'] = range(1, len(df_3) + 1)

        # Realizar la fusión (merge) de los DataFrames
        df_Doc1 = df_3[['NumeroDoc', 'Nº documento']]
        df_Doc2 = df_3[['Doc_Ind', 'Sociedad']]
        df_result = df_Doc1.merge(df_Doc2, left_on='NumeroDoc', right_on='Doc_Ind', how='left')
        df_result.rename(columns={'Result': 'Estado'}, inplace=True)

        # Procesar y limpiar los DataFrames
        df_Ajus1 = df_result[['Nº documento', 'Sociedad']]
        df_Ajus2 = df_Ajus1.copy()
        df_Ajus2.dropna(subset=['Nº documento'], inplace=True)
        df_Ajus3 = df_Ajus2.copy()
        df_Ajus3.reset_index(drop=True, inplace=True)
        df_final = df_Ajus2.copy()
        df_final.rename(columns={'Sociedad': 'Estado'}, inplace=True)

        # Filtrar y fusionar con el archivo Excel
        df_filter_excel = df_1_filter.copy()
        df_B1 = df_filter_excel[['Nºdoc.']]
        df_B2 = df_B1.copy()
        df_final1 = df_final.copy()
        df_B2['Nºdoc.'] = df_B2['Nºdoc.'].astype(str)
        df_final1['Nº documento'] = df_final1['Nº documento'].astype(str)
        df_result_ini1 = df_B2.merge(df_final1, left_on='Nºdoc.', right_on='Nº documento', how='left')
        df_result_ini2 = df_result_ini1[['Nºdoc.', 'Estado']]

        # Contar y validar los resultados
        num_filas = len(df_result_ini2)
        contador = df_result_ini2['Estado'].str.contains('Anulado con documento').sum()
        contador1 = df_result_ini2['Estado'].str.contains('El documento ya ha sido anulado').sum()

        # Guardar el archivo resultante
        df_result_ini2.to_csv(os.path.join(self.output_folder, 'Comparativo_Anulados.txt'), sep='\t', header=True, index=False)

        # Validar el resultado final
        if num_filas == contador + contador1:
            resultado = "True"
        else:
            resultado = "False"

        return resultado

    def arreglo_comparison_file_R3(self) -> str:
        def is_valid_line(line, seen_document):
            """
            Determina si una línea es válida según los criterios especificados:
            - Contiene 10 dígitos seguidos.
            - Contiene las frases específicas: "El documento ya ha sido anulado",
              "Anulado con documento", "Nº documento", "PRESUPUESTO", "Imposible anular:".
            """
            has_10_digits = bool(re.search(r'\d{10}', line))
            contains_phrase = any(phrase in line for phrase in [
                "El documento ya ha sido anulado",
                "Anulado con documento",
                "PRESUPUESTO",
                "Imposible anular:"
            ])
            if "Nº documento" in line:
                if seen_document[0]:
                    return False
                else:
                    seen_document[0] = True
                    return True
            return has_10_digits or contains_phrase

        archivo_inicial = self.input_file1
        archivo_anulado = self.input_file2
        nombre_hoja = 'Base_principal'

        # Leer el archivo de texto
        with open(archivo_anulado, 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()

        # Filtrar solo las líneas válidas
        seen_document = [False]
        valid_lines = [line for line in lines if is_valid_line(line, seen_document)]

        # Unir las líneas válidas en un único DataFrame
        data = ''.join(valid_lines)
        df = pd.read_csv(StringIO(data), sep='\t', header=None)  # Usar header=None si las tablas no tienen encabezados

        new_header = df.iloc[0]
        df = df[1:]
        df.columns = new_header
        df.reset_index(drop=True, inplace=True)

        # Procesar el archivo Excel
        df_1 = pd.read_excel(archivo_inicial, sheet_name=nombre_hoja)
        df_1_filter = df_1[df_1['ImporteenML'] > 0]

        # Determinar las columnas a eliminar
        columnas_d = df.columns
        numero_columnas = len(columnas_d)
        if numero_columnas == 9:
            columnas_a_eliminar = [0, 2, 4, 5, 6, 7, 8]
        else:
            columnas_a_eliminar = [0, 3, 4, 5, 6, 7]

        # Eliminar columnas y añadir índices
        df_3 = df.drop(df.columns[columnas_a_eliminar], axis=1)
        df_3['Doc_Ind'] = df_3.index
        df_3['NumeroDoc'] = range(1, len(df_3) + 1)

        # Realizar la fusión (merge) de los DataFrames
        df_Doc1 = df_3[['NumeroDoc', 'Nº documento']]
        df_Doc2 = df_3[['Doc_Ind', 'Sociedad']]
        df_result = df_Doc1.merge(df_Doc2, left_on='NumeroDoc', right_on='Doc_Ind', how='left')
        df_result.rename(columns={'Result': 'Estado'}, inplace=True)

        # Procesar y limpiar los DataFrames
        df_Ajus1 = df_result[['Nº documento', 'Sociedad']]
        df_Ajus2 = df_Ajus1.copy()
        df_Ajus2.dropna(subset=['Nº documento'], inplace=True)
        df_Ajus3 = df_Ajus2.copy()
        df_Ajus3.reset_index(drop=True, inplace=True)
        df_final = df_Ajus2.copy()
        df_final.rename(columns={'Sociedad': 'Estado'}, inplace=True)

        # Filtrar y fusionar con el archivo Excel
        df_filter_excel = df_1_filter.copy()
        df_B1 = df_filter_excel[['Nºdoc.']]
        df_B2 = df_B1.copy()
        df_final1 = df_final.copy()
        df_B2['Nºdoc.'] = df_B2['Nºdoc.'].astype(str)
        df_final1['Nº documento'] = df_final1['Nº documento'].astype(str)
        df_result_ini1 = df_B2.merge(df_final1, left_on='Nºdoc.', right_on='Nº documento', how='left')
        df_result_ini2 = df_result_ini1[['Nºdoc.', 'Estado']]

        # Contar y validar los resultados
        num_filas = len(df_result_ini2)
        contador = df_result_ini2['Estado'].str.contains('Anulado con documento').sum()
        contador1 = df_result_ini2['Estado'].str.contains('El documento ya ha sido anulado').sum()

        # Guardar el archivo resultante
        df_result_ini2.to_csv(os.path.join(self.output_folder, 'Comparativo_Anulados.txt'), sep='\t', header=True, index=False)

        # Validar el resultado final
        if num_filas == contador + contador1:
            resultado = "True"
        else:
            resultado = "False"

        return resultado
