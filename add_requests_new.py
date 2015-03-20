import sys
import math
import sqlite3
import datetime
import read_database
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import matplotlib.dates as dts
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import pandas as pds

    
if __name__=='__main__':
    connection=read_database.database_connect(sys.argv[1])
    
    if sys.argv[2]=='1':
        photography=[1,3,19,24,47,52,64,81,82,89]
        event=[4,23,28,32,33,40,42,43,44,46,51,67,72,76,83,93,94,96,99,100,103,106,108,110]
        home=[2,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,25,27,29,30,31,35,36,37,39,45,48,49,55,57,58,59,60,62,63,65,66,69,70,71,74,75,77,78,79,80,84,85,86,87,88,90,91,92,98,101,102,105,107,109,111]
        lessons=[17,22,34,38,50,53,54,56,61,68,95,113]
        health=[26,97,104,112]
        
        sql_get_request_id="select request_id from requests;"
        sql_get_user_id="select user_id from requests;"
        sql_get_category_id="select category_id from requests;"
        sql_get_location_id="select location_id from requests;"
        sql_get_creation_time="select creation_time from requests;"
        
        req_id=read_database.read_data(connection,sql_get_request_id)
        usr_id=read_database.read_data(connection,sql_get_user_id)
        cat_id=read_database.read_data(connection,sql_get_category_id)
        loc_id=read_database.read_data(connection,sql_get_location_id)
        crt_ti=read_database.read_data(connection,sql_get_creation_time)
        
        meta_categories=[]
        for cat in cat_id:
            if cat[0] in photography:
                meta_categories.append(1)
            elif cat[0] in event:
                meta_categories.append(2)
            elif cat[0] in lessons:
                meta_categories.append(4)
            elif cat[0] in health:
                meta_categories.append(5)
            else:
                meta_categories.append(3)
                
        db_connection = sqlite3.connect(sys.argv[1])
        ctn = db_connection.cursor()
        
        sql_add_new_requests_table="CREATE TABLE requests_new (request_id INTEGER NOT NULL, user_id INTEGER NOT NULL, category_id INTEGER NOT NULL, meta_category_id INTEGER NOT NULL, location_id INTEGER NOT NULL, creation_time DATETIME NOT NULL, PRIMARY KEY (request_id), FOREIGN KEY(user_id) REFERENCES users (user_id), FOREIGN KEY(category_id) REFERENCES categories (category_id), FOREIGN KEY(location_id) REFERENCES locations (location_id));"
        ctn.execute(sql_add_new_requests_table)
        
        for x in range (0,len(meta_categories)):
            sql_add_value="insert into requests_new (request_id, user_id, category_id, meta_category_id, location_id, creation_time) values ('%i','%i','%i','%i','%i','%s');" % (req_id[x][0],usr_id[x][0],cat_id[x][0],meta_categories[x],loc_id[x][0],str(crt_ti[x][0]))
            #print sql_add_value
            ctn.execute(sql_add_value)
            db_connection.commit()
