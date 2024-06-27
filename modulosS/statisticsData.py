import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import psycopg2
import pymysql
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge,Lasso
from sklearn.ensemble import RandomForestRegressor
from platform import system
import pdfkit
class StatisticsData:
    def __init__(self, df):
        self.log = []
        self.errors = []
        self.ErrorsPercent = 0

        if isinstance(df, str) and( (df[0] == "{" and df[len(df)-1] == "}") or ".json" in df):
            self.df = pd.read_json(df)
        elif isinstance(df, str) and ".xml" in df:
            self.df = pd.read_xml(df)
        elif isinstance(df, str) and ".csv" in df:
            self.df = pd.read_csv(df)
        elif isinstance(df, str) and ".xlsx" in df:
            self.df = pd.read_excel(df)
        elif isinstance(df, pd.DataFrame):
            self.df = df
        elif isinstance(df, dict):
            if df["database"] == "mysql":
                conn = pymysql.connect(
                    host=df["host"],
                    user=df["user"],
                    password=df["password"],
                    db=df["db"],
                    port=df["port"]
                )
                query = f"SELECT * FROM {df['table']}"
                self.df = pd.read_sql_query(query, conn)
                conn.close()
            elif df["database"] == "postgresql":
                conn = psycopg2.connect(
                    host=df["host"],
                    user=df["user"],
                    password=df["password"],
                    db=df["db"],
                    port=df["port"]
                )
                query = f"SELECT * FROM {df['table']}"
                self.df = pd.read_sql_query(query, conn)
                conn.close()
            elif df["database"] == "mongo":
                client = MongoClient(df["client"])
                db = client[df["db"]]
                collection = db[df["collection"]]
                data = list(collection.find())
                self.df = pd.DataFrame(data)
            else:
                raise ValueError("Database type not supported")
        else:
            raise ValueError("No Type supported")
        
        self.df = self.df.drop(columns=["Id"])
        self.OriginalDf = self.df.copy()
        try:
            y = self.df.iloc[:, -1]
            self.df = self.df.drop(columns=["Id", "SalePrice"], errors='ignore')
            self.df = self.binarizedData()["df_binarized"]
            self.df = self.df.assign(SalePrice=y)
        except Exception as e:
            self.df = df

        self.Errors = []
        self.errorPercent = 0
        self.RegresionLOLS = LinearRegression()
        self.RegresionLSGD = SGDRegressor()
        self.RegresionRidge = Ridge()
        self.RegresionLasso = Lasso()
        self.RegresionRandomForest = RandomForestRegressor()
        self.selectedModel = None
        self.SO = system()
        

    def ShowDataFrame(self):
        self.df.to_excel(str(input("Nombre del archivo de excel: ")) + ".xlsx", index=False)
        self.df.to_html("Tabla histórica.html")
        print(self.df)
        input("Enter para continuar...")
        #pdfkit.from_string(excel, "Tabla histórica.pdf")
        return self.df

    def SearchDataCorrelation(self):
        try:
            #correlaciones con relacion a la columna y
            y = self.df.iloc[:,-1]
            x = self.df.iloc[:, :-1]
            corr1 = {} #Guardará el porcentaje de correlacion con relacion a y
            for i in x:
                if str(x[i][0]).isnumeric():
                    corr1[i] = np.corrcoef(x[i], y)[0, 1]
            #Ahora debemos buscar los indices que estén más cercanos al 1
            maximos = []
            minimos = []
            for i in (corr1):
                if corr1[i]*100 > 0:
                    maximos.append({i : corr1[i]})
                elif corr1[i] < 0:
                    minimos.append({i: corr1[i]})
            maximos = sorted(maximos, key=lambda x: list(x.values())[0], reverse=True)
            minimos = sorted(minimos, key=lambda x: list(x.values())[0])

            # print("\t\tDatos de correlacion")
            # print("Datos directamente proporcionales: ")
            # for i in maximos:
            #     print(f"{i}")
            # print("Datos inversamente proporcionales")
            # for i in minimos:
            #     print(f"{i}")
            return {"Minimos" : minimos, "Maximos":maximos, "status":True}
        except Exception as e:
            return {"message" : e, "status" : False}
    def help(self):
        # Método que describe la funcionalidad de la clase StatisticsData y sus métodos
        description = """
    La clase StatisticsData permite cargar, manipular y analizar datos estadísticos, 
    específicamente orientada al análisis de precios de viviendas.

    Métodos disponibles:

    - ShowDataFrame(): Muestra el DataFrame actual cargado en la instancia.

    - SearchDataCorrelation(): Calcula las correlaciones entre las variables y la variable objetivo.

    - errorAnalysis(y_pred): Analiza los errores de predicción comparando los valores predichos con los observados.

    - GraficDataCorr(): Genera gráficos de las correlaciones máximas y mínimas entre variables.

    - trustRange(x_new, confidence=0.95): Calcula el rango de confianza para una nueva observación.

    - binarizedData(): Binariza los datos categóricos en el DataFrame.

    Columnas del dataframe:

    - MSSubClass: Clase de construcción.
    - MSZoning: Zonificación general de la ubicación de la vivienda.
    - LotFrontage: Longitud de la calle de la propiedad.
    - LotArea: Tamaño del lote en pies cuadrados.
    - Street: Tipo de acceso a la propiedad (pavimentado o de grava).
    - Alley: Tipo de acceso al callejón (pavimentado, de grava o sin acceso).
    - LotShape: Forma general del lote.
    - LandContour: Contorno de la propiedad (nivelado, en pendiente, etc.).
    - Utilities: Servicios disponibles (energía eléctrica, gas, agua y alcantarillado).
    - LotConfig: Configuración del lote (interior, esquina, etc.).
    - LandSlope: Pendiente de la propiedad.
    - Neighborhood: Ubicación física dentro de los límites de la ciudad de Ames.
    - Condition1: Proximidad a diversas condiciones (arterias principales, vías férreas, etc.).
    - Condition2: Proximidad a diversas condiciones (si hay más de una).
    - BldgType: Tipo de vivienda (unifamiliar, dúplex, etc.).
    - HouseStyle: Estilo de vivienda.
    - OverallQual: Calificación general del material y el acabado de la casa.
    - OverallCond: Calificación general del estado de la casa.
    - YearBuilt: Fecha de construcción original.
    - YearRemodAdd: Fecha de remodelación (igual a la fecha de construcción si no hay remodelación o adición).
    - RoofStyle: Tipo de techo.
    - RoofMatl: Material del techo.
    - Exterior1st: Revestimiento exterior principal.
    - Exterior2nd: Revestimiento exterior secundario (si hay más de uno).
    - MasVnrType: Tipo de revestimiento de mampostería.
    - MasVnrArea: Área de revestimiento de mampostería en pies cuadrados.
    - ExterQual: Calidad del material exterior.
    - ExterCond: Estado actual del material en el exterior.
    - Foundation: Tipo de cimientos.
    - BsmtQual: Altura del sótano.
    - BsmtCond: Estado general del sótano.
    - BsmtExposure: Paredes del sótano que dan al exterior.
    - BsmtFinType1: Calidad del área terminada del sótano.
    - BsmtFinSF1: Pies cuadrados de área terminada del sótano tipo 1.
    - BsmtFinType2: Calidad del segundo área terminada del sótano (si existe).
    - BsmtFinSF2: Pies cuadrados de área terminada del sótano tipo 2.
    - BsmtUnfSF: Pies cuadrados de área sin terminar del sótano.
    - TotalBsmtSF: Pies cuadrados totales del área del sótano.
    - Heating: Tipo de calefacción.
    - HeatingQC: Calidad y estado de la calefacción.
    - CentralAir: Aire acondicionado central.
    - Electrical: Sistema eléctrico.
    - 1stFlrSF: Pies cuadrados del primer piso.
    - 2ndFlrSF: Pies cuadrados del segundo piso.
    - LowQualFinSF: Pies cuadrados de acabado de baja calidad (todos los pisos).
    - GrLivArea: Pies cuadrados habitables sobre el nivel del suelo.
    - BsmtFullBath: Baños completos en el sótano.
    - BsmtHalfBath: Medios baños en el sótano.
    - FullBath: Baños completos sobre el nivel del suelo.
    - HalfBath: Medios baños sobre el nivel del suelo.
    - BedroomAbvGr: Habitaciones sobre el nivel del suelo.
    - KitchenAbvGr: Cocinas sobre el nivel del suelo.
    - KitchenQual: Calidad de la cocina.
    - TotRmsAbvGrd: Total de habitaciones sobre el nivel del suelo (no incluye baños).
    - Functional: Calificación de funcionalidad del hogar.
    - Fireplaces: Número de chimeneas.
    - FireplaceQu: Calidad de la chimenea.
    - GarageType: Ubicación del garaje.
    - GarageYrBlt: Año de construcción del garaje.
    - GarageFinish: Acabado interior del garaje.
    - GarageCars: Capacidad del garaje en términos de coches.
    - GarageArea: Tamaño del garaje en pies cuadrados.
    - GarageQual: Calidad del garaje.
    - GarageCond: Condición del garaje.
    - PavedDrive: Entrada pavimentada.
    - WoodDeckSF: Área de plataforma de madera en pies cuadrados.
    - OpenPorchSF: Área de porche abierto en pies cuadrados.
    - EnclosedPorch: Área de porche cerrado en pies cuadrados.
    - 3SsnPorch: Área de porche de tres estaciones en pies cuadrados.
    - ScreenPorch: Área de porche con pantalla en pies cuadrados.
    - PoolArea: Área de piscina en pies cuadrados.
    - PoolQC: Calidad de la piscina.
    - Fence: Calidad de la cerca.
    - MiscFeature: Otras características no cubiertas en otras categorías.
    - MiscVal: Valor de otras características.
    - MoSold: Mes de venta.
    - YrSold: Año de venta.
    - SaleType: Tipo de venta.
    - SaleCondition: Condición de venta.
    - SalePrice: Precio de venta de la propiedad.
    """
        print(description)
    def errorAnalisis(self, y_pred):
        try:
            y_true = self.df.iloc[:, -1]  # Valores observados
            
            if y_true.shape != y_pred.shape:
                raise ValueError("Dimensiones de los datos observados y predichos no coinciden.")
            
            errors = y_true - y_pred
            self.Errors = errors.tolist()
            self.errorPercent = np.mean(np.abs(errors) / np.abs(y_true)) * 100
            
            return {"Errors": self.Errors, "ErrorPercent": self.errorPercent, "status": True}
        except Exception as e:
            return {"message": str(e), "status": False}
    def GraficDataCorr(self):
        try:
            correlations = self.SearchDataCorrelation()
            
            if not correlations['status']:
                raise ValueError(correlations['message'])
            
            maximos = correlations['Maximos']
            minimos = correlations['Minimos']
            
            # Extraer nombres de variables y valores de correlación
            max_labels = [list(item.keys())[0] for item in maximos]
            max_values = [list(item.values())[0] for item in maximos]
            
            min_labels = [list(item.keys())[0] for item in minimos]
            min_values = [list(item.values())[0] for item in minimos]
            
            # Crear una sola gráfica para ambos maximos y mínimos
            plt.figure(figsize=(12, 6))
            
            # Graficar correlaciones máximas
            plt.bar(max_labels, max_values, color='blue', alpha=0.7, label='Correlaciones Positivas')
            for i in range(len(max_values)):
                plt.text(max_labels[i], max_values[i], f'{max_values[i]:.2f}', ha='center', va='bottom')
            
            # Graficar correlaciones mínimas
            plt.bar(min_labels, min_values, color='green', alpha=0.7, label='Correlaciones Negativas')
            for i in range(len(min_values)):
                plt.text(min_labels[i], min_values[i], f'{min_values[i]:.2f}', ha='center', va='bottom')
            
            plt.title('Correlaciones Máximas y Mínimas')
            plt.xlabel('Variables Independientes')
            plt.ylabel('Valor de Correlación')
            plt.xticks(rotation=90)  # Rotar etiquetas del eje x verticalmente
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            plt.show()
        
        except Exception as e:
            print({"message": str(e), "status": False})
    def trustRange(self):
        pass
    def binarizedData(self):
        try:
            df_binarized = pd.get_dummies(self.df)
            return {"df_binarized": df_binarized, "status": True}
        except Exception as e:
            return {"message": str(e), "status": False}
    def binarizedOtherData(self, df):
        try:
            df_binarized = pd.get_dummies(df)
            return df_binarized
        except Exception as e:
            return {"message": str(e), "status": False}