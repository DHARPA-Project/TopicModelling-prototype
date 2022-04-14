import os
import pandas as pd
import re

dir_list = [dir for dir in os.listdir('./datasets/') if dir != '.DS_Store']


def get_df(folder):
    
    if dir_list and folder != None:
        
        publications_list = [file for file in os.listdir(f'./datasets/{folder}/') if file != '.DS_Store' ]
        
        files_list = []

        for pub in publications_list:
            files = os.listdir(f"./datasets/{folder}/{pub}/")
            files_list.append(files)
        
        files_list_flat = [item for sublist in files_list for item in sublist]
        
        sources = pd.DataFrame(files_list_flat, columns=['file_name'])

        # get publication ref from file name
        def get_ref(file):
            ref_match = re.findall(r'(\w+\d+)_\d{4}-\d{2}-\d{2}_',file)
            return ref_match[0]

        # get date from file name
        def get_date(file):
            date_match = re.findall(r'_(\d{4}-\d{2}-\d{2})_',file)
            return date_match[0]

        # pub names
        pub_refs = ["sn85066408","2012271201","sn84020351","sn85054967","sn84037024","sn84037025","sn85055164","sn86092310","sn92051386","sn93053873"]
        pub_names = ["L\'Italia","Cronaca Sovversiva","La Sentinella","Il Patriota","La Ragione","La Rassegna","La Libera Parola","La Sentinella del West","La Tribuna del Connecticut","L\'Indipendente"]
            
     
        sources['date'] = sources['file_name'].apply(lambda x: get_date(x))

        sources['publication'] = sources['file_name'].apply(lambda x: get_ref(x))

        sources['publication_name'] = sources['publication'].replace(pub_refs, pub_names)

        preview1 = sources.head()
        preview2 = sources.tail()

    
    return [preview1,preview2,len(files_list_flat),len(publications_list)] if dir_list and folder != None else None
    




