#!/home/mota/anaconda3/bin/python3.6

# Import pandas
import pandas as pd


import importlib.util
spec = importlib.util.spec_from_file_location("convert", "/home/mota/projet_medical/convert.py")
convert_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(convert_module)


#convert_module = __import__('convert')

#loads excel file on memory
def load_excel_file(path):
    return pd.ExcelFile(path)

#returns a dictionary indexed by sheet names and each entry contains a list of column names
def get_excel_headers (excel_file):

    # Load spreadsheet
    result = {}

    for element in excel_file.sheet_names:
        result[element] = list(pd.read_excel(excel_file,sheet_name =element,  skip_footer = (excel_file.book.sheet_by_name(element).nrows - 1)))
    return result
    

#returns the pandas dataframe of the corresponding selected columns to work with
#filter is a dictionary indexed by sheet names and each entry contains a list of columns to drop
def filter_sheet_columns(in_memory_excel_file , filter):

    xl = pd.read_excel(in_memory_excel_file,sheet_name = None)

    for key in filter:
        for columns_to_drop in filter[key]:
            xl[key] = xl[key].drop(columns = columns_to_drop)

    return xl
#takes in parameter the dataframe dictionary indexed by sheet names to process and the types dictionary, parses the data and returns successfully parsed data and unseccessful parsed data



def parse_dataframe(dataframe_dict, types_dict):

    #types_dict est du format sheet => list[  (column_name, convertion_parameters)  ]
    for sheet in types_dict:

        for (column, parameter) in types_dict[sheet]:

            convertion_function = getattr(convert_module, parameter.type_function)

            dataframe_dict[sheet][column] = dataframe_dict[sheet][column].apply(lambda x : convertion_function(value = x, parameters = parameter))

            #partie pour gerer les entiers

            
            
            if parameter.type_function == "convert_int":
                dataframe_dict[sheet].dropna(inplace = True)
                dataframe_dict[sheet][column] = dataframe_dict[sheet][column].apply(int)
            #probleme de conversion des ints       



        #ici il faut supprimer toutes les lignes contenant du None ou bien les separer pour un traitement à part
        dataframe_dict[sheet].dropna(inplace = True)

        #(dataframe_dict[sheet]).dropna(inplace=True)
    #les types autorisés: int float string date.|time bool 
    #astype is useful only for clean data or from whatever to sitring


#functions de conversion à passer à apply pour convertir les types:

#string est le type par defaut

#on a soit un cast, soit un remlacement par mediane ou moyenne ou valeur par defaut, ou bien une suppression de la ligne (correspond à un NaN)