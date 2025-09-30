import pandas as pd
import os


class File:
    def __init__(self, many_file) -> None:
        self.many_file = many_file

    '''Validation title file attachment'''
    def validate_title_infotipo(self)->bool:
        # Asignar Variables a Archivos
        many_file = self.many_file
        try:
            # Verificar si el archivo existe
            if not os.path.exists(many_file):
                print(f"Error: El archivo {many_file} no existe.")
                return False

            # Título Infotipo
            titulo_infotipo = ['infotipo']

            # Leer el archivo Excel
            try:
                df = pd.read_excel(many_file)
            except Exception as e:
                print(f"Error al leer el archivo Excel: {e}")
                return False

            # Obtener los títulos actuales y normalizarlos
            titulos_actuales = [str(col).lower().strip() for col in df.columns]

            # Verificar si todos los títulos esperados están presentes
            titulos_faltantes = [titulo for titulo in titulo_infotipo if titulo not in titulos_actuales]

            if titulos_faltantes:
                print(f"Títulos faltantes: {titulos_faltantes}")
                return False

            print("Validación de títulos exitosa.")
            return True

        except Exception as error:
            print(f"Error inesperado durante la validación: {error}")
            return False

    def validate_title_ccnominas(self)->bool:
        # Asignar Variables a Archivos
        many_file = self.many_file
        try:
            # Verificar si el archivo existe
            if not os.path.exists(many_file):
                print(f"Error: El archivo {many_file} no existe.")
                return False

            # Títulos a verificar
            titulos_a_verificar = ['cc-nominas', 'clase_ausentismo']

            # Leer el archivo Excel
            try:
                df = pd.read_excel(many_file)
            except Exception as e:
                print(f"Error al leer el archivo Excel: {e}")
                return False

            # Obtener los títulos actuales y normalizarlos
            titulos_actuales = [str(col).lower().strip() for col in df.columns]

            # Verificar si alguno de los títulos esperados está presente
            if any(titulo in titulos_actuales for titulo in titulos_a_verificar):
                print("Validación de títulos exitosa.")
                return True
            else:
                print(f"Títulos faltantes: {titulos_a_verificar}")
                return False

        except Exception as error:
            print(f"Error inesperado durante la validación: {error}")
            return False
