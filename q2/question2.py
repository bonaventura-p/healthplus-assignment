# ## Question 2
import os
import pyodbc
import pandas as pd
from time import sleep
import datetime
#from helpers.analytics import DataframeCleaner, TimeConverter, columnsDict, TableCreator

#    'Driver={ODBC Driver 17 for SQL Server}'

#/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1

#sleep(3000)

#drivers=[driver for driver in pyodbc.drivers() ]

conn_string=('Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1;'
    'Server={};'
    'Database=master;'
    'uid=sa;pwd=Password123'.format('35.204.21.80,1433'))

conn = pyodbc.connect(conn_string)



def TestConnection():
    with conn:
        try:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM encounter;")
        except pyodbc.ProgrammingError as e:
            print('DB access failed: {}'.format(e))
        else:
            print('Success')

TestConnection()

def TableCreator(conn):

    tables = "[procedure] encounter condition observation medicationrequest".split()

    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES"
    names = pd.read_sql(query, conn)
    # print(names)

    data_dict = {}
    for table in tables:  # can't do from names.TABLE_name because of [procedure]
        # print(table)
        query = "SELECT * FROM {};".format(table)
        #print(table)
        data_dict[table] = pd.read_sql(query, conn)

    return data_dict


def TimeConverter(timecol, fmt="%Y%m%dT%H:%M:%S+00:00"):
    return pd.to_datetime(timecol, format=fmt)

def DataframeCleaner(table):
    table = table.apply(lambda x: x.astype(str))  # not the fastest
    table = table.groupby(table.columns, axis=1).agg(lambda x: ' | '.join(x.values))

    table.replace(' | ', '', inplace=True)
    table.replace(' |  | ', '', inplace=True)

    table.sort_index(axis=1, inplace=True)

    return table

columnsDict = {'medicationrequest':{'target':'medicationCodeableConcept', 'time':'authoredOn'},
            '[procedure]':{'target':'code', 'time':'performedPeriod_start'},
            'condition':{'target':'code', 'time':'onsetDateTime'},
            'encounter':{'target':'type', 'time':'period_start'},
            'observation':{'target':'code', 'time':'effectiveDateTime'},
           }




dataDict=TableCreator(conn)


for table in dataDict:
    dataDict[table][columnsDict[table]['time']] = TimeConverter(dataDict[table][columnsDict[table]['time']])
    dataDict[table][columnsDict[table]['time']] = dataDict[table][columnsDict[table]['time']].dt.strftime(
        "%Y%-m%-dT%H:%M:%S")




patientDict = {}

for table in dataDict:
    patientDict[table] = dataDict[table][
        ['patient_id', columnsDict[table]['time'], columnsDict[table]['target']]].pivot_table(
        index=['patient_id'], columns=columnsDict[table]['time'], values=columnsDict[table]['target'],
        aggfunc=lambda x: ' | '.join(x))

patientDf = pd.concat(
    [patientDict['[procedure]'], patientDict['condition'], patientDict['encounter'], patientDict['observation'],
     patientDict['medicationrequest']], sort=False, axis=1).fillna('')

patientDf = DataframeCleaner(patientDf)

print(os.getcwd())
patientDf.to_csv('patientTimelineTable.csv', header=True, index=False)

