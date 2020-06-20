
# ## Question 3
import pyodbc
import numpy as np
import pandas as pd
import datetime

from helpers import TableCreator, columnsDict


conn_string=('Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1;'
    'Server={};'
    'Database=master;'
    'uid=sa;pwd=Password123'.format('mssql:1433'))


#'35.204.21.80,1433'

conn = pyodbc.connect(conn_string)


#creates dict with tables
dataDict = TableCreator(conn)


#merges table with patient id and datetime feature
mergeList = 'condition observation medicationrequest encounter'.split()

featureDf = dataDict['[procedure]']

for table in mergeList:
    featureDf = featureDf.merge(dataDict[table], left_on=['patient_id', columnsDict['[procedure]']['time']],
                                right_on=['patient_id', columnsDict[table]['time']], how='outer',
                                suffixes=('', str('_' + table)))



#renaming for consistency
featureDf.rename(columns={'code': 'code_procedure', 'reasonReference_reference': 'reasonReference_reference_procedure'},
                 inplace=True)


#merging encounter_id columns into 1
encountersList = ['encounter_id_condition', 'encounter_id_observation', 'encounter_id_medicationrequest']

for encounter in encountersList:
    featureDf['encounter_id'] = featureDf.apply(
        lambda x: x[encounter] if pd.isnull(x['encounter_id']) else x['encounter_id'], axis=1)

    featureDf.drop(encounter, axis=1, inplace=True)


#creating a common timestamps feature
featureDf['timestamp'] = np.nan

for table in dataDict:
    featureDf['timestamp'] = featureDf.apply(
        lambda x: x[columnsDict[table]['time']] if pd.isnull(x['timestamp']) else x['timestamp'], axis=1)



featureDf.to_csv('patientFeaturesTable.csv', header=True, index=False)
