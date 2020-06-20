
# DataframeCleaner, TimeConverter, columnsDict, TableCreator

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


def TimeConverter(timecol, fmt="%Y%m%dT%H:%M:%S+00:00"):
    '''Converts time feature to a given format'''
    return pd.to_datetime(timecol, format=fmt)


def TimeDelta(start, end, factor):
    '''Compute time delta in a given time unit. Y/M no longer supported by pandas, so manual fix.'''
    if factor == 'Y':
        denominator = pd.to_timedelta(1, unit='days')*365
    elif factor =='M':
        denominator = pd.to_timedelta(1, unit='days')*30
    else:
        denominator = pd.to_timedelta(1, unit=factor)

    return (end - start) / denominator


def DataframeCleaner(table):
    '''merges fields with same datetime feature and sorts table by date'''
    table = table.apply(lambda x: x.astype(str))  # not the fastest
    table = table.groupby(table.columns, axis=1).agg(lambda x: ' | '.join(x.values))

    table.replace(' | ', '', inplace=True)
    table.replace(' |  | ', '', inplace=True)

    table.sort_index(axis=1, inplace=True)

    return table


#some columns name organised as dict of dicts
columnsDict = {'medicationrequest':{'target':'medicationCodeableConcept', 'time':'authoredOn'},
            '[procedure]':{'target':'code', 'time':'performedPeriod_start'},
            'condition':{'target':'code', 'time':'onsetDateTime'},
            'encounter':{'target':'type', 'time':'period_start'},
            'observation':{'target':'code', 'time':'effectiveDateTime'},
           }