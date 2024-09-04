from ...model.insert_conf import InsertConf

def get_pac_text(insert: InsertConf) -> str:
    if insert.semester == "":
        return ("AÑO", f"20{insert.year}")
    else:
        return("PERIODO", f'20{insert.year}-{insert.semester}S')