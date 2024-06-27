import os
os.system("python3 bibliotecas.py")
from Analizador import Analizador
import platform 
import pandas as pd

def borrarP():
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")
print("BIENVENIDO AL PROGRAMA DE EVALUACIÓN DE CASAS")
print("------------------------------------------------")
menu = """
1. Ingresar la dirección donde se encuentran los datos históricos con el siguiente formato:
    C:/direccion/de/carpetas/al/archivo.ext
        Los archivos aceptados son:
            - .json
            - .xml
            - .csv
            - .xlsx
2. Ingresar la cadena de la estructura de datos, lo formatos aceptados son:
    '{
        "dato1":valor1,
        "dato2":valor2,
    }'
    ó
    '<xml><etiquetas></etiquetas></xml>'
3. Ingresar un diccionario de python con la siguiente estructura:
    {
        "host":str(),
        "user":str(),
        "password":str(),
        "db":str(),
        "port":str()
        "table" : str()
    }
    dónde str() representa que los datos que se ingresen allí serán cadenas de texto (palabras que irán entre comillas dobles o simples)
Recuerda que los datos deben tener una columna o apartado llamado 'SalePrice', ya que esta columna será la que evalúa el programa
"""
band = True
while band:
    try:
        usuario1 = Analizador(str(input("Insertar datos.\nPara insertar el historial de datos en el programa deberá ingresar uno de los siguientes\n"+ menu+"\n\tIngresa una de las 3 opciones (No ingresar números ni cadenas inválidas)\n\t\t> ")))
        opcs = """Opciones de uso 
        1. Mostrar gráfico de datos más relevantes para el precio
        2. Mostrar y guardar pdf de la tabla histórica de datos
        3. Añadir columna extra a los datos
        4. Predecir precios de datos nuevos
        5. Limpiar y optimizar datos manulamente
        6. Visualizar las características principales de la casa
        7. Salir del programa
        """
        
        while True:
            borrarP()
            print(opcs)
            opc = int(input("\tOpción> "))
            if opc == 1:
                usuario1.GraficDataCorr()
            elif opc == 2:
                usuario1.ShowDataFrame()
                input()
            elif opc == 3:
                borrarP()
                opc2 = str(input("¿Cómo desea insertar su columna?\n\t1. Insertar datos manualmente\n\t2. Insertar direccion de archivo\n\t\t> "))
                if opc2 == "1":
                    ncol = str(input("Nombre de la columna: "))
                    opc3 = str(input("Su columna tiene datos (s/n): "))
                    band3 = False
                    if opc3[0] == "s" or opc3[0] == "1" or opc3[0] == "S" or opc3[0] == "Y" or opc3[0]=="y":
                        band3 = True
                    col1 = {ncol: []}
                    for i in range(len(usuario1.df)):
                        if band3:
                            col1[ncol].append(str(input("Valor de la columna: ")))
                        else:
                            col1[ncol].append(0)
                    print(col1)
                    usuario1.addColumn(col1)
                elif opc2 == "2":
                    ncol = str(input("Dirección y nombre de la columna en su computadora: "))
                    if ".xlsx" in ncol:
                        da = pd.read_excel(ncol)
                        usuario1.addColumn(da)
                    elif ".csv" in ncol:
                        da = pd.read_csv(ncol)
                        usuario1.addColumn(da)
                    elif ".json" in ncol:
                        da = pd.read_json(ncol)
                        usuario1.addColumn(da)
                    elif ".xml" in ncol:
                        da = pd.read_xml(ncol)
                        usuario1.addColumn(da)
                    else:
                        print("No se reconoce el formato de archivo")
                        input("Enter para continuar...")
            elif opc == 4:
                datosN = str(input("Dirección y nombre.extensión de el archivo dónde están los datos nuevos: "))
                usuario1.predecir(datosN)
                print("Datos predecidos y guardados en el historial")
                input("Enter para continuar...")
            elif opc == 5:
                usuario1.limpiarSelfData()
            elif opc == 6:
                borrarP()
                print("Características y su porcentaje de impacto en el precio de la vivienda\n\n")
                usuario1.limpiarSelfData()
                corm = usuario1.SearchDataCorrelation()["Minimos"]
                corM = usuario1.SearchDataCorrelation()["Maximos"]
                print("Correlación Negativas: \n")
                for i in corm:
                    a = list(i.keys())
                    v = list(i.values())
                    print(f"{a[0]} : {round(v[0]*100, 2)}%")
                
                print("--------------------\nCorrelación Positivas: \n")
                for i in corM:
                    a = list(i.keys())
                    v = list(i.values())
                    print(f"{a[0]} : {round(v[0]*100, 2)}%")
                #print(usuario1.SearchDataCorrelation())
                input("Presiona enter para continuar...")
            elif opc == 7:
                band = False
                break
    except Exception as e:
        borrarP()
        print("Error: ",e)
        input()
        borrarP()
quit()

        