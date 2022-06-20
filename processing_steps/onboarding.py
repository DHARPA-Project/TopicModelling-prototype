from kiara import Kiara
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation


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
        print('Table not found')
        return ('Table not found')
    
    else:
        print('ok table')
        table_obj = table_value.data
        arrow_table = table_obj.arrow_table
        df = arrow_table.to_pandas()

        return df.head(), df.tail()


