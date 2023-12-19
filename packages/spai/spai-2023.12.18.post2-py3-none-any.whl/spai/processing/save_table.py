import pandas as pd

def save_table(data, columns, table_name, date, storage):
    # columns number must be equal to data number of columns
    if len(columns) != len(data):
        raise ValueError("columns number must be equal to data number of columns")
    # check if table exists in storage
    if table_name in storage.list():
        # append data to table
        df = storage.read(table_name)
        if date in df.index:
            return df
        df = pd.concat([pd.DataFrame([data], columns=columns, index=[date]),df.loc[:]])
    else:
        # create table with data
        df = pd.DataFrame([data], columns=columns, index=[date])                          
    storage.create(data=df, name=table_name)
    return df
