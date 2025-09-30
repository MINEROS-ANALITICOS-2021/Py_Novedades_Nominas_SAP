import pandas as pd
import os


class Head:
    def __init__(self, many_file, arr_titles_for) -> None:
        self.many_file = many_file
        self.arr_titles_for = arr_titles_for

    '''Validation title the file format'''
    def validate_title_format(self)->bool:
        # Asignar Variables a Archivos
        many_file = self.many_file
        arr_titles_for = self.arr_titles_for
        try:
            # Verificar si el archivo existe
            if not os.path.exists(many_file):
                print(f"Error: El archivo {many_file} no existe.")
                return False

            # Titles the format file
            titulos = [elemento.strip("'") for elemento in arr_titles_for.split(",")]

            # Leer el archivo Excel
            try:
                df = pd.read_excel(many_file)
            except Exception as e:
                print(f"Error al leer el archivo Excel: {e}")
                return False

            # Obtener los títulos actuales y normalizarlos
            titulos_actuales = [str(col).lower().strip() for col in df.columns]

            # Verificar si todos los títulos esperados están presentes
            titulos_faltantes = [titulo for titulo in titulos if titulo not in titulos_actuales]

            if titulos_faltantes:
                print(f"Títulos faltantes: {titulos_faltantes}")
                return False

            print("Validación de títulos exitosa.")
            return True

        except Exception as error:
            print(f"Error inesperado durante la validación: {error}")
            return False
