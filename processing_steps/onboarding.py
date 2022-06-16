from kiara import Kiara
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation


def onboard_df(corpus,alias):
    print('onboarding')
    
    kiara = Kiara.instance()

    import_fb = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
    try:
        import_res = import_fb.run(path=corpus)
        file_bundle = import_res.get_value_obj('file_bundle')
    except Exception:
        print('sthg wrong first op')
        pass

    create_table = KiaraOperation(kiara=kiara, operation_name="create.table.from.text_file_bundle")
    inputs = {'text_file_bundle': file_bundle}
    job_id = create_table.queue_job(**inputs)
    
    try:
        create_table.save_result()
        job_id=job_id, aliases={"table": alias}

    except Exception:
        print('sthg wrong 2nd op')
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


