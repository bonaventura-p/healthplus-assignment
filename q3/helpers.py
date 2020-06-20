
# columnsDict, TableCreator

import pandas as pd
import datetime


def TableCreator(conn):
    '''query the database using conn and retrieve table names. then retrieve tables. '''

    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES"
    names = pd.read_sql(query, conn)

    tables = "[procedure] encounter condition observation medicationrequest".split()

    data_dict = {}
    for table in tables:  # can't do from names.TABLE_name because of procedure is a reserved keyword in SQL
        query = "SELECT * FROM {};".format(table)
        print(table)
        data_dict[table] = pd.read_sql(query, conn)

    return data_dict



#some columns name organised as dict of dicts
columnsDict = {'medicationrequest':{'target':'medicationCodeableConcept', 'time':'authoredOn'},
            '[procedure]':{'target':'code', 'time':'performedPeriod_start'},
            'condition':{'target':'code', 'time':'onsetDateTime'},
            'encounter':{'target':'type', 'time':'period_start'},
            'observation':{'target':'code', 'time':'effectiveDateTime'},
           }