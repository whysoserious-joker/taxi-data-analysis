# %%
import csv
import math
import seaborn as sns     
sns.set()
import matplotlib.pyplot as plt
%matplotlib inline

import datetime as dt
import time

import pprint

# %%

f=open("trip_data_1.csv",'r')
r=csv.reader(f)
n=0
for row in r:
    print(row)
    print(type(row))
    n+=1
    if n>5:
        break


# %% [markdown]
# In this project we will analyze a dataset which contains information about taxi rides in NYC.  The data set is quite large so getting a basic idea of what the data contains is important.  Each student should use one of the CSV files.  Answer the following questions:
# 
# - What datetime range does your data cover?  How many rows are there total?
# - What are the field names?  Give descriptions for each field.
# - Give some sample data for each field.
# - What MySQL data types / len would you need to store each of the fields?
#     int(xx), varchar(xx),date,datetime,bool, decimal(m,d)
# - What is the geographic range of your data (min/max - X/Y)?
#     Plot this (approximately on a map)
# - What is the average computed trip distance? (You should use Haversine Distance)
# - Draw a histogram of the trip distances binned anyway you see fit.
# - What are the distinct values for each field? (If applicable)
# - For other numeric types besides lat and lon, what are the min and max values?
# - Create a chart which shows the average number of passengers each hour of the day. (X axis should have 24 hours)
# - Create a new CSV file which has only one out of every thousand rows.
# - Repeat step 9 with the reduced dataset and compare the two charts.
# 
# 

# %% [markdown]
# #### 1. What datetime range does your data cover? How many rows are there total?
# 

# %%
start=time.time()
total_rows=0
d=[]
f=open("trip_data_1.csv",'r')
r=csv.reader(f)
total_rows=0
for row in r:
    if total_rows!=0:
        pickup_date=dt.datetime.strptime(row[5],"%Y-%m-%d %H:%M:%S")
        d.append(pickup_date)
    total_rows+=1
print("Total Rows: ",total_rows)
print("Datetime Range: from {a} to {b}".format(a=min(d),b=max(d)))
print("Time taken:",time.time()-start)

# %% [markdown]
# #### 2. What are the field names? Give descriptions for each field.

# %%
f=open("trip_data_1.csv",'r')
r=csv.reader(f)
for row in r:
    print("Field Names:",*row,sep='\n-')
    break

# %% [markdown]
# *Field Names and their description:*
# - **medallion**          : permits allowing an individual or company to operate a taxicab
# - **hack_license**      : driver's license
# - **vendor_id**     : company id which opereates the Taxi
# - **rate_code**        : type of fare that is applied for that ride
# - **store_and_fwd_flag** : 
# - **pickup_datetime**   : datetime when the passenger was picked up
# - **dropoff_datetime**   : datetime when the passenger was dropped off
# - **passenger_count**    : count of passengers in each ride
# - **trip_time_in_secs**  : dropoff_datetime - pickup_datetime (total time in seconds to drop the passsenger to destination)
# - **trip_distance**      : distance of the trip
# - **pickup_longitude**   : longitude coordinate of the pickup location.
# - **pickup_latitude**    : latitude coordinate of the pickup location.
# - **dropoff_longitude**  : longitude coordinate of the dropoff location.
# - **dropoff_latitude**   : latitude coordinate of the dropoff location.

# %% [markdown]
# #### 3. Give some sample data for each field.

# %%
f=open("trip_data_1.csv",'r')
r=csv.reader(f)
n=0

for row in r:
    print(*row,sep=" | ")
    n+=1
    if n>5:
        break

# %%
import pprint
f=open("trip_data_1.csv",'r')
r=csv.reader(f)

keys=next(r)
values=[]
n=0
for row in r:
    if n>0:
        values.append(row)
    n+=1
    if n>5:
        break
values
my_dict = {key: value for key, *value in zip(keys, *values)}
pprint.pp(my_dict)

# %% [markdown]
# #### 4. What MySQL data types / len would you need to store each of the fields? int(xx),      --varchar(xx),date,datetime,bool, decimal(m,d)

# %% [markdown]
# *Field Names and their datatypes:*
# - **medallion**          : VARCHAR(500)
# - **hack_license**      : VARCHAR(500)
# - **vendor_id**     : VARCHAR(500)
# - **rate_code**        : INT
# - **store_and_fwd_flag** : VARCHAR(10)
# - **pickup_datetime**   : DATETIME
# - **dropoff_datetime**   : DATETIME
# - **passenger_count**    : INT
# - **trip_time_in_secs**  : INT
# - **trip_distance**      : decimal(6,2)
# - **pickup_longitude**   : decimal(10,6)
# - **pickup_latitude**    : decimal(10,6)
# - **dropoff_longitude**  : decimal(10,6)
# - **dropoff_latitude**   : decimal(10,6)

# %% [markdown]
# #### 5. What is the geographic range of your data (min/max - X/Y)? Plot this (approximately on a map)

# %%
# lets have the rows with correct lats and longs in a variable
f=open("trip_data_1.csv",'r')
r=csv.reader(f)
n=0


max_pickup_lat_value = float('-inf')
max_dropoff_lat_value = float('-inf')

max_pickup_long_value = float('-inf')
max_dropoff_long_value = float('-inf')

min_pickup_long_value = float('inf')
min_dropoff_long_value = float('inf')

min_pickup_lat_value = float('inf')
min_dropoff_lat_value = float('inf')

incorrect_values=0
blank=0

from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of Earth in kilometers (you can use 6371.0 km for distance in km)
    radius = 3958.8

    # Calculate the distance
    distance = radius * c

    return distance

for row in r:
    if n!=0:
        try:
            long1=float(row[10])# pickup_longitude
            lat1=float(row[11])# pickup_latitude
            long2=float(row[12])# dropoff_longitude
            lat2=float(row[13])# dropoff_latitude
            
            h_distance=math.floor(haversine_distance(lat1,long1,lat2,long2))
            act_distance=math.floor(float(row[9]))
            
            
            if ((round(abs(long1)) not in range(1,180)) or (round(abs(long2)) not in range(1,180)) or 
                (round(abs(lat1)) not in range(1,90)) or (round(abs(lat2)) not in range(1,90))):
                incorrect_values+=1
            
            else:
                
                if (((act_distance>0) and (abs(h_distance-act_distance) <2)) and 
                    ((int(lat1) in range(24,47)) and (int(lat2) in range(24,47)) and 
                    (int(long1) in range(-121,-69)) and (int(long2) in range(-121,-69)))):
                                
                    pickup_long_values=long1
                    pickup_lat_values=lat1
                    dropoff_long_values=long2
                    dropoff_lat_values=lat2

                    max_pickup_lat_value=max(pickup_lat_values,max_pickup_lat_value)
                    max_dropoff_lat_value=max(dropoff_lat_values,max_dropoff_lat_value)

                    min_pickup_lat_value=min(pickup_lat_values,min_pickup_lat_value)
                    min_dropoff_lat_value=min(dropoff_lat_values,min_dropoff_lat_value)


                    max_pickup_long_value=max(pickup_long_values,max_pickup_long_value)
                    max_dropoff_long_value=max(dropoff_long_values,max_dropoff_long_value)

                    min_pickup_long_value=min(pickup_long_values,min_pickup_long_value)
                    min_dropoff_long_value=min(dropoff_long_values,min_dropoff_long_value)
                  
        except Exception as e:
            blank+=1
            
    n+=1

print("Latitude Range: {} to {}".format(min(min_pickup_lat_value, min_dropoff_lat_value), max(max_pickup_lat_value, max_dropoff_lat_value)))
print("Longitude Range: {} to {}".format(min(min_pickup_long_value, min_dropoff_long_value), max(max_pickup_long_value, max_dropoff_long_value)))
    



# %% [markdown]
# #### 6. What is the average computed trip distance? (You should use Haversine Distance)

# %%
f=open("trip_data_1.csv",'r')
r=csv.reader(f)
h_distance=[]
actual_distance=[]
n=0
for row in r:
    if (n!=0) and (row[10]!='') and (row[11]!='') and (row[12]!='') and (row[13]!=''):
        # to exclude headers and skip blanks for lat and lon values 
        h_distance.append(haversine_distance(float(row[11]),float(row[10]),float(row[13]),float(row[12])))
        actual_distance.append(float(row[9]))
    n+=1

print("Average computed trip distance using haversine_distance: {} miles".format(round(sum(h_distance)/len(h_distance),0)))
print("Average computed trip distance using trip_distance column: {} miles".format(round(sum(actual_distance)/len(actual_distance),0)))

# %%
f=open("trip_data_1.csv",'r')
r=csv.reader(f)

n=0

incorrect_values=0
correct_values=0
blanks=0

for row in r:
    if n!=0:
        try:
            long1=float(row[10])# pickup_longitude
            lat1=float(row[11])# pickup_latitude
            long2=float(row[12])# dropoff_longitude
            lat2=float(row[13])# dropoff_latitude
            
            if ((round(abs(long1)) not in range(1,180)) or (round(abs(long2)) not in range(1,180)) or 
                (round(abs(lat1)) not in range(1,90)) or (round(abs(lat2)) not in range(1,90))):
                incorrect_values+=1
        
            else:
                correct_values+=1
                
        except Exception as e:
            blanks+=1
            
    n+=1

print("Total rows : {}".format(total_rows))
print("Rows with incorrect_values:",incorrect_values)
print("Rows with blanks:",blanks)
print("Total rows with incorrect coordinates : {} ".format(incorrect_values+blanks))
print("Percentage of incorrect values : ",round(((incorrect_values+blanks)/total_rows)*100,0),"%")

# %%

f=open("trip_data_1.csv",'r')
r=csv.reader(f)
n=0

incorrect_values=0
correct_values=0
blank=0

h_distance=[]
actual_distance=[]


for row in r:
    if n!=0:
        try:
            long1=float(row[10])# pickup_longitude
            lat1=float(row[11])# pickup_latitude
            long2=float(row[12])# dropoff_longitude
            lat2=float(row[13])# dropoff_latitude
            
            if ((round(abs(long1)) not in range(1,180)) or (round(abs(long2)) not in range(1,180)) or 
                (round(abs(lat1)) not in range(1,90)) or (round(abs(lat2)) not in range(1,90))):
                incorrect_values+=1
        
            else:
                correct_values+=1
                h_distance.append(haversine_distance(float(row[11]),float(row[10]),float(row[13]),float(row[12])))
                actual_distance.append(float(row[9]))
                
        except Exception as e:
            blank+=1
            
    n+=1
print("Total_rows : {}".format(total_rows))
print("Rows with incorrect coordinates : {} ".format(incorrect_values+blank))
print("Percentage of incorrect values : ",round(((incorrect_values+blank)/total_rows)*100,0),"%")
print("Average computed trip distance using haversine_distance: {} miles".format(round(sum(h_distance)/len(h_distance),2)))
print("Average computed trip distance using trip_distance column: {} miles".format(round(sum(actual_distance)/len(actual_distance),2)))


# %% [markdown]
# #### 7. Draw a histogram of the trip distances binned anyway you see fit.
# 

# %%
import plotly.express as px

f=open("trip_data_1.csv",'r')
r=csv.reader(f)
td=[]
n=0
for row in r:
    if n!=0:
        td.append(float(row[9]))
    n+=1

# %%
px.histogram(td,
                   nbins=100, 
                   title="Trip Distance", 
                   labels={'value': 'Distance (miles)', 'count': 'Frequency'}).show()



# %%
sns.histplot(td,kde=False,bins=30,binrange=(1,30))

# %% [markdown]
# #### 8. What are the distinct values for each field? (If applicable)

# %%

f=open("trip_data_1.csv",'r')
r=csv.reader(f)
n=0
medallion=[]
hack_license=[]
vendors=[]
rate_code=[]
store_and_fwd_flag=[]
passenger_count=[]

for row in r:
    if n!=0:
        medallion.append(row[0])   
        hack_license.append(row[1])
        vendors.append(row[2])
        rate_code.append(row[3])
        store_and_fwd_flag.append(row[4])
        passenger_count.append(row[7])
    n+=1


        



# %%
print("Unique Vendors:",set(vendors))
print("Unique rate_code:",set(rate_code))
print("Unique store_and_fwd_flag:",set(store_and_fwd_flag))
print("Unique passenger_count:",set(passenger_count))

# %% [markdown]
# #### 9. For other numeric types besides lat and lon, what are the min and max values?

# %%
import csv
f=open("trip_data_1.csv",'r')
r=csv.reader(f)

n=0

pc_max=float('-inf')
pc_min=float('inf')

tt_max=float('-inf')
tt_min=float('inf')

td_max=float('-inf')
td_min=float('inf')

n=0
for row in r:
    
    if n!=0:
        if (float(row[7]) in range(1,20)) and (float(row[8])>0) and (float(row[9])>0):
            pc=float(row[7])
            pc_max=max(pc_max,pc)
            pc_min=min(pc_min,pc)

            tt=float(row[8])
            tt_max=max(tt_max,tt)
            tt_min=min(tt_min,tt)

            td=float(row[9])
            td_max=max(td_max,td)
            td_min=min(td_min,td)
    
    n+=1


# %%
print("passenger_count_max | passenger_count_min | triptime_mx | triptime_min | tripdistance_mx | tripdistance_min")
print(pc_max,"                |",pc_min,"                |",tt_max,"    |",tt_min,"         |",td_max,"          |",td_min)

# %% [markdown]
# #### 10. Create a chart which shows the average number of passengers each hour of the day. (X axis should have 24 hours)

# %%
import datetime as dt
f=open("trip_data_1.csv",'r')
r=csv.reader(f)

pph={}
n=0

for row in r:
    if n!=0 and (float(row[7]) in range(1,10)):
        pickup_date=dt.datetime.strptime(row[5],"%Y-%m-%d %H:%M:%S")
        hr=pickup_date.hour
        if hr in pph:
            pph[hr]['Passenger_Count']+=float(row[7])
            pph[hr]['trip_count']+=1
        else:
            pph[hr]={}
            pph[hr]['Passenger_Count']=float(row[7])
            pph[hr]['trip_count']=1
    n+=1

        
pph=dict(sorted(pph.items(),key=lambda item:item[0],reverse=True))
print(pph)

# %%
pprint.pp(pph)

# %%
apph={}
for k,v in pph.items():
    apph[k]=v['Passenger_Count']/v['trip_count']
apph
        

# %%
import plotly.express as px
import plotly.graph_objects as go

fig = px.line(x=apph.keys(),
             y=apph.values(),
                   title="Average passengers per each hour | Original Dataset",
              
             )
fig.update_layout(
   xaxis = dict(
      tickmode = 'linear'
   ),
    xaxis_title="Hour",
    yaxis_title="Passenger_count"
)
fig.show()

# %%
sns.lineplot(x=apph.keys(),
             y=apph.values()).set_title("Average passengers per each hour | Original Dataset")


# %% [markdown]
# #### 11. Create a new CSV file which has only one out of every thousand rows.

# %%
import csv
import numpy as np

# get random numbers from each 1000 numbers
rand_idx=[]
n=0
x=0
y=1000
while(n<total_rows):
    rand_idx.append(np.random.randint(x,y))
    x=y+1
    y+=1000
    n+=1000
print("Sample Indexes for every 1000 rows")
rand_idx[0:10]

# %%
n=0

f=open("trip_data_1.csv",'r')
r=csv.reader(f)

f2=open("one_outof_1000.csv",'w')
f2.write('')
f2.close()
f2=open('one_outof_1000.csv','a')
w=csv.writer(f2,delimiter=',',lineterminator='\n')


for row in r:
    if n in rand_idx:
        w.writerow(row)
    n+=1

f.close()
f2.close()

# %% [markdown]
# #### 12. Repeat step 9 with the reduced dataset and compare the two charts.

# %%
import csv
f=open("one_outof_1000.csv",'r')
r=csv.reader(f)

n=0

pc_max=float('-inf')
pc_min=float('inf')

tt_max=float('-inf')
tt_min=float('inf')

td_max=float('-inf')
td_min=float('inf')

n=0
for row in r:
    
    if n!=0:
        if (float(row[7]) in range(1,20)) and (float(row[8])>0) and (float(row[9])>0):
            pc=float(row[7])
            pc_max=max(pc_max,pc)
            pc_min=min(pc_min,pc)

            tt=float(row[8])
            tt_max=max(tt_max,tt)
            tt_min=min(tt_min,tt)

            td=float(row[9])
            td_max=max(td_max,td)
            td_min=min(td_min,td)
    
    n+=1

print("passenger_count_max | passenger_count_min | triptime_mx | triptime_min | tripdistance_mx | tripdistance_min")
print(pc_max,"                |",pc_min,"                |",tt_max,"     |",tt_min,"         |",td_max,"          |",td_min)

# other numeric columns : passenger_count,trip_time_in_secs,trip_distance


# %%
# average passengers per each hour
f=open("one_outof_1000.csv",'r')
r=csv.reader(f)

pph={}
n=0

for row in r:
    if n!=0 and (float(row[7]) in range(1,10)):
        pickup_date=dt.datetime.strptime(row[5],"%Y-%m-%d %H:%M:%S")
        hr=pickup_date.hour
        if hr in pph:
            pph[hr]['Passenger_Count']+=float(row[7])
            pph[hr]['trip_count']+=1
        else:
            pph[hr]={}
            pph[hr]['Passenger_Count']=float(row[7])
            pph[hr]['trip_count']=1
    n+=1

        
pph=dict(sorted(pph.items(),key=lambda item:item[0],reverse=True))

apph_reduced={}
for k,v in pph.items():
    apph_reduced[k]=v['Passenger_Count']/v['trip_count']


    
fig = px.line(x=apph_reduced.keys(),
             y=apph_reduced.values(),
                   title="Average passengers per each hour | Reduced Dataset",
             )
fig.update_layout(
   xaxis = dict(
      tickmode = 'linear'
   ),
    xaxis_title="Hour",
    yaxis_title="Passenger_count"
)
fig.show()

# %%
sns.lineplot(x=apph_reduced.keys(),
             y=apph_reduced.values()).set_title("Average passengers per each hour | Reduced Dataset")

# %%
fig = px.line(x=apph.keys(),
             y=apph.values(),
                   title="Average passengers per each hour | Original Dataset",
              
             )
fig.update_layout(
   xaxis = dict(
      tickmode = 'linear'
   ),
    xaxis_title="Hour",
    yaxis_title="Passenger_count"
)
fig.show()

fig = px.line(x=apph_reduced.keys(),
             y=apph_reduced.values(),
                   title="Average passengers per each hour | Reduced Dataset",
             )
fig.update_layout(
   xaxis = dict(
      tickmode = 'linear'
   )
)
fig.show()

# %%
sns.lineplot(x=apph.keys(),
             y=apph.values())

sns.lineplot(x=apph_reduced.keys(),
             y=apph_reduced.values()).set_title("Average passengers per each hour | Original vs Reduced Dataset")

# %%
f=open("one_outof_1000.csv",'r')
r=csv.reader(f)
td_reduced=[]
n=0
for row in r:
    if n!=0:
        td_reduced.append(float(row[9]))
    n+=1

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
f, axes = plt.subplots(1, 2)

sns.histplot(td,kde=False,bins=30,binrange=(1,30),ax=axes[0]).set(title="TripDistance Freq plot | Original Dataset")
sns.histplot(td_reduced,kde=False,bins=30,binrange=(1,30),ax=axes[1]).set(title="TripDistance Freq plot | Reduced Dataset")
plt.show()


