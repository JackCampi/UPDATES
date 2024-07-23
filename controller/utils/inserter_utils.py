import pandas as pd
from ...model.table import Table
from ...model.insert_conf import InsertConf

#for future, istead of require the table and index, require only the row

def build_statement(table: Table, insert: InsertConf, seq: pd.DataFrame) -> str:

    i = seq.index[0]

    statement = f'INSERT INTO {table.name}'
    # Write column name if there is some auto increment
    # value we de not include
    if insert.write_columns:
        statement += '('
        for col in table.column_names:
            if col == 'desc':
                statement +=f'`{col}`,'
            else:
                statement +=f'{col},'
        statement = statement[:-1] + ')'

    # Start instering values
    statement += ' VALUE ('

    for index in range(len(table.column_names)):
        if pd.isna(seq[table.column_names[index]][i]) or seq[table.column_names[index]][i] == "#N/D":
            statement += f'NULL,'
        elif table.column_types[index] == "str":
            statement += f'"{seq[table.column_names[index]][i]}",'
        elif table.column_types[index] == "int":
            statement += f'{seq[table.column_names[index]][i]},'
    statement = statement[:-1] + ");\n"
    return statement