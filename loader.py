#!/home/mota/anaconda3/bin/python3.6

import pandas as pd
import importlib.util

import sqlite3

convert_spec = importlib.util.spec_from_file_location("convert", "/home/sp/ISD/Mem/projet_medical/convert.py")
convert_module = importlib.util.module_from_spec(convert_spec)
convert_spec.loader.exec_module(convert_module)

#SQLite_spec = importlib.util.spec_from_file_location("db", "/home/sp/ISD/Mem/projet_medical/SQLiteDB.py")
#db_module = importlib.util.module_from_spec(SQLite_spec)
#SQLite_spec.loader.exec_module(db_module)

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

def processFile(file, d):
    #Read a dictionary of DataFrames
    dictDF = pd.read_excel(file,sheet_name = None)

    #Write a new excel file
    writer = pd.ExcelWriter('./downloads/processedFile.xlsx',engine='xlsxwriter')

    #Create a DB connection
    conn = sqlite3.connect("mydatabase.db") # or :memory to put it in RAM

    for sheetDF in dictDF:
        cols_to_drop = []
        for column in list(dictDF[sheetDF]):
            if not column in d[sheetDF]:
                cols_to_drop.append(column)
            else:                
                #Fill Nan values
                if d[sheetDF][column]["behaviour"] == "mean":
                    dictDF[sheetDF][column].fillna(dictDF[sheetDF][column].mean())
                elif d[sheetDF][column]["behaviour"] == "default_value":
                    dictDF[sheetDF][column] = dictDF[sheetDF][column].fillna(d[sheetDF][column]["default_value"])

                #Check column type
                typeC = d[sheetDF][column]["type"]
                if typeC != str(dictDF[sheetDF][column].dtypes):
                    try: 
                        dictDF[sheetDF][column] = dictDF[sheetDF].astype(typeC)
                    except ValueError:
                        print('\x1b[0;31;40m' + 'Error while converting the column ', column + '\x1b[0m')

        dictDF[sheetDF] = dictDF[sheetDF].drop(cols_to_drop, axis=1)

        print(end='\n')
        print('\x1b[0;31;40m' + sheetDF + '\x1b[0m')
        print(dictDF[sheetDF].dtypes) 
        
        #Add sheet to the writer
        dictDF[sheetDF].to_excel(writer,sheet_name=sheetDF,startrow=0, startcol=0, index=False)
        
        # .tables 
        # PRAGMA table_info(table_name)

        # Add table to DB
        dictDF[sheetDF].to_sql(sheetDF, con=conn, if_exists='replace', index=None)

        '''
        cursor = conn.cursor()
        
        # create a table
        cursor.execute("""CREATE TABLE alboums
                        (title text, artist text, release_date text, 
                        publisher text, media_type text) 
                    """)
        # insert some data
        cursor.execute("INSERT INTO alboums VALUES ('Glow', 'Andy Hunter', '7/24/2012', 'Xplore Records', 'MP3')")
        
        # save data to database
        conn.commit()
        
        # insert multiple records using the more secure "?" method
        albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
                ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
                ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
                ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]
        cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
        conn.commit()
        '''
    return dictDF
    #return dictDF["Justificatifs"].to_json(orient='records')[1:-1].replace('},{', '} {')
#takes in parameter the dataframe dictionary indexed by sheet names to process and the types dictionary, parses the data and returns successfully parsed data and unseccessful parsed data

#prend en parametre un fichier, un sheet, un interval de lignes et de colonnes
#retourne un dataframe indexé par la premiere ligne et contenant les données selectionnées

def get_data_from_sheet(in_memory_excel_file, sheet_name,header_line, lines_number, columns_list):

    df = pd.read_excel(in_memory_excel_file,sheet_name = sheet_name, header = header_line, usecols =  columns_list  )
    return df.head(lines_number)
#header is 0 indexed, data starts from that line
#columns list is a list of integers  indexed to specify columns to parse

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