import pandas as pd
import os
import re
from datetime import datetime

class Normalizar:

    def __init__(self, filequery1, pathdirectory):
        self.filequery1 = filequery1
        self.pathdirectory = pathdirectory


    def normalize_query_ZHR26(self) -> str:

        # Leer el archivo de texto
        with open(self.filequery1, 'r', encoding='latin-1') as archivo:
            lineas = archivo.readlines()

        # Encontrar la línea con "No. Empleado"
        for i, linea in enumerate(lineas):
            if "No. Empleado" in linea:
                # Dividir la línea de encabezados
                encabezados1 = linea.strip().split('\t')
                datos_inicio1 = i + 1
                break

        # Leer los datos saltando los encabezados
        datos = []
        for linea in lineas[datos_inicio1:]:
            # Ignorar líneas con '*' o completamente vacías
            if '*' in linea or not linea.strip():
                continue

            # Dividir la línea en partes
            partes = linea.strip().split('\t')

            # Asegurar que solo se tomen los datos relevantes
            if len(partes) >= len(encabezados1):
                datos.append(partes[:len(encabezados1)])

        # Crear DataFrame
        df = pd.DataFrame(datos, columns=encabezados1)

        # Eliminar columnas completamente vacías
        df = df.dropna(axis=1, how='all')

        # guardar CSV
        df.to_csv(os.path.join(self.pathdirectory, "001_Report_Norma_ZHR26.csv"), index=False)

        return "ok"

    def normalize_query__FLEXI(self) -> str:

        # Leer el archivo de texto
        with open(self.filequery1, 'r', encoding='latin-1') as archivo:
            lineas = archivo.readlines()

        # Encontrar la línea con "No. Empleado"
        for i, linea in enumerate(lineas):
            if "Número de personal" in linea:
                # Dividir la línea de encabezados
                encabezados2 = [col.strip() for col in linea.strip().split('\t')][:12]
                # encabezados = linea.strip().split('\t')
                datos_inicio2 = i + 1
                break
        datos_inicio2 = datos_inicio2 +1
        # Leer los datos saltando los encabezados
        datos = []
        for linea in lineas[datos_inicio2:]:
            # Limpiar y dividir la línea
            partes = [parte.strip() for parte in linea.strip().split('\t')]

            # Filtrar líneas con datos relevantes
            if partes and '*' not in partes and len(partes) >= len(encabezados2):
                datos.append(partes[:len(encabezados2)])

        # Crear DataFrame
        df = pd.DataFrame(datos, columns=encabezados2)

        # Eliminar columnas completamente vacías
        df = df.dropna(axis=1, how='all')

        # guardar CSV
        df.to_csv(os.path.join(self.pathdirectory, "001_Report_Norma_FLEXI.csv"), index=False)

        return "ok"

    def adapt_dates(self) -> str:
        def transformar_fecha(fecha: str) -> str:
            fecha_str = str(fecha).strip()
            if re.fullmatch(r"\d{8}", fecha_str):
                return fecha_str
            else:
                formatos = ["%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"]
                for fmt in formatos:
                    try:
                        fecha_dt = datetime.strptime(fecha_str, fmt)
                        fecha_transformada = fecha_dt.strftime("%Y%m%d")
                        if len(fecha_transformada) == 7:
                            fecha_transformada = fecha_transformada[:6] + '0' + fecha_transformada[6:]
                        return fecha_transformada
                    except ValueError:
                        continue
            return "Formato inválido"

        def validar_columnas(dt: pd.DataFrame) -> bool:
            dt['Fecha_inicio'] = dt['Fecha_inicio'].astype(str)
            dt['Fecha_fin'] = dt['Fecha_fin'].astype(str)
            if dt['Fecha_inicio'].str.contains(r'[\\/.-]').any() or dt['Fecha_fin'].str.contains(r'[\\/.-]').any():
                return False
            return True

        try:
            df = pd.read_excel(self.filequery1)
            formato = validar_columnas(df)
            print(formato)
            if formato:
                try:
                    if 'Fecha_inicio' not in df.columns or 'Fecha_fin' not in df.columns:
                        raise KeyError("Las columnas 'Fecha_inicio' y/o 'Fecha_final' no existen en el DataFrame.")
                    df['Fecha_inicio_new'] = df['Fecha_inicio'].apply(lambda x: transformar_fecha(str(x).strip()))
                    df['Fecha_fin_new'] = df['Fecha_fin'].apply(lambda x: transformar_fecha(str(x).strip()))
                except Exception as e:
                    return f"Error al procesar las fechas1: {e}"
            else:
                try:
                    df['Fecha_inicio'] = pd.to_datetime(df['Fecha_inicio'], dayfirst=True).dt.date
                    df['Fecha_fin'] = pd.to_datetime(df['Fecha_fin'], dayfirst=True).dt.date
                    if 'Fecha_inicio' not in df.columns or 'Fecha_fin' not in df.columns:
                        raise KeyError("Las columnas 'Fecha_inicio' y/o 'Fecha_final' no existen en el DataFrame.")
                    df['Fecha_inicio_new'] = df['Fecha_inicio'].apply(lambda x: transformar_fecha(str(x).strip()))
                    df['Fecha_fin_new'] = df['Fecha_fin'].apply(lambda x: transformar_fecha(str(x).strip()))
                except Exception as e:
                    return f"Error al procesar las fechas2: {e}"
        except Exception as e:
            return f"Error al leer el archivo: {e}"

        if 'Descripción' in df.columns:
            df['Descripción'] = df['Descripción'].fillna('SinDato')

        df.to_csv(os.path.join(self.pathdirectory, "00_Nueva_plantillaFechas.csv"), index=False)
        return "ok"

    def validate_duplica_Infotipos(self) -> str:

        # Leer archivo original
        dt_fileInicial = pd.read_csv(self.filequery1)

        # Add columna marcando Duplicados todos
        dt_fileInicial['Valida_Duplicados'] = dt_fileInicial.duplicated(subset='Código', keep=False).map({True: 'Duplicado', False: 'Correcto'})

        df_Duplicados = dt_fileInicial.copy()
        df_Optimus = dt_fileInicial.copy()

        df_Duplicados = dt_fileInicial[dt_fileInicial['Valida_Duplicados'] == 'Duplicado']

        df_Optimus = dt_fileInicial[dt_fileInicial['Valida_Duplicados'] == 'Correcto']

        # Guardar el DataFrame consolidado en un archivo CSV Validación Duplicados
        df_Duplicados.to_csv(os.path.join(self.pathdirectory, "Reporte_Duplicados.csv"), index=False)
        df_Optimus.to_csv(os.path.join(self.pathdirectory, "Reporte_Load.csv"), index=False)

        return "ok"

    def validate_duplica_2001(self) -> str:
        try:
            # Leer archivo original
            dt_fileInicial = pd.read_csv(self.filequery1)

            # Marcar duplicados según las 4 columnas
            dt_fileInicial['Valida_Duplicados'] = dt_fileInicial.duplicated(
                subset=['Código', 'Clase_Ausentismo', 'Fecha_inicio', 'Fecha_fin'],
                keep=False
            ).map({True: 'Duplicado', False: 'Correcto'})

            # Filtrar duplicados y correctos
            df_Duplicados = dt_fileInicial[dt_fileInicial['Valida_Duplicados'] == 'Duplicado']
            df_Optimus = dt_fileInicial[dt_fileInicial['Valida_Duplicados'] == 'Correcto']

            # Guardar solo si hay datos
            if not df_Duplicados.empty:
                df_Duplicados.to_csv(os.path.join(self.pathdirectory, "Reporte_Duplicados.csv"), index=False)

            if not df_Optimus.empty:
                df_Optimus.to_csv(os.path.join(self.pathdirectory, "Reporte_Load.csv"), index=False)

            return "ok"

        except Exception as e:
            return f"Error: {e}"
