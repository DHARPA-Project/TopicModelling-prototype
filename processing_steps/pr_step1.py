from kiara import Kiara
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation
import os
import pandas as pd
import re

dir_list = [dir for dir in os.listdir('./datasets/') if dir != '.DS_Store']


def get_df(folder):

    kiara = Kiara.instance()

   
    op = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
    inputs = {"path": folder}
    job_id = op.queue_job(**inputs)

    try:
        op.save_result(
        job_id=job_id, aliases={'file_bundle': 'text_file_bundle'}
    )
    except Exception:
        pass

    
    
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
        sources['date'] = pd.to_datetime(sources['date'])
        sources = sources.sort_values(by='date')

        preview1 = sources.head()
        preview2 = sources.tail()

        # data for viz

        df = sources[['date', 'publication_name', 'publication']].copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')

        def data_agg(df,pub_list):

            df_main = pd.DataFrame()

            for publication in pub_list:

                df_year = df.groupby([pd.Grouper(freq='Y'), 'publication_name']).count()
                df_year['agg'] = 'year'
                
                df_month = df.groupby([pd.Grouper(freq='M'), 'publication_name']).count()
                df_month['agg'] = 'month'

                df_week = df.groupby([pd.Grouper(freq='W'), 'publication_name']).count()
                df_week['agg'] = 'week'

                df_day = df.groupby([pd.Grouper(freq='D'), 'publication_name']).count()
                df_day['agg'] = 'day'

                df_main = pd.concat([df_main, df_year,df_month,df_day])
            
            return df_main
        
        df_distrib = data_agg(df,publications_list)

        # cleaning up
        df_distrib = df_distrib.rename(columns={"publication": "count"})
        df_distrib = df_distrib.reset_index(level=['date', 'publication_name'])
        df_distrib = df_distrib.drop_duplicates()

        #df_distrib['date'] = df_distrib['date'].astype('string')
        df_distrib['date'] = pd.to_datetime(df_distrib['date'])
        df_distrib['count'] = df_distrib['count'].astype('string')

        #print(df_distrib.head())
       
        df_distrib = df_distrib.sort_values(by='date')
        viz_data = df_distrib.to_dict('records')
        

    return {'preview1': preview1.to_dict('records'),
            'preview2': preview2.to_dict('records'),
            'files-len': len(files_list_flat),
            'pub-list-len': len(publications_list),
            'viz-data': viz_data
            } if dir_list and folder != None else None    




