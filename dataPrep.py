import pandas as pd

def loadData(type, filePath):
    if type == "csv":
        return pd.read_csv(filePath)
    elif type == "excel":
        return pd.read_excel(filePath)

def delRows(df, rows):
    return df.drop(rows, axis=0)

def delColumns(df, cols):
    return df.drop(cols, axis=1)

def replace_val(df, val1, val2):
    if val1 == ' ': 
        df = df[df == val1] = val2
    else:
        df = df.replace(val1, val2)
    return df

def fillna(df, val):
    return df.fillna(val)

def exportToCSV(df, name):
    df.to_csv(name, sep = ',')

def describe(df):
    return df.describe()

def inspectDF(df, rows=10):
    return df.head(rows)

def processFile(df, json):
        return True