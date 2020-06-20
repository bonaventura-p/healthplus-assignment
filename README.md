# healthplus-assignment


### Question 1
Open the jupyter notebook in the directory q1. 
There are visualisations that summarise the information in the database tables.

### Questions 2 and 3

#### Set up an Ubuntu instance on GCP or any other public cloud

From this directory and provided you have the CLI installed and configured: 
1. Create an Ubuntu instance  (e.g. in GCP:
gcloud compute instances create healthplus-assignment \
 --image-family ubuntu-minimal-1804-lts  \
--image-project ubuntu-os-cloud \
--zone europe-west4-a )

2. SSH into the instance (*Note 1 below*)
3. Install git (e.g. sudo apt-get update && sudo apt-get install -y git)
4. git clone this directory 
5. Give permissions to **healthplus-assignment/execute.sh** (e.g. with sudo chmod +x)
6. Run the shell script **healthplus-assignment/execute.sh**


#### If you are already on an Ubuntu instance
1. git clone this directory
2. Give permissions and execute **healthplus-assignment/execute.sh**


Running the shell script will first install some required dependencies and then build and run three docker containers (i.e. the services in the docker-compose file):
1. MSSQL is to set up the MSSQL database;
2. Q2 sets up a python env to run the script for question 3 (*Note 2 below*);
3. Q3 sets up a python env to run the script for question 3 (*Note 2 below*);
4. Both Q2 and Q3 end by saving results as csv in the corresponding service folders.


### Remarks
- In Q2 the final table has fields with multiple entries (e.g. if the patient has multiple records on the same timestamp). This of course is not the way I would go about to run analyses but it was an efficient ways of creating timelines (as requested);
- In Q3, the key-value structure of the features has not been changed and the tables have only been rearranged into one by patient_id x timestamp. With a clear analysis goal in mind (e.g. training a specific model) I might have taken a different approach. This is just a neat way of putting all the information into a single table ordered by patient and time feature;
- In a production setting, I would have tried to minimise the size of the images (e.g. alpine vs ubuntu, or see *Note 2* for python);
- In a production setting, I would have also consolidated the rules for the table column names. 

<br/>
<br/>
<br/>

 



*Note 1:* SSH into instances is not a good practice. Here it's just a quick way
to run the containers on Ubuntu 

*Note 2:* With more time I would have created a slimmer image (e.g. a python 3.7 image instead of an Ubuntu one with Python installed)
