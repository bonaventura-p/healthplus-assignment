
# ## Question 3
import pyodbc
import numpy as np
import pandas as pd


#from helpers.analytics import TableCreator
conn_string=('Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1;'
    'Server={};'
    'Database=master;'
    'uid=sa;pwd=Password123'.format('35.204.21.80,1433'))

conn = pyodbc.connect(conn_string)

columnsDict = {'medicationrequest':{'target':'medicationCodeableConcept', 'time':'authoredOn'},
            '[procedure]':{'target':'code', 'time':'performedPeriod_start'},
            'condition':{'target':'code', 'time':'onsetDateTime'},
            'encounter':{'target':'type', 'time':'period_start'},
            'observation':{'target':'code', 'time':'effectiveDateTime'},
           }



def TableCreator(conn):

    tables = "[procedure] encounter condition observation medicationrequest".split()

    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES"
    names = pd.read_sql(query, conn)
    # print(names)

    data_dict = {}
    for table in tables:  # can't do from names.TABLE_name because of [procedure]
        # print(table)
        query = "SELECT * FROM {};".format(table)
        print(table)
        data_dict[table] = pd.read_sql(query, conn)

    return data_dict



dataDict = TableCreator(conn)


mergeList = 'condition observation medicationrequest encounter'.split()

featureDf = dataDict['[procedure]']

for table in mergeList:
    featureDf = featureDf.merge(dataDict[table], left_on=['patient_id', columnsDict['[procedure]']['time']],
                                right_on=['patient_id', columnsDict[table]['time']], how='outer',
                                suffixes=('', str('_' + table)))

# In[21]:


featureDf.rename(columns={'code': 'code_procedure', 'reasonReference_reference': 'reasonReference_reference_procedure'},
                 inplace=True)

# In[ ]:


encountersList = ['encounter_id_condition', 'encounter_id_observation', 'encounter_id_medicationrequest']

for encounter in encountersList:
    featureDf['encounter_id'] = featureDf.apply(
        lambda x: x[encounter] if pd.isnull(x['encounter_id']) else x['encounter_id'], axis=1)

    featureDf.drop(encounter, axis=1, inplace=True)


featureDf['timestamp'] = np.nan

for table in dataDict:
    featureDf['timestamp'] = featureDf.apply(
        lambda x: x[columnsDict[table]['time']] if pd.isnull(x['timestamp']) else x['timestamp'], axis=1)



featureDf.to_csv('patientFeaturesTable.csv', header=True, index=False)
