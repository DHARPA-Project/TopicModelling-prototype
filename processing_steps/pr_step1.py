import os
import pandas as pd

dir_list = [dir for dir in os.listdir('./datasets/') if dir != '.DS_Store']


def get_df(folder):
    if dir_list:
        print(f'./datasets/{folder}/')
        files_list = [file for file in os.listdir(f'./datasets/{folder}/') if file != '.DS_Store' ]
        sources = pd.DataFrame(files_list, columns=['file_name'])
    
    return sources
    




