from kiara import Kiara
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation



def get_table_preview(alias):

    kiara = Kiara.instance()

    table_value = kiara.data_registry.get_value(f'alias:{alias}')

    if not table_value:
        return ('Table not found')
    
    else:
        table_obj = table_value.data
        # see query table module
        arrow_table = table_obj.arrow_table
        df = arrow_table.to_pandas()

        return df.head(), df.tail(), df.columns.values.tolist()


def onboard_df(corpus,alias):
    
    kiara = Kiara.instance()

    #experiment without storing intermediary value in data store, but in this case 
    #it then takes much more time when needing to do the operation several time as 
    #intermediary process is quite long

    # import_fb = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
    # try:
    #     import_res = import_fb.run(path=corpus)
    #     file_bundle = import_res.get_value_obj('file_bundle')
    # except Exception as e:
    #     print(e)
    #     pass

    import_file_bundle = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
    inputs = {'path': corpus}
    job_id = import_file_bundle.queue_job(**inputs)
    
    try:
        import_file_bundle.save_result(
        job_id=job_id, aliases={"file_bundle": 'tm_onboarding'}
        )

    except Exception as e:
        print(e)
        pass


    create_table = KiaraOperation(kiara=kiara, operation_name="create.table.from.text_file_bundle")
    inputs = {'text_file_bundle': 'alias:tm_onboarding'}
    job_id = create_table.queue_job(**inputs)
    
    try:
        create_table.save_result(
        job_id=job_id, aliases={"table": 'tm_onboarding'}
        )

    except Exception as e:
        print(e)
        pass

    table_value = kiara.data_registry.get_value(f'alias:{alias}')

    if not table_value:
        return ('Table not found')
    
    else:
        # table_obj = table_value.data
        # arrow_table = table_obj.arrow_table
        # df = arrow_table.to_pandas()

        return get_table_preview(alias)


def extract_metadata(alias,column):
    
    kiara = Kiara.instance()

    output_alias = 'tm_metadata'


    augmented_table = KiaraOperation(kiara=kiara, operation_name="kiara_plugin.playground.playground.mariella.file_name_metadata")
    inputs = {'table_input': f"alias:{alias}", 'column_name':column}
    job_id = augmented_table.queue_job(**inputs)
    
    try:
        augmented_table.save_result(
        job_id=job_id, aliases={"table_output": output_alias, 'publication_ref':'pub_refs','publication_counts':'pub_count'}
        )
        

    except Exception as e:
        print(e)
        pass
        

    return get_table_preview('tm_metadata'), output_alias


def timestamped_corpus_data(alias):
    
    kiara = Kiara.instance()

    #sql_query_month = "SELECT strptime(concat('01/', month, '/', year), '%d/%m/%Y') as date, pub_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, pub_name, count(*) as count FROM data group by YEAR(date), MONTH(date), pub_name ORDER BY year, month, pub_name) AS agg"

    agg_table = KiaraOperation(kiara=kiara, operation_name="query.table")
    inputs = {'table': f"alias:{alias}", 'query':"SELECT strptime(concat('01/', month, '/', year), '%d/%m/%Y') as date, publication as publication_name, count FROm (SELECT YEAR(date) as year, MONTH(date) as month, publication, count(*) as count FROM data GROUP BY publication, YEAR(date), MONTH(date))"}

    job_id = agg_table.queue_job(**inputs)

    try:
        agg_table.save_result(
        job_id=job_id, aliases={"query_result": 'viz_data_tm'}
        )  

        table_value = kiara.data_registry.get_value(f'alias:viz_data_tm')
        table_obj = table_value.data

        # see query table module
        arrow_table = table_obj.arrow_table
        df = arrow_table.to_pandas()
        print(df)
        print(df.info())

        return df

    except Exception as e:
        print('this thing did not work')
        print(e)
        pass










