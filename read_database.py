import sys
import sqlite3
import time
import datetime

def database_connect(db_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	
	return c	# db_name provided as argument when running script

def make_simple_sql_query(table_name, list_of_queries):	#queries are entered as tuples: (attribute, value)
	if len(list_of_queries)==0:
		sql = "SELECT * FROM "+table_name
	elif len(list_of_queries)==1:
		sql = "SELECT * FROM "+table_name+" WHERE "+list_of_queries[0][0]+" = "+str(list_of_queries[0][1])
	else:
		sql = "SELECT * FROM "+table_name+" WHERE "
		for query in list_of_queries[:-1]:
			sql=sql+query[0]+" = "+str(query[1])+" AND "
			sql=sql+list_of_queries[-1][0]+" = "+str(list_of_queries[-1][1])
				
	return sql	# query over any of the attributes in one relation

def read_data(db_con, sql_query):
	result=[]
	for row in db_con.execute(sql_query):
		result.append(row)
        
	return result
    
    
if __name__ == '__main__':
	pass
	  