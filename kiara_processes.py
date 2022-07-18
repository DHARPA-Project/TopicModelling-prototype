from kiara import Kiara
from kiara import Kiara
from kiara.interfaces.python_api.operation import KiaraOperation

# kiara processes that are used by the UI to let users create and handle data via Kiara and Kiara data store


# get head, tail and columns list for a given table
# this may need to be modified to use arrow methods and ultimately polars instead of pandas when possible
def get_table_preview(alias):

    kiara = Kiara.instance()

    table_value = kiara.data_registry.get_value(f'alias:{alias}')

    if not table_value:
        return ('Table not found')
    
    else:
        table_obj = table_value.data
        arrow_table = table_obj.arrow_table
        df = arrow_table.to_pandas()

        return df.head(), df.tail(), df.columns.values.tolist()


# used by 1st step: onboard a folder containing corpus and have it available as table
def onboard_df(corpus,alias):
    
    kiara = Kiara.instance()

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
        job_id=job_id, aliases={"table": f'{alias}'}
        )

    except Exception as e:
        print('nope')
        print(e)
        pass

    table_value = kiara.data_registry.get_value(f'alias:{alias}')

    if not table_value:
        return ('Table not found')
    
    else:

        return get_table_preview(alias)


# get metadata from corpus file names and augment table
def extract_metadata(alias,column):

    # table.cut_column
    # parse.date_array
    
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


# prepare data for the timestamped corpus viz
# this will need a bit of reworking since it would probably make more sense to directly 
# have data transformed into json instead of df
def timestamped_corpus_data(alias,col,agg):
    
    kiara = Kiara.instance()

    agg_table = KiaraOperation(kiara=kiara, operation_name="query.table")

    if agg == 'month':
        query = f"SELECT strptime(concat(month, '/', year), '%m/%Y') as date, {col} as publication_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, {col}, count(*) as count FROM data GROUP BY {col}, YEAR(date), MONTH(date))"
    
    elif agg == 'year':
        query = f"SELECT strptime(year, '%Y') as date, {col} as publication_name, count FROM (SELECT YEAR(date) as year, {col}, count(*) as count FROM data GROUP BY {col}, YEAR(date))"
    
    elif agg == 'day':
        query = query = f"SELECT strptime(concat('01/', month, '/', year), '%d/%m/%Y') as date, {col} as publication_name, count FROM (SELECT YEAR(date) as year, MONTH(date) as month, {col}, count(*) as count FROM data GROUP BY {col}, YEAR(date), MONTH(date), DAY(date))"
    
    inputs = {'table': f"alias:{alias}", 'query':query}

    job_id = agg_table.queue_job(**inputs)

    try:
        agg_table.save_result(
        job_id=job_id, aliases={"query_result": 'viz_data_tm'}
        )  

        table_value = kiara.data_registry.get_value(f'alias:viz_data_tm')
        table_obj = table_value.data

        arrow_table = table_obj.arrow_table
        df = arrow_table.to_pandas()
        

        return df

    except Exception as e:
        print('this thing did not work')
        print(e)
        pass


# get unique values of a table column
def get_col_unique_values(alias,col):

    kiara = Kiara.instance()
    table_value = kiara.data_registry.get_value(f'alias:{alias}')
    table_obj = table_value.data
    arrow_table = table_obj.arrow_table
    column = arrow_table.column(col)
    unique_val = column.unique().tolist()

    return unique_val

# augment table with mapped publication ids to publication names
def map_pub_ids(alias,col1,col2,replace):
    
    kiara = Kiara.instance()

    augmented_table = KiaraOperation(kiara=kiara, operation_name="kiara_plugin.playground.playground.mariella.map_column")
    inputs = {'table_input': f"alias:{alias}", 'column_name':col1, 'mapping_keys':replace, 'output_col_name':col2}
    job_id = augmented_table.queue_job(**inputs)
    
    try:
        augmented_table.save_result(
        job_id=job_id, aliases={"table_output": 'tm_publication_names'}
        )

    except Exception as e:
        print(e)
        pass

    return [get_table_preview('tm_publication_names'), 'tm_publication_names']