from sklearn.model_selection import train_test_split
from modulosS.statisticsData import StatisticsData
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from os import system
class Analizador(StatisticsData):
    def DataBinColumn(self):
        special_c = []
        for col in self.df.select_dtypes(include=['object']):  # Focus on string columns
            unique_values = self.df[col].unique()  # Get unique values in the column
            special_c.append(col)
            self.df[col] = self.df[col].astype('category')  # Convert to categorical type (optional)
            for value in unique_values:
                self.df[f'{col}_{value}'] = (self.df[col] == value).astype(int)
        for i in special_c:
            del self.df[i]
    def DataBinColumnAnother(self, df):
        special_c = []
        for col in df.select_dtypes(include=['object']):  # Focus on string columns
            unique_values = df[col].unique()  # Get unique values in the column
            special_c.append(col)
            df[col] = df[col].astype('category')  # Convert to categorical type (optional)
            for value in unique_values:
                df[f'{col}_{value}'] = (df[col] == value).astype(int)
        for i in special_c:
            del df[i]
    def addColumn(self, Ncolumn):
        if len(self.df) == len(Ncolumn) and not isinstance(Ncolumn, dict):
            if isinstance(Ncolumn, list) or isinstance(Ncolumn, tuple) or isinstance(Ncolumn, pd.Series) or isinstance(Ncolumn, np.array):
                Ncolumn = pd.DataFrame(Ncolumn)
                self.df[str(input("Nombre de columna: "))] = Ncolumn
            else:
                return ValueError("Formato incorrecto\nLa columna nueva debe tener el mismo tamaño para el dataframe")
        elif isinstance(Ncolumn, dict):
            nOb = (list(Ncolumn.keys()))
            if len(nOb) != 1:
                return ValueError("Not a single column")
            elif len(Ncolumn[nOb[0]]) == len(self.df):
                self.df[nOb[0]] = Ncolumn[nOb[0]]
            else:
                return ValueError("Formato incorrecto\nLa columna nueva debe tener el mismo tamaño para el dataframe")
        else:
            return ValueError("Formato incorrecto\nLa columna nueva debe tener el mismo tamaño para el dataframe")
    def addData(self, data):
        if isinstance(data, dict):
            d = pd.DataFrame(data)
            longi = len(data)
            s = 0
            for i in self.df:
                s+=1
            if longi == s:
                d = pd.concat([d, self.df], axis=0)
                self.df = d
                d = None
            else:
                ValueError("Tamaños diferentes en las columnas")
        elif isinstance(data, pd.DataFrame):
            d = pd.concat([d, self.df], axis=0)
            self.df = d
            d = None
        else:
            self.addColumn(data)
    def SelectRegressionModel(self):
        self.df.fillna(0, inplace=True)
        x = self.df.iloc[:, :-1]
        y = self.df["SalePrice"]
        porcOLS = []
        porcSGD = []
        porcRidge = []
        porcLasso = []
        porcRf = []
        pruebas = np.random.randint(10, 30)
        for i in range(pruebas):
            if self.SO == "Windows":
                system("cls")
            else:
                system("clear")
            print("Entrenando modelos")
            x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3, shuffle=True, random_state=i)
            mean_y_test = np.mean(y_test)
            #Linear OLS Regressor:
            self.RegresionLOLS.fit(x_train, y_train)
            spredOLS = self.RegresionLOLS.predict(x_test)
            mean_spredOLS = np.mean(spredOLS)
            porcOLS.append(abs(mean_y_test - mean_spredOLS))
            if self.SO == "Windows":
                system("cls")
            else:
                system("clear")
            print("Entrenando modelos")
            #Linear SGD Regressor:
            self.RegresionLSGD.fit(x_train, y_train)
            spredsgd = self.RegresionLSGD.predict(x_test)
            mean_spredsgd = np.mean(spredsgd)
            porcSGD.append(abs(mean_y_test - mean_spredsgd))
            if self.SO == "Windows":
                system("cls")
            else:
                system("clear")
            print("Entrenando modelos")
            #Ridge
            self.RegresionRidge.fit(x_train, y_train)
            ridgepred = self.RegresionRidge.predict(x_test)
            mean_ridgepred = np.mean(ridgepred)
            porcRidge.append(abs(mean_y_test - mean_ridgepred))
            print("Entrenando modelos")
            if self.SO == "Windows":
                system("cls")
            else:
                system("clear")
            print("Entrenando modelos")
            #Lasso
            self.RegresionLasso.fit(x_train, y_train)
            lassoPredict = self.RegresionLasso.predict(x_test)
            mean_lassoPredict = np.mean(lassoPredict)
            porcLasso.append(abs(mean_y_test - mean_lassoPredict))
            print("Entrenando modelos")
            if self.SO == "Windows":
                system("cls")
            else:
                system("clear")
            print("Entrenando modelos")
            #RandomForest
            self.RegresionRandomForest.fit(x_train, y_train)
            RFpred = self.RegresionRandomForest.predict(x_test)
            mean_RFpred = np.mean(RFpred)
            porcRf.append(abs(mean_y_test - mean_RFpred))

        absolute_means = [np.mean(porcOLS), np.mean(porcSGD), np.mean(porcRidge), np.mean(porcLasso), np.mean(porcRf)]
        minimo = min(absolute_means)
        tit = ""
        if minimo == absolute_means[0]:
            self.selectedModel = self.RegresionLOLS
            tit = "Regresion lineal OLS"
        elif minimo == absolute_means[1]:
            self.selectedModel = self.RegresionLSGD
            tit = "Regresion lineal SGD"
        elif minimo == absolute_means[2]:
            self.selectedModel = self.RegresionRidge
            tit = "Regresion Ridge"
        elif minimo == absolute_means[3]:
            self.selectedModel = self.RegresionLasso
            tit = "Regresion Lasso"
        elif minimo == absolute_means[4]:
            self.selectedModel = self.RegresionRandomForest
            tit = "Regresion Random Forest"

        print(f"Mean absolute difference from y_test mean with un total de {pruebas} ensayos\n\tRegresionLineal OLS: {absolute_means[0]}\n\tRegresion Lineal SGD: {absolute_means[1]}\n\tRegresion Ridge: {absolute_means[2]}\n\tRegresion Lasso: {absolute_means[3]}\n\tRegresion por Random Forest: {absolute_means[4]}\n\tSelected Model: {tit}")
    def predecir(self, df):
        self.SelectRegressionModel()
        """
        df es la direccion de un dataset fuera del programa que nos dará datos de las casas con la misma estructura que el que hay aquí
        escribe "help" en caso de no conocer la estructura
        """
        if isinstance(df, str) and df[0] == "{" and df[len(df)-1] == "}" or ".json" in df:
            df = pd.read_json(df)
            
        elif isinstance(df, str) and ("xml" in df or ("<" in df and ">" in df)) or ".xml" in df:
            df = pd.read_xml(df)
        elif isinstance(df, dict):
            df = pd.DataFrame(df)
        elif isinstance(df, str) and ".csv" in df:
            df = pd.read_csv(df)
        elif isinstance(df, str) and ".xlsx" in df:
            df = pd.read_excel(df)
        elif isinstance(df, pd.DataFrame):
            pass
        else:
            raise Exception("Datos no válidos")
        #Limpiando data nueva:
        df = self.limpiarData(df)
        x = self.df.iloc[:, :-1]
        y = self.df["SalePrice"]
        self.selectedModel.fit(x, y)
        pred = self.selectedModel.predict(df)
        df["SalePrice"] = pred
        cdf = []
        for i in df:
            cdf.append(i)
        cselfdf =[]
        for i in self.df:
            cselfdf.append(i)
        if cdf == cselfdf:
            print("Logrado")
        else: 
            print("Error de longitudes inespearado")
            print(cdf)
            print(cselfdf)
        #Aqui se debe añadir el df al self.df
        self.log = df
        print(df)
        self.df = pd.concat([self.df, df])

    def limpiarData(self, df):
        if df is not None:
            if isinstance(df, str) and df[0] == "{" and df[len(df)-1] == "}" or ".json" in df:
                df = pd.read_json(df)
            elif isinstance(df, str) and ("xml" in df or ("<" in df and ">" in df)) or ".xml" in df:
                df = pd.read_xml(df)
            elif isinstance(df, dict):
                df = pd.DataFrame(df)
            elif isinstance(df, str) and ".csv" in df:
                df = pd.read_csv(df)
            elif isinstance(df, pd.DataFrame):
                pass
            else:
                return "Datos no válidos"
            df = self.binarizedOtherData(df)
            contardf = 0
            contarself = 0
            if "Id" in df:
                df.drop(columns=["Id"])

            correlaciones = [i for i in self.SearchDataCorrelation()["Minimos"]]
            for i in self.SearchDataCorrelation()["Maximos"]:
                correlaciones.append(i)
            #Ahora sacamos los valores que irán en las tablas:
            atributos = []
            for i in correlaciones:
                t = list(i.keys())
                atributos.append(t[0])
            #print(len(atributos))
            #Veremos que columnas no estan en atributos primero en df:
            eliminaciondf = []
            for i in df:
                contardf+=1
                if i not in atributos:
                    eliminaciondf.append(i)
            #Eliminamos las columnas correspondientes:
            df1 = df.drop(columns=eliminaciondf)
            self.limpiarSelfData()
            #print(df1)
            return df1
    def limpiarSelfData(self):
        correlaciones = [i for i in self.SearchDataCorrelation()["Minimos"]]
        for i in self.SearchDataCorrelation()["Maximos"]:
            correlaciones.append(i)
        #Ahora sacamos los valores que irán en las tablas:
        atributos = []
        for i in correlaciones:
            t = list(i.keys())
            atributos.append(t[0])
        atributos.append("SalePrice")
        #print(len(atributos))
        eliminaciondf = []
        contarself = 0
        for i in self.df:
            contarself+=1
            if i not in atributos:
                eliminaciondf.append(i)
        self.df = self.df.drop(columns=eliminaciondf)
        