

#TimeConverter, TimeDelta, TableCreator, GroupBarPlot, CatPlotter, columnsDict

import pandas as pd
import datetime
import random
import seaborn as sns
import matplotlib.pyplot as plt


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


def GroupBarPlot(table, x, y, index, val):
    '''Creates barplot of y over x with random fill color. First filters the table by a val of index and groups by mean over x'''

    # lambda else not callable
    r = lambda: random.randint(0, 255)

    groupDf = table.loc[table[index] == val, [x, y]].groupby(x, as_index=False).mean()

    fig = sns.catplot(x=x, y=y, kind='bar', color='#{:02x}{:02x}{:02x}'.format(r(), r(), r()),
                      data=groupDf)
    plt.xticks(rotation=90)
    (fig.set_axis_labels("Year", val),
     fig.fig.set_figwidth(15),
     fig.fig.set_figheight(8))


def CatPlotter(x, y, val, table):
    '''Violin boxplot with random fill color of y over x for a given val of y'''
    r = lambda: random.randint(0, 255)

    fig = sns.catplot(x=x, y=y, color='#{:02x}{:02x}{:02x}'.format(r(), r(), r()),
                      kind="violin", orient='h', data=table.loc[table[y] == val])
    (fig.set_axis_labels("Hours", ""),
     fig.fig.set_figwidth(12),
     fig.fig.set_figheight(10))


#some columns name organised as dict of dicts
columnsDict = {'medicationrequest':{'target':'medicationCodeableConcept', 'time':'authoredOn'},
            '[procedure]':{'target':'code', 'time':'performedPeriod_start'},
            'condition':{'target':'code', 'time':'onsetDateTime'},
            'encounter':{'target':'type', 'time':'period_start'},
            'observation':{'target':'code', 'time':'effectiveDateTime'},
           }