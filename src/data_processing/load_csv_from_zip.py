import pandas as pd
from zipfile import ZipFile

'''
Helper function that loads a list of datasets from a zip file into a list of pandas.DataFrame structures.

Args:
 - ZipFileName: A string representing the path and name of the zip file.
 - FileNameList: A list of strings each representing a dataset file contained in the zip file.
 - encoding: A list of strings representing the encoding of each dataset files.

Return:
 - A list of pandas.DataFrame structures.

Example:

import load_csv_from_zip as lcfz
dfs = lcfz.read_csv_from_zip('./data/raw/Abt-Buy.zip', ['Abt.csv', 'Buy.csv', 'abt_buy_perfectMapping.csv'], ['ISO-8859-1', 'ascii', 'ascii'])

OR

df1, df2, df3 = lcfz.read_csv_from_zip('./data/raw/Abt-Buy.zip', ['Abt.csv', 'Buy.csv', 'abt_buy_perfectMapping.csv'], ['ISO-8859-1', 'ascii', 'ascii'])

'''

def read_csv_from_zip(ZipFileName: str,FileNameList: list, encodings=[])->list:
    if(len(FileNameList) != len(encodings)): encodings = ['utf-8' for _ in FileNameList]  # If the length of the encoding list does not match the length of the file names, set them all to utf-8 by default
    df_list = []
    with ZipFile(ZipFileName, 'r') as zip:
        for idx, FileName in enumerate(FileNameList):
            with zip.open(FileName) as file:
                df = pd.read_csv(file, encoding=encodings[idx])
                df_list.append(df)

    return df_list
