import pandas as pd
import os
import re


class Reports2:

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def consolidate_AVG(self) -> str:
        # Especifica la ruta de la carpeta - Archivo download
        ruta_carpeta = self.output_dir

        # Lista los archivos en la carpeta
        archivos_en_carpeta = os.listdir(ruta_carpeta)
        archivos_totales = []

        # Ciclo para tomar archivos de carpetas
        for archivo in archivos_en_carpeta:
            variable = archivo
            extension = os.path.splitext(ruta_carpeta + variable)[1].lower()
            if extension in ['.xlsx']:
                # Si cumple con las condiciones, agrega a la lista de archivos válidos
                archivos_totales.append(variable)
            else:
                # Si no cumple con las condiciones, puedes imprimir un mensaje o realizar otras acciones
                var_add1 = 1

        # Filtrar los archivos que se necesitan

        archivos_filtrados = [archivo for archivo in archivos_totales if "ZHER3_AVG" in archivo]
        # Lista para almacenar los DataFrames de cada archivo

        dataframes = []

        # Ciclo para validar los archivos subidos al arreglo
        for archivoReal in archivos_filtrados:
            # Cargar el archivo CSV en un DataFrame
            archivo_ext = os.path.join(ruta_carpeta, archivoReal)

            # Guardar en un Dataframe
            df = pd.read_excel(archivo_ext)

            # Obtener los nombres de las columnas
            columnas = df.columns

            # Crear un diccionario para mapear los nombres de las columnas originales a los nombres sin espacios
            nuevos_nombres = {columna: columna.replace(' ', '') for columna in columnas}

            # Renombrar las columnas utilizando el diccionario
            df = df.rename(columns=nuevos_nombres)

            # Eliminar columnas vacías
            df = df.dropna(axis=1, how='all')

            # Filtrar y eliminar filas con "9999"
            valores_a_excluir = ['9999']
            df = df[~df['Concepto'].isin(valores_a_excluir)]

            # Eliminar columnas
            df = df.drop(columns=df.columns[[0, 1, 2, 4]])

            # Agregar el DataFrame actual a la lista
            dataframes.append(df)

        # Concatenate all DataFrames in the list to create a single DataFrame
        df_consolidado_1 = pd.concat(dataframes, ignore_index=True)

        # Guardar el DataFrame consolidado en un archivo CSV (optional)
        df_consolidado_1.to_csv(os.path.join(self.output_dir, "Consolidate_FILE_AVG.csv"), index=False)

        return "OK"

    def consolidate_GNR(self)-> str:
        # Especifica la ruta de la carpeta - Archivo download
        ruta_carpeta = self.output_dir

        def extract_number(text):
            match = re.search(r'(\d{8})\d', text)
            if match:
                return match.group(1)
            return None

        def remove_leading_zeros(s):
            return ','.join([str(int(num)) for num in s.split(',')])

        # Lista los archivos en la carpeta
        archivos_carpeta = os.listdir(ruta_carpeta)
        archivos_totales = [archivo for archivo in archivos_carpeta if archivo.lower().endswith('.csv')]

        # Filtrar archivos para procesar
        archivos_filtrados = [archivo for archivo in archivos_totales if "Report_ZHER3_GNR" in archivo]

        if not archivos_filtrados:
            raise FileNotFoundError("No hay archivos para procesar.")

        # Lista para almacenar los DataFrames de cada archivo
        dataframes = []

        # Ciclo para validar los archivos subidos al arreglo
        for archivoReal in archivos_filtrados:
            # Cargar el archivo CSV en un DataFrame
            archivo_ext = os.path.join(ruta_carpeta, archivoReal)

            try:
                # Intentar leer el archivo CSV con 7 columnas - "Ya tiene bono en esta fecha"
                df = pd.read_csv(archivo_ext, sep='\t', encoding='ISO-8859-1')

                # Convertir las columnas a cadenas de texto
                df['No.Empl.'] = df['No.Empl.'].astype(str)
                df['NOMBRE'] = df['NOMBRE'].astype(str)

                # Filtrar las filas donde la columna 'A' o la columna 'B' tengan el valor 'ok'
                filtered_df = df[df['No.Empl.'].str.contains('Solo para los') | df['NOMBRE'].str.contains(' ya tiene creado') | df['NOMBRE'].str.contains('Número')]

                new_df = filtered_df[['No.Empl.', 'NOMBRE']]

            except pd.errors.ParserError:
                # Si hay un error de análisis, leer el archivo - Se aplicó Bono
                df = pd.read_csv(archivo_ext, sep='\t', encoding='ISO-8859-1', usecols=range(8))

                # Convertir las columnas a cadenas de texto
                df['No.Empl.'] = df['No.Empl.'].astype(str)
                df['NOMBRE'] = df['NOMBRE'].astype(str)

                # Eliminar la novena columna si existe
                # df = df.drop(df.columns[4], axis=1)

                # Verificar si alguna fila en la columna 'NOMBRE' está vacía
                filtered_df = df[df['No.Empl.'].str.contains('Solo para los') | df['NOMBRE'].str.contains(' ya tiene creado') | df['NOMBRE'].str.contains('Número')]

                # Convertir la columna 'Unnamed: 4' a cadenas de texto usando .loc
                filtered_df = filtered_df.copy()
                filtered_df['Unnamed: 4'] = filtered_df['Unnamed: 4'].astype(str)

                for index, row in filtered_df.iterrows():
                    extracted_number = extract_number(row['Unnamed: 4'])
                    if extracted_number:
                        filtered_df.at[index, 'No.Empl.'] = extracted_number
                        filtered_df.at[index, 'NOMBRE'] = 'modified'
                        # print(extracted_number)
                new_df = filtered_df[['No.Empl.', 'NOMBRE']]

            # Agregar el DataFrame actual a la lista
            dataframes.append(new_df)

        # Concatenate all DataFrames in the list to create a single DataFrame
        df_consolidado_1 = pd.concat(dataframes, ignore_index=True)

        # Aplicar la función a la columna
        df_consolidado_1['No.Empl.'] = df_consolidado_1['No.Empl.'].apply(remove_leading_zeros)

        # Convertir la columna a string
        df_consolidado_1['No.Empl.'] = df_consolidado_1['No.Empl.'].astype(str)

        # Guardar el DataFrame consolidado en un archivo CSV (optional)
        df_consolidado_1.to_csv(os.path.join(self.output_dir, "Consolidate_FILE_GNR.csv"), index=False)

        return "ok"

    def validar_fechas_excel(self)-> str:
        try:
            df = pd.read_excel(self.output_dir, engine='openpyxl')

            columnas = df.columns
            tiene_inicio = 'Fecha_inicio' in columnas
            tiene_fin = 'Fecha_fin' in columnas

            # Validar si alguna celda en las columnas está vacía
            if tiene_inicio and df['Fecha_inicio'].isnull().any():
                return 'empty'
            if tiene_fin and df['Fecha_fin'].isnull().any():
                return 'empty'

            if tiene_inicio or tiene_fin:
                return 'ok'
            return 'Columns not found'
        except Exception as e:
            return f"Error: {e}"
