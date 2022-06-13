from kiara import Kiara
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation


def onboard_df(corpus,alias):
    
    kiara = Kiara.instance()
   
    op = KiaraOperation(kiara=kiara, operation_name="import.file_bundle")
    inputs = {"path": corpus}
    job_id = op.queue_job(**inputs)

    try:
        op.save_result(
        job_id=job_id, aliases={'file_bundle': 'text_file_bundle'}
    )
    except Exception:
        pass


    op = KiaraOperation(kiara=kiara, operation_name="create.table.from.text_file_bundle")
    inputs = {"text_file_bundle": 'alias:text_file_bundle'}
    job_id = op.queue_job(**inputs)

    try:
        op.save_result(
        job_id=job_id, aliases={"table": alias}
    )
    except Exception:
        pass


    table_value = kiara.data_registry.get_value(f'alias:{alias}')


    actual_table_obj = table_value.data
    arrow_table = actual_table_obj.arrow_table
    df = arrow_table.to_pandas()

    return df.head(), df.tail()


