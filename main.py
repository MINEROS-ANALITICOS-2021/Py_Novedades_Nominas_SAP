import sys
import json

from Validation.FileAdj import File
from Validation.FileHead import Head
from Create.CreateFormat import InfotiposProcessor
from Create.CreateReport1 import Reports1
from Create.CreateReport2 import Reports2
from Create.CreateReport3 import Reports3
from Create.CreateReport4 import Reports4
from Validation.CalendarGnr import Calendar1
from Validation.CalendarCus import Calendar2
from Validation.ValidateMinimo import Minimos
from Create.CreateNormalize import Normalizar
from Create.CreateConsolidate import Consolidate
from Create.CreateSegmentation import Segmentation

def shellHandler() -> None:
    """Interface for command shell class and scripts"""
    try:
        func_name = sys.argv[1]
        if func_name.strip() == "val_title_info":
            many_file = sys.argv[2]

            file = File(many_file)
            result = file.validate_title_infotipo()
            print(json.dumps(result))

        elif func_name.strip() == "val_title_form":
            many_file = sys.argv[2]
            arr_titles_for = sys.argv[3]

            head = Head(many_file, arr_titles_for)
            result = head.validate_title_format()
            print(json.dumps(result))

        elif func_name.strip() == "val_title_ccnomina":
            many_file = sys.argv[2]

            file = File(many_file)
            result = file.validate_title_ccnominas()
            print(json.dumps(result))

        elif func_name.strip() == "cre_form_inf":
            input_file = sys.argv[2]
            expected_columns = sys.argv[3]
            infotipo = sys.argv[4]
            case = sys.argv[5]
            output_directory = sys.argv[6]

            infotiposProcessor = InfotiposProcessor(input_file, expected_columns, infotipo, case, output_directory)
            result = infotiposProcessor.process_infotipos()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_1":
            input_path = sys.argv[2]
            output_dir = sys.argv[3]
            case = sys.argv[4]

            reports1= Reports1(input_path, output_dir, case)
            result = reports1.create_file_report()
            print(json.dumps(result))

        elif func_name.strip() == "calendarGnr":

            calendar1= Calendar1()
            result = calendar1.obtener_fechas_trimestre()
            print(json.dumps(result, ensure_ascii=False))

        elif func_name.strip() == "calendar_cus":
            year = int(sys.argv[2])

            calendar2 = Calendar2(year)
            result = calendar2.obtener_fechas_trimestre_cust()
            print(json.dumps(result))

        elif func_name.strip() == "nor_query_ZHR26":
            filequery1 = sys.argv[2]
            pathdirectory = sys.argv[3]

            normalizar = Normalizar(filequery1, pathdirectory)
            result = normalizar.normalize_query_ZHR26()
            print(json.dumps(result))

        elif func_name.strip() == "nor_dates":
            filequery1 = sys.argv[2]
            pathdirectory = sys.argv[3]

            normalizar = Normalizar(filequery1, pathdirectory)
            result = normalizar.adapt_dates()
            print(json.dumps(result))

        elif func_name.strip() == "nor_query_FLEXI":
            filequery1 = sys.argv[2]
            pathdirectory = sys.argv[3]

            normalizar = Normalizar(filequery1, pathdirectory)
            result = normalizar.normalize_query__FLEXI()
            print(json.dumps(result))

        elif func_name.strip() == "val_dup_info":
            filequery1 = sys.argv[2]
            pathdirectory = sys.argv[3]

            normalizar = Normalizar(filequery1, pathdirectory)
            result = normalizar.validate_duplica_Infotipos()
            print(json.dumps(result))

        elif func_name.strip() == "val_dup_2001":
            filequery1 = sys.argv[2]
            pathdirectory = sys.argv[3]

            normalizar = Normalizar(filequery1, pathdirectory)
            result = normalizar.validate_duplica_2001()
            print(json.dumps(result))

        elif func_name.strip() == "con_FLEXI_PARAM":
            filequery1 = sys.argv[2]
            filequery2 = sys.argv[3]
            pathdirectory = sys.argv[4]

            consolidate= Consolidate(filequery1, filequery2, pathdirectory)
            result = consolidate.merge_csv_files()
            print(json.dumps(result))

        elif func_name.strip() == "con_end":
            filequery1 = sys.argv[2]
            filequery2 = sys.argv[3]
            pathdirectory = sys.argv[4]

            consolidate= Consolidate(filequery1, filequery2, pathdirectory)
            result = consolidate.consolidate_end()
            print(json.dumps(result))

        elif func_name.strip() == "con_POSICION_PARAM":
            filequery1 = sys.argv[2]
            filequery2 = sys.argv[3]
            pathdirectory = sys.argv[4]

            consolidate= Consolidate(filequery1, filequery2, pathdirectory)
            result = consolidate.consolidate_param_posicion()
            print(json.dumps(result))

        elif func_name.strip() == "nor_segmeta_base":
            filequery1 = sys.argv[2]
            pathdirectory = sys.argv[3]
            pathUpload = sys.argv[4]

            segmentation = Segmentation(filequery1, pathdirectory, pathUpload)
            result = segmentation.create_file_load()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_AVG":
            output_dir = sys.argv[2]

            reports2 = Reports2(output_dir)
            result = reports2.consolidate_AVG()
            print(json.dumps(result))

        elif func_name.strip() == "validate_date":
            output_dir = sys.argv[2]

            reports2 = Reports2(output_dir)
            result = reports2.validar_fechas_excel()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_GNR":
            output_dir = sys.argv[2]

            reports2 = Reports2(output_dir)
            result = reports2.consolidate_GNR()
            print(json.dumps(result))

        elif func_name.strip() == "cre_AVG_PLUS_GNR":
            filequery1 = sys.argv[2]
            filequery2 = sys.argv[3]
            pathdirectory = sys.argv[4]

            consolidate= Consolidate(filequery1, filequery2, pathdirectory)
            result = consolidate.merge_AVG_GNR()
            print(json.dumps(result))

        elif func_name.strip() == "cre_TOTAL":
            filequery1 = sys.argv[2]
            filequery2 = sys.argv[3]
            pathdirectory = sys.argv[4]

            consolidate= Consolidate(filequery1, filequery2, pathdirectory)
            result = consolidate.merge_ROWS_PROCESS()
            print(json.dumps(result))

        elif func_name.strip() == "validate_minimo":
            file_total = sys.argv[2]
            out_directory = sys.argv[3]
            minAVM = sys.argv[4]
            minOTR = sys.argv[5]

            minims= Minimos(file_total, out_directory, minAVM, minOTR)
            result = minims.validate_minimos()
            print(json.dumps(result))

        elif func_name.strip() == "validate_minimo_GNR":
            file_total = sys.argv[2]
            out_directory = sys.argv[3]
            minAVM = sys.argv[4]
            minOTR = sys.argv[5]

            minims= Minimos(file_total, out_directory, minAVM, minOTR)
            result = minims.validate_minimos_report_gnr()
            print(json.dumps(result))

        elif func_name.strip() == "add_change_amount":
            filequery1 = sys.argv[2]
            filequery2 = sys.argv[3]
            pathdirectory = sys.argv[4]

            consolidate = Consolidate(filequery1, filequery2, pathdirectory)
            result = consolidate.merge_change_amount()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_Duplicados":
            input_path = sys.argv[2]
            output_dir = sys.argv[3]
            case = sys.argv[4]

            reports1= Reports1(input_path, output_dir, case)
            result = reports1.validate_user_duplica()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_UserSAP":
            infile1= sys.argv[2]
            infile2 = sys.argv[3]
            outdirectory = sys.argv[4]

            reports3= Reports3(infile1, infile2, outdirectory)
            result = reports3.stage_User_ValidSAP()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_Pos":
            infile1= sys.argv[2]
            infile2 = sys.argv[3]
            outdirectory = sys.argv[4]

            reports3= Reports3(infile1, infile2, outdirectory)
            result = reports3.report_GNR_Pos()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_Mon":
            infile1= sys.argv[2]
            infile2 = sys.argv[3]
            outdirectory = sys.argv[4]

            reports3= Reports3(infile1, infile2, outdirectory)
            result = reports3.report_GNR_montos()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_ExiUsr":
            infile1= sys.argv[2]
            infile2 = sys.argv[3]
            outdirectory = sys.argv[4]

            reports3= Reports3(infile1, infile2, outdirectory)
            result = reports3.report_GNR_ExisUser()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_NewUsr":
            infile1= sys.argv[2]
            infile2 = sys.argv[3]
            outdirectory = sys.argv[4]

            reports3= Reports3(infile1, infile2, outdirectory)
            result = reports3.consolidate_Report_New_User()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_AdjMin":
            infile1= sys.argv[2]
            infile2 = sys.argv[3]
            outdirectory = sys.argv[4]

            reports3= Reports3(infile1, infile2, outdirectory)
            result = reports3.consolidate_Report_Minimun()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_Final":
            input_path = sys.argv[2]
            output_dir = sys.argv[3]
            case = sys.argv[4]

            reports1= Reports1(input_path, output_dir, case)
            result = reports1.consolidate_Final()
            print(json.dumps(result))

        elif func_name.strip() == "cre_repot_Final_Simple":
            input_path = sys.argv[2]
            output_dir = sys.argv[3]
            case = sys.argv[4]

            reports1= Reports1(input_path, output_dir, case)
            result = reports1.consolidate_Final_Simple()
            print(json.dumps(result))

        elif func_name.strip() == "file_cancelation_HANA":
            input_file1 = sys.argv[2]
            input_file2 = sys.argv[3]
            output_folder = sys.argv[4]

            reports4= Reports4(input_file1, input_file2, output_folder)
            result = reports4.arreglo_comparison_file_HANA()
            print(json.dumps(result))

        elif func_name.strip() == "file_cancelation_R3":
            input_file1 = sys.argv[2]
            input_file2 = sys.argv[3]
            output_folder = sys.argv[4]

            reports4= Reports4(input_file1, input_file2, output_folder)
            result = reports4.arreglo_comparison_file_R3()
            print(json.dumps(result))



    except Exception as err:
        print(json.dumps({"error": True, "msj": "Error critico: "+str(err)}))


if __name__ == "__main__":
    shellHandler()
