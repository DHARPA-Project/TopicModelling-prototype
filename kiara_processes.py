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

    print('hello')
    print('*************************************')
    print('*************************************')
    
    kiara = Kiara.instance()

    augmented_table = KiaraOperation(kiara=kiara, operation_name="kiara_plugin.playground.playground.mariella.file_name_metadata")
    inputs = {'table_input': f"alias:{alias}", 'column_name':column}
    job_id = augmented_table.queue_job(**inputs)
    
    try:
        augmented_table.save_result(
        job_id=job_id, aliases={"table_output": 'tm_metadata', 'publication_ref':'pub_refs','publication_counts':'pub_count'}
        )
        

    except Exception as e:
        print(e)
        pass
        

    return get_table_preview('tm_metadata')




