import sys
import math
import read_database
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.pylab as plb


def check_gender_info(users):
	male_names=["noah","mason","william","ethan","michael","aiden","liam","alexander","jacob","jayde"]
	female_names=["mia","olivia","emily","elizabeth","madison","abigail","sophia","isabella","ava","emma"]
	
	male_users=0
	female_users=0
	
	for x in range (0,len(users)):
		name_is=""
		for boy in male_names:
			if boy in str(users[x][1]):
				male_users+=1
				name_is="m"
				break
		if name_is != "m":
			for girl in female_names:
				if girl in str(users[x][1]):
					female_users+=1
					name_is="f"
					break

	print "The number of male users is: %i" % male_users
	print "The number of female users is: %i" % female_users
	print "The number of total users is: %i" % len(users)
    	
	return

def check_customer_or_provider(db_connect, sql_query, all_users_list):
	provider_users=read_database.read_data(db_connect, sql_query);
	
	print "The number of users who are service providers is: %i" % len(provider_users)
	print "The number of users who are consumers is: %i" % (len(all_users_list)-len(provider_users))
	
	return
	
def check_location(db_connect, show_or_tell):  #choose either print to console (tell) or plot with matplotlib (show)
	#Note: the code can be written this way since in this dataset, each consumer makes only one request
	#		if consumers are allowed to make multiple requests (as would be desirable in reality)
	#		then we would have to use a different sql query
	
	populations=[19949502, 13131431, 9537289, 6810913, 6313158, 6034678, 5949859, 5828191, 5522942, 4684299, 4516276, 4380878, 4398762	, 4294983, 3610105, 3459146, 3211252, 2870569, 2787701, 2770738, 2697476, 2360867, 2335358, 2314554, 2277550, 2267846, 2215770, 2137406, 2064725, 2054473, 2027868, 1967066, 1953961, 1919641, 1883051, 1757912, 1707369, 1604291, 1569659, 1394624, 1341746, 1262261, 1319677, 1245764, 1240977, 1215211, 1214516, 1140300, 1134155, 1140483, 1083278, 1016603, 996544, 983429	, 961561, 955272, 939904, 926710, 902797, 895151, 877905, 862287, 864124, 852715, 850965, 839620, 831036, 827048, 820159, 815996, 802489, 793779, 741065, 732535, 724385, 704379, 705686, 712220	, 678319, 661934, 650820, 661115, 650288, 637394, 626915, 627431, 623009, 621580, 608145, 600756, 599789, 576382, 580270, 562037, 555506, 557711, 562239, 550823, 541744, 535724]
	pop_sqrt_median=[]
	msas=[]
	consumers=[]
	
	for MSA in range (1,101):
		msas.append(MSA)
		num_consumers_in_location=0
		sql_query_consumers_in_location=read_database.make_simple_sql_query('requests',[('location_id',MSA)])
		num_consumers_in_location=len(read_database.read_data(db_connect, sql_query_consumers_in_location))
		consumers.append(math.sqrt(num_consumers_in_location))
		pop_sqrt_median.append(math.sqrt(populations[MSA-1]/54083.73))
		
		if show_or_tell=="tell" or show_or_tell=="both":
			print "The number of users in MSA %i is %i" % (MSA, num_consumers_in_location)
			
	if show_or_tell=="show" or show_or_tell=="both":
		fig = plt.figure(facecolor='white')
		plt.title('Users (consumers) distributed by location', y=1.02)
		plt.xlabel('location id [Decreasing Metropolitan Statistical Area population]', fontsize=14, color='black', labelpad=10)
		plt.ylabel('sqrt(number of consumer users)', fontsize=14, color='black', labelpad=25)
		plt.plot(msas, pop_sqrt_median, color="black")
		ax = plt.subplot(111)
		ax.axis([1,100,0,32])
		ax.bar(msas, consumers, width=1, color='yellow', alpha=0.15)
		plb.savefig('users_by_location.pdf')
		#plb.show()
	
	print "The median number of users (consumers) per location is: %f" % (np.median(consumers)*np.median(consumers))
	return
	
def check_category(db_connect, show_or_tell):
	#Note: the code can be written this way since in this dataset, each consumer makes only one request
	#		if consumers are allowed to make multiple requests (as would be desirable in reality)
	#		then we would have to use a different sql query
	categories=[]
	consumers_in_categories=[]
	photography=[1,3,19,24,47,52,64,81,82,89]
	event=[4,23,28,32,33,40,42,43,44,46,51,67,72,76,83,93,94,96,99,100,103,106,108,110]
	home=[2,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,25,27,29,30,31,35,36,37,39,45,48,49,55,57,58,59,60,62,63,65,66,69,70,71,74,75,77,78,79,80,84,85,86,87,88,90,91,92,98,101,102,105,107,109,111]
	lessons=[17,22,34,38,50,53,54,56,61,68,95,113]
	health=[26,97,104,112]
	consumers_in_metacategories=[0,0,0,0,0]
	
	for cat in range (1,114):
		categories.append(cat)
		num_consumers_in_cat=0
		sql_query_consumers_in_category=read_database.make_simple_sql_query('requests',[('category_id',cat)])
		num_consumers_in_cat=len(read_database.read_data(db_connect, sql_query_consumers_in_category))
		consumers_in_categories.append(num_consumers_in_cat)
		
		if cat in photography:
			consumers_in_metacategories[0]+=num_consumers_in_cat
		elif cat in event:
			consumers_in_metacategories[1]+=num_consumers_in_cat
		elif cat in health:
			consumers_in_metacategories[4]+=num_consumers_in_cat
		elif cat in lessons:
			consumers_in_metacategories[3]+=num_consumers_in_cat
		else:
			consumers_in_metacategories[2]+=num_consumers_in_cat
			
		
		if show_or_tell=="tell" or show_or_tell=="both":
			print "The number of users in category %i is %i" % (cat, num_consumers_in_cat)
			
	if show_or_tell=="show" or show_or_tell=="both":
		fig = plt.figure(facecolor='white', figsize=(15,6))

		ax1 = plt.subplot(1,2,1)
		plt.axis([1,113,0,160])
		plt.title('Users (consumers) by category', y=1.02)
		plt.xlabel('category id', fontsize=14, color='black', labelpad=10)
		plt.ylabel('number of consumer users', fontsize=14, color='black', labelpad=15)
		plt.plot([0,113],[np.median(consumers_in_categories),np.median(consumers_in_categories)], color='black')
		plt.bar(categories, consumers_in_categories, width=1, color='yellow', alpha=0.15)
		
		ax2 = plt.subplot(1,2,2)
		plt.axis([1,6,200,2800])
		plt.title('Users (consumers) by metacategory', y=1.02)
		plt.xlabel('metacategory id', fontsize=14, color='black', labelpad=10)
		plt.ylabel('number of consumer users', fontsize=14, color='black', labelpad=15)
		plt.plot([0,6],[np.median(consumers_in_metacategories),np.median(consumers_in_metacategories)], color='black')
		plt.bar([1,2,3,4,5], consumers_in_metacategories, width=1, color='yellow', alpha=0.3)
		
		plb.savefig('users_by_category.pdf')
		#plb.show()
	
	print "The median number of users (consumers) per category is: %f" % (np.median(consumers_in_categories))
	print "The median number of users (consumers) per metacategory is: %f" % (np.median(consumers_in_metacategories))
		
	return


if __name__ == '__main__':
    
    connection=read_database.database_connect(sys.argv[1])

    if sys.argv[2]=='1':
    	sql_users_all=read_database.make_simple_sql_query('users',[])
    	users_all=read_database.read_data(connection, sql_users_all)	# This array holds user ID and email
    
    	#Check the gender of the users
    	check_gender_info(users_all)
    	
    elif sys.argv[2]=='2':
		#Check whether a user is a customer or a provider
    	sql_users_without_requests="select user_id from (select * from users left join requests on users.user_id=requests.user_id) where request_id is null;"
    	sql_users_all=read_database.make_simple_sql_query('users',[])
    	users_all=read_database.read_data(connection, sql_users_all)	# This array holds user ID and email
    	check_customer_or_provider(connection, sql_users_without_requests, users_all)
    	
    elif sys.argv[2]=='3':
    	#Check how many users live in each MSA
    	check_location(connection, "show")

    elif sys.argv[2]=='4':
    	#Check how many users made requests in each category
    	check_category(connection,"show")
    	
    else:
    	print "You entered %s" % sys.argv[2]
    	print "Please enter a valid argument for argv[2]:"
    	print "1: info about users' gender"
    	print "2: info about users' status (customer, provider)"
    	print "3: info about users' location"
    	print "4: info about users' request category"
    
    
