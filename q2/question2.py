# ## Question 2


import pyodbc
import pandas as pd
import datetime
from helpers import DataframeCleaner, TimeConverter, columnsDict, TableCreator



conn_string=('Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1;'
    'Server={};'
    'Database=master;'
    'uid=sa;pwd=Password123'.format('mssql'))


#'35.204.21.80,1433'

conn = pyodbc.connect(conn_string)

#create a dictionary with the tables form the sql
dataDict=TableCreator(conn)

#data preparation
for table in dataDict:
    dataDict[table][columnsDict[table]['time']] = TimeConverter(dataDict[table][columnsDict[table]['time']])
    dataDict[table][columnsDict[table]['time']] = dataDict[table][columnsDict[table]['time']].dt.strftime(
        "%Y%-m%-dT%H:%M:%S")




patientDict = {}

#reshape tables to patients x time with target column (e.g. code) as field
for table in dataDict:
    patientDict[table] = dataDict[table][
        ['patient_id', columnsDict[table]['time'], columnsDict[table]['target']]].pivot_table(
        index=['patient_id'], columns=columnsDict[table]['time'], values=columnsDict[table]['target'],
        aggfunc=lambda x: ' | '.join(x))


#concatenate the tables
patientDf = pd.concat(
    [patientDict['[procedure]'], patientDict['condition'], patientDict['encounter'], patientDict['observation'],
     patientDict['medicationrequest']], sort=False, axis=1).fillna('')

#merge fields with same datetime feature and clean up
patientDf = DataframeCleaner(patientDf)

patientDf.to_csv('patientTimelineTable.csv', header=True, index=False)
print('Success')

