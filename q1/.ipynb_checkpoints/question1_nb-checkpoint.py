
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
from wordcloud import WordCloud

from helpers.analytics import TimeConverter, TimeDelta, TableCreator, GroupBarPlot, CatPlotter, columnsDict


# comments:
# column names inconsistent




sns.set(style="darkgrid")
plt.rcParams["figure.figsize"] = (18,8)


conn = pyodbc.connect(
    'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
    'Server=localhost;'
    'Database=master;'
    'uid=sa;pwd=Password123')



dataDict = TableCreator(conn)


## Data Preparation
for table in dataDict:
    
    dataDict[table][columnsDict[table]['time']] = TimeConverter(dataDict[table][columnsDict[table]['time']])
    



# In[11]:

dataDict['condition']['clinicalStatusDuration'] = TimeDelta(start=dataDict['condition']['onsetDateTime'],
                                                           end=datetime.datetime.now(),factor='Y')


# In[12]:

dataDict['encounter']['period_end'] = TimeConverter(dataDict['encounter']['period_end'])
dataDict['[procedure]']['performedPeriod_end'] = TimeConverter(dataDict['[procedure]']['performedPeriod_end'])


# In[13]:

dataDict['encounter']['encounterDuration'] = TimeDelta(end=dataDict['encounter']['period_end'],
                                              start=dataDict['encounter']['period_start'],factor='H')



# In[14]:

dataDict['observation']['value']=dataDict['observation']['value'].astype('float')



# In[15]:

dataDict['observation']['year']=dataDict['observation']['effectiveDateTime'].dt.year



# In[16]:


dataDict['[procedure]']['year']=dataDict['[procedure]']['performedPeriod_end'].dt.year
dataDict['[procedure]']['month']=dataDict['[procedure]']['performedPeriod_end'].dt.month





# ### Condition table

# In[17]:


fig=sns.catplot(x="clinicalStatus", y="clinicalStatusDuration", hue="code", data=dataDict['condition'], legend=False)
(fig.set_axis_labels("Clinical Status", "Duration"),fig.fig.set_figwidth(12),
    fig.fig.set_figheight(10))


# ### Encounter table

# In[19]:


[CatPlotter(y='class', x="encounterDuration", val=val, table=dataDict['encounter']) for val in dataDict['encounter']['class'].unique()]



# ### Observation table

# In[20]:

print(dataDict['observation']['code'].value_counts()[:5])


# In[22]:


#could do for any, but here just four columns

for val in ['Body Height','Body Weight','Body Mass Index', 'Hemoglobin A1c/Hemoglobin.total in Blood']:

    GroupBarPlot(dataDict['observation'],x='year',y='value',index='code',val=val)


# ### Medication request table

# In[23]:


wordcloud = WordCloud(width = 1000, height = 1000, 
            background_color ='white', 
            min_font_size = 10).generate(' '.join(dataDict['medicationrequest']['medicationCodeableConcept'])) 

# plot the WordCloud image                        
plt.figure(figsize = (10, 10), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 

plt.show() 


# ### Procedure table

# In[24]:


groupedProcedureDf = dataDict['[procedure]'][['reasonReference_display','year','month']].groupby(['year','month'], as_index=False).count()
groupedProcedureDf = groupedProcedureDf.pivot("month", "year", "reasonReference_display")


# In[27]:


ax = sns.heatmap(groupedProcedureDf,cmap='inferno')
(ax.set_xlabel("Year"),ax.set_ylabel("Month"),
 ax.set_title('Frequency of procedures'))  







