from calendar import monthrange
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Calendar2:

    def __init__(self, year_cus):
        self.year_cus = year_cus

    def obtener_fechas_trimestre_cust(self) -> dict:
        """
        Calcula fechas relevantes para reportes trimestrales incluyendo:
        - Fecha actual
        - Primera y segunda quincena del mes actual
        - Primer y último día del mes hace 3 meses
        - Primer y último día del mes anterior

        Returns:
            dict: Diccionario con fechas formateadas como dd.mm.yyyy
        """
        # Fecha actual y mes actual
        fecha_base = datetime.now()
        year_actual = self.year_cus if self.year_cus is not None else fecha_base.year

        fecha_actual = fecha_base.replace(year=year_actual)
        dia_actual = fecha_actual.day
        mes_actual = fecha_actual.month

        # Calcular fechas hace 3 meses y 1 mes
        fecha_3_meses = fecha_actual - relativedelta(months=3)
        fecha_1_mes = fecha_actual - relativedelta(months=1)

        # Obtener último día de cada mes
        _, ultimo_dia_3m = monthrange(fecha_3_meses.year, fecha_3_meses.month)
        _, ultimo_dia_1m = monthrange(fecha_1_mes.year, fecha_1_mes.month)
        _, ultimo_dia_actual = monthrange(year_actual, mes_actual)

        # Crear objetos date para los rangos
        fecha_inicio_actual = date(year_actual, mes_actual, 1)
        fecha_fin_actual = date(year_actual, mes_actual, ultimo_dia_actual)
        fecha_inicio_3m = date(fecha_3_meses.year, fecha_3_meses.month, 1)
        fecha_fin_3m = date(fecha_3_meses.year, fecha_3_meses.month, ultimo_dia_3m)
        fecha_inicio_1m = date(fecha_1_mes.year, fecha_1_mes.month, 1)
        fecha_fin_1m = date(fecha_1_mes.year, fecha_1_mes.month, ultimo_dia_1m)

        return {
            "fecha_actual": fecha_actual.strftime("%d.%m.%Y"),
            "primera_quincena": f"10.{mes_actual:02d}.{year_actual}",
            "segunda_quincena": f"20.{mes_actual:02d}.{year_actual}",
            "dia_quince": f"15.{mes_actual:02d}.{year_actual}",
            "inicio_tres_meses": fecha_inicio_3m.strftime("%d.%m.%Y"),
            "fin_tres_meses": fecha_fin_3m.strftime("%d.%m.%Y"),
            "inicio_mes_anterior": fecha_inicio_1m.strftime("%d.%m.%Y"),
            "fin_mes_anterior": fecha_fin_1m.strftime("%d.%m.%Y"),
            "inicio_mes_actual": fecha_inicio_actual.strftime("%d.%m.%Y"),
            "fin_mes_actual": fecha_fin_actual.strftime("%d.%m.%Y"),
            "mes_actual": f"{mes_actual:02d}",
            "year_actual": f"{year_actual}",
            "dia_actual": f"{dia_actual}",
        }
