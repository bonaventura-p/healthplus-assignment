import pyodbc
import pandas as pd
import datetime
import random
import seaborn as sns

def TestConnection():
    with conn:
        try:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM encounter;")
        except pyodbc.ProgrammingError as e:
            print('DB access failed: {}'.format(e))
        else:
            print('Success')


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


def TableExplorer(data_dict):
    for table in data_dict.keys():
        # print("{} has shape {}".format(table,data_dict[table].shape))
        if table != "encounter":
            print("{} has {} patients, {} encounters and {} unique ids".format(table,
                                                                               data_dict[table].patient_id.nunique(),
                                                                               data_dict[table].encounter_id.nunique(),
                                                                               data_dict[table].id.nunique()))
        else:
            print("{} has {} patients and {} unique ids".format(table, data_dict[table].patient_id.nunique(),
                                                                data_dict[table].id.nunique()))


def TimeConverter(timecol, fmt="%Y%m%dT%H:%M:%S+00:00"):
    return pd.to_datetime(timecol, format=fmt)


def TimeDelta(start, end, factor):
    return (end - start) / pd.to_timedelta(1, unit=factor)


def GroupBarPlot(table, x, y, index, val):
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
    r = lambda: random.randint(0, 255)

    fig = sns.catplot(x=x, y=y, color='#{:02x}{:02x}{:02x}'.format(r(), r(), r()),
                      kind="violin", orient='h', data=table.loc[table[y] == val])
    (fig.set_axis_labels("Hours", ""),
     fig.fig.set_figwidth(12),
     fig.fig.set_figheight(10))


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