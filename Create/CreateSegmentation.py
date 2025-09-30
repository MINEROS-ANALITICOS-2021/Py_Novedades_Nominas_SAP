import pandas as pd
import os

class Segmentation:

    def __init__(self, filequery1, pathdirectory, pathUpload):
        self.filequery1 = filequery1
        self.pathdirectory = pathdirectory
        self.pathUpload = pathUpload

    def create_file_load(self) -> str:

        # Cargar archivo df
        df = pd.read_csv(self.filequery1)

        # Function to format quantity
        def format_quantity(x):
            return f"0{x}" if x < 10 else str(x)

        # Process each column
        df['formatted_quantity'] = df['Cantidad'].apply(format_quantity)
        df['variante_code'] = df['Variante'].apply(lambda x: '1' if x == 'DIA DOBLE G2' else '2')
        df['position_code'] = df['Val_Posicion'].apply(lambda x: '2' if x == 'CTM' else '1')
        # Crear un identificador único para cada valor en "Descripción"
        df['description_id'] = df['Descripcion'].factorize()[0] + 1
        df['formatted_Descrip'] = df['description_id'].apply(format_quantity)
        # df['description_id'] = df['description_id'].astype(str)

        # Create group_valid column
        df['group_valid'] = df['formatted_quantity'] + df['variante_code'] + df['position_code'] + df['formatted_Descrip']

        # Save to new CSV
        df.to_csv(os.path.join(self.pathdirectory, "006_Segmentacion_Consolidado.csv"), index=False)

        for group in df['group_valid'].unique():
            group_df = df[df['group_valid'] == group]
            group_df.to_excel(os.path.join(self.pathUpload, f'{group}_group.xlsx'), index=False)

        return "ok"
