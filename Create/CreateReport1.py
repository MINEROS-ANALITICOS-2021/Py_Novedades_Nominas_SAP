import pandas as pd
import os
import csv
import random

class Reports1:

    def __init__(self, input_path, output_dir, case):
        self.input_path = input_path
        self.output_dir = output_dir
        self.case = case

    def create_file_report(self) -> str:
        """
        Procesa un archivo de validación y crea un reporte CSV con los registros y errores.

        Returns:
            str: Mensaje de éxito o error
        """
        try:
            # Inicialización
            extracted_data = []

            with open(self.input_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    try:
                        line = line.strip()

                        # Procesar líneas con "Record"
                        if "Record" in line:
                            parts = line.split()
                            extracted_data.append({
                                "Type": "Record",
                                "Code": parts[1],
                                "Document": parts[2],
                                "Status": parts[3]
                            })

                        # Procesar líneas con "ERROR"
                        elif "ERROR" in line:
                            parts = line.split()
                            extracted_data.append({
                                "Type": "ERROR",
                                "Code": parts[1],
                                "Document": "",
                                "Status": ""
                            })

                    except IndexError as e:
                        print(f"Error procesando la línea {line_number}: {line} ({e})")

            # Escribir datos al CSV
            with open(self.output_dir, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ["Type", "Code", "Document", "Status"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(extracted_data)

            print(f"Archivo procesado exitosamente. Datos guardados en {self.output_dir}")

        except Exception as e:
            print(f"Error general: {e}")

    def validate_user_duplica(self) -> str:
        try:
            # Función para generar un código aleatorio de 3 cifras
            def generate_random_code():
                return str(random.randint(100, 999))

            # Leer archivo original
            dt_fileInicial = pd.read_excel(self.input_path)

            # Crea id para cada registro
            dt_fileInicial['id_Users'] = dt_fileInicial['Código'].astype(str) + "_" + dt_fileInicial['Cantidad'].astype(str) + "_" + dt_fileInicial['Descripción'] + "_" + dt_fileInicial.apply(lambda row: generate_random_code(), axis=1)

            # Crea id para cada registro
            dt_fileInicial['UsersConc'] = dt_fileInicial['Código'].astype(str) + "_" + dt_fileInicial['Cantidad'].astype(str) + "_" + dt_fileInicial['Descripción']

            # Add columna marcando Duplicados Que no se van a procesar
            dt_fileInicial['Users_Process'] = dt_fileInicial.duplicated(subset='UsersConc').map({True: 'Duplicado: Solo se Procesa 1', False: 'Correcto'})
            # Add columna marcando Duplicados todos
            dt_fileInicial['Valida_Duplicados'] = dt_fileInicial.duplicated(subset='UsersConc', keep=False).map({True: 'Duplicado: Solo se Procesa 1', False: 'Correcto'})
            # df sin Duplicados
            # df_sin_duplicados = dt_fileInicial[dt_fileInicial['Users_Process'] == 'Correcto']

            # Hacer copia del Original con todos los datos
            # dt_baseReport = dt_fileInicial[['Código', 'Sociedad', 'Cantidad', 'Descripción', 'Valida_Duplicados']].copy()

            cantidad_Total = len(dt_fileInicial)
            Duplicados = dt_fileInicial['Valida_Duplicados'].value_counts().get('Duplicado: Solo se Procesa 1', 0)
            Correctos = dt_fileInicial['Valida_Duplicados'].value_counts().get('Correcto', 0)

            Datos_Iniciales = {'Total Registros': cantidad_Total, 'Registros Duplicados': Duplicados, 'Registros Correctos': Correctos}

            with open(os.path.join(self.output_dir, "Datos_Iniciales_Proyecto_" + self.case + ".txt"), "w") as file:
                file.write("DATOS INICIALES - NOVEDADES NOMINAS - Duplicados \n\n")
                file.write(f"Total Registros: {cantidad_Total}\n")
                file.write(f"Registros Duplicados: {Duplicados}\n")
                file.write(f"Registros Unicos: {Correctos}\n")

            # Guardar el DataFrame consolidado en un archivo CSV Validación Duplicados
            dt_fileInicial.to_csv(os.path.join(self.output_dir, "Reporte_General_Duplicados_" + self.case + ".csv"), index=False)

            return "ok"

        except Exception as e:
            return f"Error: {e}"

    def consolidate_Final(self) -> str:
        # Leer archivos CSV
        df = pd.read_csv(self.input_path)

        # Crear la columna 'Status End' inicialmente vacía
        df['Status End'] = ''

        # Función para evaluar las condiciones y actualizar la columna 'Status End'
        def evaluar_status_end(df):
            # Primera condición
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                        row['Valida_Duplicados'] != 'Correcto' else row['Status End'], axis=1)

            # Segunda condición
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                        row['Valida_Position'] != 'Position_ok' else row['Status End'], axis=1)

            # Tercera condición
            df['Status End'] = df.apply(lambda row: 'Procesado' if row['Status End'] == '' and
                                        row['Valida_Duplicados'] == 'Correcto' and
                                        row['Valida_Position'] == 'Position_ok' and
                                        row['NOMBRE'] == 'modified' and
                                        row['Valida_Status'] == 'Cargado' and
                                        row['Status_Mini'] != 'Ajustar'else row['Status End'], axis=1)

            # four condición Usuarios Nuevos
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                        row['Valida_Duplicados'] == 'Correcto' and
                                        row['Valida_Position'] == 'Position_ok' and
                                        row['NOMBRE'] != 'modified' and
                                        row['Valida_Status'] != 'Cargado' and
                                        row['Estado'] != 'Registro creado' else row['Status End'], axis=1)

            # Five condición Usuarios Cambio mínimo
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                        row['Valida_Duplicados'] == 'Correcto' and
                                        row['Valida_Position'] == 'Position_ok' and
                                        row['NOMBRE'] != 'modified' and
                                        row['Val_New_Usr'] == 'No Procesado' and
                                        row['Val_Min'] == 'No Procesado' else row['Status End'], axis=1)

            # Six condición Usuarios Nuevos
            df['Status End'] = df.apply(lambda row: 'Procesado' if row['Status End'] == '' and
                                        row['Estado'] == 'Registro creado' else row['Status End'], axis=1)

            # Seven condición Usuarios Cambio mínimo
            df['Status End'] = df.apply(lambda row: 'Procesado' if row['Status End'] == '' and
                                        row['Val_Min'] == 'Procesado' else row['Status End'], axis=1)

            return df

        # Aplicar la función al DataFrame
        df = evaluar_status_end(df)

        df_final = df[['Código', 'Cantidad_x', 'Descripción_x', 'Valida_Duplicados', 'Posición_x', 'Sociedad_x_x', 'Valida_Position', 'Valida_Montos', 'NOMBRE', 'Estado', 'Val_New_Usr','Status End']]
        # guardar CSV
        df_final.to_csv(os.path.join(self.output_dir, "Reporte_General_Final" + self.case +".csv"), index=False)

        return "ok"

    def consolidate_Final_Simple(self) -> str:
        # Leer archivos CSV
        df = pd.read_csv(self.input_path)

        # Crear la columna 'Status End' inicialmente vacía
        df['Status End'] = ''

        # Función para evaluar las condiciones y actualizar la columna 'Status End'
        def evaluar_status_end(df1):
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                    row['Users_Process'] != 'Correcto' else row['Status End'], axis=1)

            # Segunda condición
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                    row['Valida_Position'] != 'Position_ok' else row['Status End'], axis=1)

            # Tercera condición
            df['Status End'] = df.apply(lambda row: 'Procesado' if row['Status End'] == '' and
                                        row['Users_Process'] == 'Correcto' and
                                        row['Valida_Position'] == 'Position_ok' and
                                        row['NOMBRE'] == 'modified' and
                                        row['Valida_Status'] == 'Cargado' and
                                        row['Status_Mini'] != 'Ajustar'else row['Status End'], axis=1)

            #  Cuarta condición
            df['Status End'] = df.apply(lambda row: 'No Procesado' if row['Status End'] == '' and
                                        row['Valida_Duplicados'] == 'Correcto' and
                                        row['Valida_Position'] == 'Position_ok' and
                                        row['NOMBRE'] != 'modified' and
                                        row['Valida_Status'] == 'Cargado' and
                                        row['Status_Mini'] != 'Ajustar'else row['Status End'], axis=1)


            return df

        # Aplicar la función al DataFrame
        df = evaluar_status_end(df)

        df_final = df[['Código', 'Cantidad_x', 'Descripción_x', 'Valida_Duplicados', 'Posición_x', 'Sociedad_x_x', 'Valida_Position', 'Valida_Montos', 'NOMBRE', 'Status End']]
        # guardar CSV
        df_final.to_csv(os.path.join(self.output_dir, "Reporte_General_Final" + self.case + ".csv"), index=False)

        return "ok"
