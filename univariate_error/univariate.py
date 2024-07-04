class univariate():
    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            print(columnName)
            if(dataset[columnName].dtype=='object'):
                print("qual")
                qual.append(columnName)
            else:
                print("quan")
                quan.append(columnName)
        return quan,qual
    def freqTable(columnName,dataset):
        freqTable=pd.DataFrame(columns=["unique_values","Frequency","Relative_frequency","Cumsum"])
        freqTable["unique_values"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Relative_frequency"]=(freqTable["Frequency"]/103)
        freqTable["Cumsum"]=freqTable["Relative_frequency"].cumsum()
        return freqTable
    def Univariate(dataset,quan):
        import pandas as pd
        import numpy as np
        descriptive=pd.DataFrame(index=["mean","median","mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%",
                                   "IQR","1.5rule","Lesser","Greater","Min","Max"],columns=quan)
        for columnName in quan:
            descriptive[columnName]["mean"]=dataset[columnName].mean()
            descriptive[columnName]["median"]=dataset[columnName].median()
            descriptive[columnName]["mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]-descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]=descriptive[columnName]["Q1:25%"]-descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"]+descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"]=dataset[columnName].min()
            descriptive[columnName]["Max"]=dataset[columnName].max()
        return descriptive
    def Finding_outliers(descriptive, Quan):
        Lesser = []
        Greater = []
        for ColumnName in Quan:
            if descriptive[ColumnName]["Min"] < descriptive[ColumnName]["Lesser"]:
                Lesser.append(ColumnName)
            if descriptive[ColumnName]["Max"] > descriptive[ColumnName]["Greater"]:
                Greater.append(ColumnName)
        return Lesser, Greater
    def Handle_outliers(dataset, descriptive, Quan):
        #Lesser, Greater = Finding_outliers(descriptive, Quan)
        for ColumnName in Lesser:
            dataset.loc[dataset[ColumnName] < descriptive[ColumnName]["Lesser"], ColumnName] = descriptive[ColumnName]["Lesser"]
        for ColumnName in Greater:
            dataset.loc[dataset[ColumnName] > descriptive[ColumnName]["Greater"], ColumnName] = descriptive[ColumnName]["Greater"]
        return dataset