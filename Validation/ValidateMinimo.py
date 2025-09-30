import pandas as pd
import os

class Minimos:
    def __init__(self, file_total, out_directory, minAVM, minOTR) -> None:
        self.file_total = file_total
        self.out_directory = out_directory
        self.minAVM = float(minAVM)
        self.minOTR = float(minOTR)
    '''Validation minimos'''

    def validate_minimos(self) -> str:

        """
        Procesa el archivo CSV de entrada para calcular la columna 'Pago_Mini' según el valor en 'Val_Posicion'.
        Calcula 'Pago_Mini' multiplicando la columna 'Cantidad' por var_3 si 'Val_Posicion' es "AVM" o por var_4 en
        otro caso. No se filtran las filas en función de la comparación con 'Promedio(3)', es decir, se conservan
        todas las filas. Guarda archivos CSV para cada subconjunto y uno consolidado.

        Parámetros:
          - var_1: Ruta del archivo CSV de entrada.
          - var_2: Carpeta de salida para guardar los archivos.
          - var_3: Factor de multiplicación para cuando 'Val_Posicion' es "AVM".
          - var_4: Factor de multiplicación para cuando 'Val_Posicion' no es "AVM".

        Retorna:
          - "ok" si todo sale bien.
        """
        try:
            df = pd.read_csv(self.file_total, encoding='utf-8')
        except Exception as e:
            return f"Error al leer el archivo: {e}"

        try:
            # Convertir columnas a tipos numéricos
            df['Promedio(3)'] = pd.to_numeric(df['Promedio(3)'], errors='coerce')
            df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').astype('Int64')
        except Exception as e:
            return f"Error al convertir columnas: {e}"

        # Separar registros según el valor de 'Val_Posicion'
        df_AVM = df[df['Val_Posicion'].str.upper() == "AVM"].copy()
        df_OTROS = df[df['Val_Posicion'].str.upper() != "AVM"].copy()

        # Para AVM: calcular 'Pago_Mini' usando el factor var_3
        if not df_AVM.empty:
            df_AVM['Pago_Mini'] = (df_AVM['Cantidad'] * self.minAVM).round(2)
            df_AVM.loc[df_AVM['Promedio(3)'] < df_AVM['Pago_Mini'], 'Status_Mini'] = "Ajustar"
            df_AVM_filtrado = df_AVM[df_AVM['Promedio(3)'] < df_AVM['Pago_Mini']]
            if not df_AVM_filtrado.empty:
                out_path_avm = os.path.join(self.out_directory, "Users_minimo_AVM.csv")
                df_AVM_filtrado.to_csv(out_path_avm, index=False)

        else:
            print("No se encontraron registros para AVM.")

        # Para los demás: calcular 'Pago_Mini' usando el factor var_4
        if not df_OTROS.empty:
            df_OTROS['Pago_Mini'] = (df_OTROS['Cantidad'] * self.minOTR).round(2)
            df_OTROS_filtrado = df_OTROS[df_OTROS['Promedio(3)'] < df_OTROS['Pago_Mini']]
            if not df_OTROS_filtrado.empty:
                out_path_otros = os.path.join(self.out_directory, "Users_minimo_OTROS.csv")
                df_OTROS_filtrado.to_csv(out_path_otros, index=False)

        else:
            print("No se encontraron registros para otros.")

        # Consolidar ambos subconjuntos sin filtrar por 'Promedio(3)'
        df_consolidado = pd.concat([df_AVM, df_OTROS], ignore_index=True)
        out_path_consolidado = os.path.join(self.out_directory, "Consolidado_Calculado_minimos.csv")
        df_consolidado.to_csv(out_path_consolidado, index=False)

        return "ok"

    def validate_minimos_report_gnr(self) -> str:
        """
        Procesa el archivo CSV de entrada para calcular la columna 'Pago_Mini' según el valor en 'Val_Posicion'.
        Calcula 'Pago_Mini' multiplicando la columna 'Cantidad' por var_3 si 'Val_Posicion' es "AVM" o por var_4 en
        otro caso. No se filtran las filas en función de la comparación con 'Promedio(3)', es decir, se conservan
        todas las filas. Guarda archivos CSV para cada subconjunto y uno consolidado.

        Parámetros:
          - var_1: Ruta del archivo CSV de entrada.
          - var_2: Carpeta de salida para guardar los archivos.
          - var_3: Factor de multiplicación para cuando 'Val_Posicion' es "AVM".
          - var_4: Factor de multiplicación para cuando 'Val_Posicion' no es "AVM".

        Retorna:
          - "ok" si todo sale bien.
        """
        try:
            df = pd.read_csv(self.file_total, encoding='utf-8')
        except Exception as e:
            return f"Error al leer el archivo: {e}"

        try:
            # Convertir columnas a tipos numéricos
            df['Promedio(3)'] = pd.to_numeric(df['Promedio(3)'], errors='coerce')
            df['Cantidad_x'] = pd.to_numeric(df['Cantidad_x'], errors='coerce').astype('Int64')
        except Exception as e:
            return f"Error al convertir columnas: {e}"

        df['Promedio(3)'] = df['Promedio(3)'].fillna(0)

        # Separar registros según el valor de 'Val_Posicion'
        df_AVM = df[df['Evaluar'].str.upper() == "AVM"].copy()
        df_OTROS = df[df['Evaluar'].str.upper() != "AVM"].copy()

        # Para AVM: calcular 'Pago_Mini' usando el factor self.minAVM
        if not df_AVM.empty:
            df_AVM['Pago_Mini'] = (df_AVM['Cantidad_x'] * self.minAVM).round(2)
            df_AVM.loc[(df_AVM['Promedio(3)'] < df_AVM['Pago_Mini']) & (df_AVM['Valida_Position'].reindex(df_AVM.index) == 'Position_ok'), 'Status_Mini'] = "Ajustar"
            df_AVM_filtrado = df_AVM[df_AVM['Promedio(3)'] < df_AVM['Pago_Mini']]
            if not df_AVM_filtrado.empty:
                out_path_avm = os.path.join(self.out_directory, "Users_minimo_AVM.csv")
                df_AVM_filtrado.to_csv(out_path_avm, index=False)
        else:
            print("No se encontraron registros para AVM.")

        # Para los demás: calcular 'Pago_Mini' usando el factor self.minOTR
        if not df_OTROS.empty:
            df_OTROS['Pago_Mini'] = (df_OTROS['Cantidad_x'] * self.minOTR).round(2)
            df_OTROS.loc[(df_OTROS['Promedio(3)'] < df_OTROS['Pago_Mini']) & (df_OTROS['Valida_Position'].reindex(df_OTROS.index) == 'Position_ok'), 'Status_Mini'] = "Ajustar"
            df_OTROS_filtrado = df_OTROS[df_OTROS['Promedio(3)'] < df_OTROS['Pago_Mini']]
            if not df_OTROS_filtrado.empty:
                out_path_otros = os.path.join(self.out_directory, "Users_minimo_OTROS.csv")
                df_OTROS_filtrado.to_csv(out_path_otros, index=False)
        else:
            print("No se encontraron registros para otros.")

        # Consolidar ambos subconjuntos sin filtrar por 'Promedio(3)'
        df_consolidado = pd.concat([df_AVM, df_OTROS], ignore_index=True)
        out_path_consolidado = os.path.join(self.out_directory, "Consolidado_Calculado_minimos.csv")
        df_consolidado.to_csv(out_path_consolidado, index=False)

        return "ok"
