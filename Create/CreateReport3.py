import pandas as pd
import os


class Reports3:

    def __init__(self, infile1, infile2, outdirectory):
        self.infile1 = infile1
        self.infile2 = infile2
        self.outdirectory = outdirectory

    def stage_User_ValidSAP(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.infile1)
        # Leer archivos CSV
        df2= pd.read_csv(self.infile2 )

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='Número de personal',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Número de personal', 'Área de personal', 'Sociedad_y', 'Area', 'Descripcion de Sociedad'], inplace=True)

        # Crear la columna 'validacion' basada en la columna 'registros'
        merged_df['Valida_UsrSAP'] = merged_df['Posición'].apply(lambda x: 'No_User_SAP' if pd.isna(x) or x == '' else 'User_SAP')

        No_UserSAP = merged_df['Valida_UsrSAP'].value_counts().get('No_User_SAP', 0)
        UserSAP = merged_df['Valida_UsrSAP'].value_counts().get('User_SAP', 0)

        with open(os.path.join(self.outdirectory, "Datos_Iniciales_Proyecto_UsrSAP.txt"), "w") as file:
            file.write("DATOS - NOVEDADES NOMINAS - Usuarios SAP \n\n")
            file.write(f"Usuarios no encontrados SAP: {No_UserSAP}\n")
            file.write(f"Usuarios SAP: {UserSAP}\n")

        # guardar CSV
        merged_df.to_csv(os.path.join(self.outdirectory, "Reporte_General_UserSAP.csv"), index=False)

        return "ok"

    def report_GNR_Pos(self) -> str:

        '''

        Une el archivo
        Reporte_General_UserSAP.csv con 004_Consolidate_END.csv
        Add la posición para evaluar tiene que ser VENTAS o TRADE MARKETING

        '''

        # Leer archivos CSV
        df1 = pd.read_csv(self.infile1)
        # Leer archivos CSV
        df2= pd.read_csv(self.infile2)


        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='Código',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Sociedad_y', 'Infotipo_y', 'Fecha_inicio_y', 'Fecha_fin_y', 'CC-nominas_y', 'Cantidad_y', 'Unidad_y', 'Descripción_y', 'Número de personal', 'Posición_y', 'Sociedad_x_y', 'Variante_y'], inplace=True)

        # Crear la columna 'validacion' basada en la columna 'registros'
        merged_df['Valida_Position'] = merged_df['Evaluar'].apply(lambda x: 'No_Position' if pd.isna(x) or x == 'OPE' else 'Position_ok')

        No_Position = merged_df['Valida_Position'].value_counts().get('No_Position', 0)
        Position_ok = merged_df['Valida_Position'].value_counts().get('Position_ok', 0)

        with open(os.path.join(self.outdirectory, "Datos_Iniciales_Proyecto_Position.txt"), "w") as file:
            file.write("DATOS - NOVEDADES NOMINAS - Posición \n\n")
            file.write(f"Usuarios sin Posición Correcta: {No_Position}\n")
            file.write(f"Usuarios Posición ok: {Position_ok }\n")


        # guardar CSV
        merged_df.to_csv(os.path.join(self.outdirectory, "Report_GNR_pos.csv"), index=False)

        return "ok"

    def report_GNR_montos(self) -> str:

        '''

        Une el archivo
        Report_GNR_pos.csv con Consolidate_FILE_AVG.csv
        Add la posición para evaluar tiene que ser VENTAS o TRADE MARKETING

        '''

        # Leer archivos CSV
        df1 = pd.read_csv(self.infile1)
        # Leer archivos CSV
        df2= pd.read_csv(self.infile2)


        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='Persona',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Persona'], inplace=True)

        # Crear la columna 'validacion' basada en la columna 'registros'
        merged_df['Valida_Montos'] = merged_df['Promedio(3)'].apply(lambda x: 'Sin_Monto' if pd.isna(x) or x == '' else 'Monto')

        Sin_Monto = merged_df['Valida_Montos'].value_counts().get('Sin_Monto', 0)
        Con_Monto = merged_df['Valida_Montos'].value_counts().get('Monto', 0)

        with open(os.path.join(self.outdirectory, "Datos_Iniciales_Proyecto_Montos.txt"), "w") as file:
            file.write("DATOS - NOVEDADES NOMINAS - Procesados SAP - ZHR13 \n\n")
            file.write(f"Usuarios sin Monto: {Sin_Monto}\n")
            file.write(f"Usuarios con Monto: {Con_Monto}\n")


        # guardar CSV
        merged_df.to_csv(os.path.join(self.outdirectory, "Report_GNR_mont.csv"), index=False)

        return "ok"

    def report_GNR_ExisUser(self) -> str:

        '''

        Une el archivo
        Report_GNR_mont.csv con Consolidate_FILE_GNR.csv
        Add la posición para evaluar tiene que ser VENTAS o TRADE MARKETING

        '''

        # Leer archivos CSV
        df1 = pd.read_csv(self.infile1)
        # Leer archivos CSV
        df2= pd.read_csv(self.infile2)


        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='No.Empl.',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['No.Empl.'], inplace=True)

        # Crear la columna 'validacion' basada en la columna 'registros'
        merged_df['Valida_Status'] = merged_df['NOMBRE'].apply(lambda x: 'Sin_time_SAP' if pd.isna(x) or x == '' else 'Cargado')

        No_Carga = merged_df['Valida_Status'].value_counts().get('Sin_time_SAP', 0)
        Carga = merged_df['Valida_Status'].value_counts().get('Cargado', 0)

        with open(os.path.join(self.outdirectory, "Datos_Iniciales_Proyecto_StatusCarga.txt"), "w") as file:
            file.write("DATOS - NOVEDADES NOMINAS - Carga \n\n")
            file.write(f"Usuarios Sin Inf Suficiente: {No_Carga}\n")
            file.write(f"Usuarios Cargados: {Carga}\n")


        # guardar CSV
        merged_df.to_csv(os.path.join(self.outdirectory, "Report_GNR_statusCarga.csv"), index=False)

        return "ok"

    def consolidate_Report_New_User(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.infile1)
        # Leer archivos CSV
        df2= pd.read_csv(self.infile2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='Codigo',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Codigo'], inplace=True)

        # Crear la columna 'validacion' basada en la columna 'registros'
        merged_df['Val_New_Usr'] = merged_df['Estado'].apply(lambda x: 'Procesado' if x == 'Registro creado' else 'No Procesado')

        No_Pro = merged_df['Val_New_Usr'].value_counts().get('No Procesado', 0)
        Pro = merged_df['Val_New_Usr'].value_counts().get('Procesado', 0)

        with open(os.path.join(self.outdirectory, "05_Datos_Proyecto_NewUser_Process" + ".txt"), "w") as file:
            file.write("DATOS - NOVEDADES NOMINAS - NewUser \n\n")
            file.write(f"Usuarios no Procesados: {No_Pro}\n")
            file.write(f"Usuarios Procesados: {Pro}\n")

        # guardar CSV
        merged_df.to_csv(os.path.join(self.outdirectory, "Reporte_General_NewUser_Process" + ".csv"), index=False)

        return "ok"

    def consolidate_Report_Minimun(self) -> str:
        # Leer archivos CSV
        df1 = pd.read_csv(self.infile1)
        # Leer archivos CSV
        df2= pd.read_csv(self.infile2)

        # Merge de archivos basados en columnas comunes
        merged_df = pd.merge(df1, df2,
                             left_on='Código',
                             right_on='Codigo_x',
                             how='left')

        # Eliminar la columna
        merged_df.drop(columns=['Codigo_x', 'Tipo_Carga'], inplace=True)

        # Crear la columna 'validacion' basada en la columna 'registros'
        merged_df['Val_Min'] = merged_df['Ajuste'].apply(lambda x: 'No Procesado' if pd.isna(x) or x == '' else 'Procesado')

        No_Pro = merged_df['Val_New_Usr'].value_counts().get('No Procesado', 0)
        Pro = merged_df['Val_New_Usr'].value_counts().get('Procesado', 0)

        with open(os.path.join(self.outdirectory, "06_Datos_Proyecto_Minimun" + ".txt"), "w") as file:
            file.write("DATOS - NOVEDADES NOMINAS - Minimun \n\n")
            file.write(f"Usuarios no Procesados: {No_Pro}\n")
            file.write(f"Usuarios Procesados: {Pro}\n")

        # guardar CSV
        merged_df.to_csv(os.path.join(self.outdirectory, "Reporte_General_Minimun" + ".csv"), index=False)

        return "ok"
