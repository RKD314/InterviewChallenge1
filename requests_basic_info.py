import sys
import math
import datetime
import read_database
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import matplotlib.dates as dts
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

def convert_time_to_datetime(time_string):
    (year,month,daytime)=time_string.split("-")
    (day,time)=daytime.split(" ")
    (hour,min,secdec)=time.split(":")
    
    microsec=float(secdec)%1.0
    sec=float(secdec)-microsec
    
    microsec=microsec*1000000.
    
    converted_time=datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), int(microsec))
    
    return converted_time

def requests_vs_time_all_mc(plot_on_or_off):
    sql_requests_time="select creation_time from requests;"
    requests_time=read_database.read_data(connection, sql_requests_time)
        
    requests_converted_time=[]
    for timedate in requests_time:
        requests_converted_time.append(convert_time_to_datetime(str(timedate[0])))
        
    if plot_on_or_off.lower()=='on':
        hfmt = dts.DateFormatter('%m/%d')
        fig = plt.figure(facecolor='white',figsize=(15,6))
        
        ax1 = plt.subplot(1,2,1)
        plt.title('Requests over time (daily)', y=1.02)
        plt.xlabel('request creation time [day]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of requests', fontsize=14, color='black', labelpad=15)
        plt.axis([dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0)),0,600])
        plt.hist(dts.date2num(requests_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=64, normed=0, facecolor='green', alpha=0.15)
        ax1.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU, SA)))
        ax1.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)
        
        ax2 = plt.subplot(1,2,2)
        plt.title('Requests over time (weekly)', y=1.02)
        plt.xlabel('request creation time [week]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of requests', fontsize=14, color='black', labelpad=15)
        plt.axis([dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0)),0,3200])
        plt.hist(dts.date2num(requests_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=9, normed=0, facecolor='green', alpha=0.15)
        ax2.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU)))
        ax2.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)        
        
        plb.savefig('requests_over_time_daily_and_weekly.pdf')
        #plb.show()
        
    print "The first recorded request took place at %s" % min(requests_converted_time)
    print "The last recorded request took place at %s" % max(requests_converted_time)
    print "There were %i requests total" % len(requests_converted_time)
    
    return

def requests_vs_time_given_mc(plot_on_or_off, mcid):
    sql_requests_time="select creation_time from requests_new where meta_category_id=%s;" % mcid
    requests_time=read_database.read_data(connection, sql_requests_time)
        
    requests_converted_time=[]
    for timedate in requests_time:
        requests_converted_time.append(convert_time_to_datetime(str(timedate[0])))
        
    if plot_on_or_off.lower()=="on":
        hfmt = dts.DateFormatter('%m/%d')
        fig = plt.figure(facecolor='white',figsize=(15,6))
        
        ax1 = plt.subplot(1,2,1)
        plt.title('Requests over time (daily), meta-category %s' % mcid, y=1.02)
        plt.xlabel('request creation time [day]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of requests', fontsize=14, color='black', labelpad=15)
        plt.xlim((dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0))))
        plt.hist(dts.date2num(requests_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=64, normed=0, facecolor='green', alpha=0.15)
        ax1.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU, SA)))
        ax1.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)
        
        ax2 = plt.subplot(1,2,2)
        plt.title('Requests over time (weekly), meta-category %s' % mcid, y=1.02)
        plt.xlabel('request creation time [week]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of requests', fontsize=14, color='black', labelpad=15)
        plt.xlim((dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0))))
        plt.hist(dts.date2num(requests_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=9, normed=0, facecolor='green', alpha=0.15)
        ax2.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU)))
        ax2.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)        
        
        plb.savefig('requests_over_time_daily_and_weekly_metcat%s.pdf' % mcid)
        #plb.show()
        
    print "The first recorded request took place at %s" % min(requests_converted_time)
    print "The last recorded request took place at %s" % max(requests_converted_time)
    print "There were %i requests total" % len(requests_converted_time)
    
    return

def requests_to_invites_all_mc_date_range(plot_on_or_off,date1,date2,ret_list):
    sql_requestid_invites="select requests.request_id from requests join invites on requests.request_id=invites.request_id where creation_time >= date('%s') and creation_time <= date('%s');" % (date1,date2)
    requestsid_invites=read_database.read_data(connection, sql_requestid_invites)
    
    sql_requestid_noinvite="select 0 from requests left join invites on requests.request_id=invites.request_id where invite_id is null and creation_time >= date('%s') and creation_time <= date('%s');" % (date1,date2)
      
    dict_request_invites={}
    for req in requestsid_invites:
        if req in dict_request_invites:
            dict_request_invites[req]+=1
        else:
            dict_request_invites.setdefault(req,1)
        
    num_invites_per_request=[]
    map(lambda z: num_invites_per_request.append(z[0]),read_database.read_data(connection, sql_requestid_noinvite))
    for requ in dict_request_invites:
        num_invites_per_request.append(dict_request_invites[requ])
        
    if plot_on_or_off.lower()=='on':
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Requests to Invites, [%s, %s]' % (date1,date2))
        plt.xlabel('number of invites for a given request', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of requests', fontsize=14, color='black', labelpad=15)
        plt.hist(num_invites_per_request,range=(0,15),bins=15,normed=0,facecolor='green',alpha=0.2)
        plb.savefig('requests_to_invites_counts_%s_to_%s.pdf' % (date1,date2))
        #plb.show()
        
    if ret_list==1:
        return num_invites_per_request
    else:
        return

def requests_to_invites_given_mc_date_range(plot_on_or_off,date1,date2,mcid,ret_list):
    sql_requestid_invites="select requests_new.request_id from requests_new join invites on requests_new.request_id=invites.request_id where creation_time >= date('%s') and creation_time <= date('%s') and meta_category_id=%s;" % (date1,date2,mcid)
    requestsid_invites=read_database.read_data(connection, sql_requestid_invites)
    
    sql_requestid_noinvite="select 0 from requests_new left join invites on requests_new.request_id=invites.request_id where invite_id is null and creation_time >= date('%s') and creation_time <= date('%s') and meta_category_id=%s;" % (date1,date2,mcid)
    
    dict_request_invites={}
    for req in requestsid_invites:
        if req in dict_request_invites:
            dict_request_invites[req]+=1
        else:
            dict_request_invites.setdefault(req,1)
        
    num_invites_per_request=[]
    map(lambda z: num_invites_per_request.append(z[0]),read_database.read_data(connection, sql_requestid_noinvite))
    for requ in dict_request_invites:
        num_invites_per_request.append(dict_request_invites[requ])
        
    if plot_on_or_off.lower()=='on':
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Requests to Invites, [%s, %s], meta-category %s' % (date1,date2,mcid))
        plt.xlabel('number of invites for a given request', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of requests', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,1.0))
        plt.hist(num_invites_per_request,range=(0,15),bins=15,normed=1,facecolor='green',alpha=0.2)
        plb.savefig('requests_to_invites_counts_%s_to_%s_metcat%s.pdf' % (date1,date2,mcid))
        #plb.show()
        
    if ret_list==1:
        return num_invites_per_request
    else:
        return

def locations_per_requesttime_all_mc_date_range(date1,date2):
    sql_locationid_requests="select location_id from requests where creation_time >= date('%s') and creation_time <= date('%s');" % (date1,date2)
    locationid_requests=read_database.read_data(connection, sql_locationid_requests)
    return len(set(locationid_requests))

def locations_per_requesttime_all_mc_date_range_pop(date1,date2,pop):
    if pop=='low':
        sql_locationid_requests="select location_id from requests where creation_time >= date('%s') and creation_time <= date('%s') and location_id>=53 and location_id<=100;" % (date1,date2)
    elif pop=='med':
        sql_locationid_requests="select location_id from requests where creation_time >= date('%s') and creation_time <= date('%s') and location_id>=10 and location_id<=52;" % (date1,date2)
    else:
        sql_locationid_requests="select location_id from requests where creation_time >= date('%s') and creation_time <= date('%s') and location_id>=1 and location_id<=9;" % (date1,date2)
    locationid_requests=read_database.read_data(connection, sql_locationid_requests)
    return len(set(locationid_requests))

def categories_per_requesttime_all_mc_date_range(date1,date2):
    if date1==date2:
        sql_categoryid_requests="select category_id from requests where date(creation_time) = '%s';" % date1
    else:
        sql_categoryid_requests="select category_id from requests where creation_time >= date('%s') and creation_time <= date('%s');" % (date1,date2)
    categoryid_requests=read_database.read_data(connection, sql_categoryid_requests)
    return len(set(categoryid_requests))

def plot_mean_invites_per_week_bins(mcid):
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    #All metacategories
    if mcid.lower()=='all':
        linecolr=colors[0]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            val=np.mean(requests_to_invites_all_mc_date_range("off",week_starts[week],week_ends[week],1))
            weekly_rates.append(val)
    #Given metacategory
    else:
        linecolr=colors[int(mcid)]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            val=np.mean(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],mcid,1))
            weekly_rates.append(val)
    #print weekly_rates
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Mean Number of Invitations Sent vs Time, meta-category %s' % (mcid))
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('mean number of invites', fontsize=14, color='black', labelpad=15)
    plt.ylim((0,10))
    plt.plot(weekly_rates,color='%s' % linecolr,linewidth=2.5)
    plb.savefig('mean_ni_vs_t_metcat%s.pdf' % mcid)
    #plb.show()

def plot_mean_invites_per_week_bins_superimposed():
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_rates_all=[]
    for week in range(0,len(week_starts)):
        weekly_rates_all.append(np.mean(requests_to_invites_all_mc_date_range("off",week_starts[week],week_ends[week],1)))
    weekly_rates_1=[]
    for week in range(0,len(week_starts)):
        weekly_rates_1.append(np.mean(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'1',1)))
    weekly_rates_2=[]
    for week in range(0,len(week_starts)):
        weekly_rates_2.append(np.mean(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'2',1)))
    weekly_rates_3=[]
    for week in range(0,len(week_starts)):
        weekly_rates_3.append(np.mean(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'3',1)))
    weekly_rates_4=[]
    for week in range(0,len(week_starts)):
        weekly_rates_4.append(np.mean(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'4',1)))
    weekly_rates_5=[]
    for week in range(0,len(week_starts)):
        weekly_rates_5.append(np.mean(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'5',1)))
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Mean Number of Invitations Sent vs Time')
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('mean number of invites', fontsize=14, color='black', labelpad=15)
    plt.ylim((3.5,6.5))
    mc_all, = plt.plot(weekly_rates_all,color='%s' % colors[0],linewidth=2.5,label='All metacategories')
    mc_1, = plt.plot(weekly_rates_1,color='%s' % colors[1],linewidth=2.5,label='Metacategory 1')
    mc_2, = plt.plot(weekly_rates_2,color='%s' % colors[2],linewidth=2.5,label='Metacategory 2')
    mc_3, = plt.plot(weekly_rates_3,color='%s' % colors[3],linewidth=2.5,label='Metacategory 3')
    mc_4, = plt.plot(weekly_rates_4,color='%s' % colors[4],linewidth=2.5,label='Metacategory 4')
    mc_5, = plt.plot(weekly_rates_5,color='%s' % colors[5],linewidth=2.5,label='Metacategory 5')
    plt.legend([mc_all, mc_1, mc_2, mc_3, mc_4, mc_5], ['All metacategories','Metacategory 1','Metacategory 2','Metacategory 3','Metacategory 4','Metacategory 5'])
    plb.savefig('mean_ni_vs_t_superimposed.pdf')
    #plb.show()

def plot_median_invites_per_week_bins(mcid):
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    #All metacategories
    if mcid.lower()=='all':
        linecolr=colors[0]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            val=np.median(requests_to_invites_all_mc_date_range("off",week_starts[week],week_ends[week],1))
            weekly_rates.append(val)
    #Given metacategory
    else:
        linecolr=colors[int(mcid)]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            val=np.median(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],mcid,1))
            weekly_rates.append(val)
    #print weekly_rates
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Median Number of Invitations Sent vs Time, meta-category %s' % (mcid))
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('median number of invites', fontsize=14, color='black', labelpad=15)
    plt.ylim((0,10))
    plt.plot(weekly_rates,color='%s' % linecolr,linewidth=2.5)
    plb.savefig('median_ni_vs_t_metcat%s.pdf' % mcid)
    #plb.show()

def plot_median_invites_per_week_bins_superimposed():
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_rates_all=[]
    for week in range(0,len(week_starts)):
        weekly_rates_all.append(np.median(requests_to_invites_all_mc_date_range("off",week_starts[week],week_ends[week],1)))
    weekly_rates_1=[]
    for week in range(0,len(week_starts)):
        weekly_rates_1.append(np.median(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'1',1)))
    weekly_rates_2=[]
    for week in range(0,len(week_starts)):
        weekly_rates_2.append(np.median(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'2',1)))
    weekly_rates_3=[]
    for week in range(0,len(week_starts)):
        weekly_rates_3.append(np.median(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'3',1)))
    weekly_rates_4=[]
    for week in range(0,len(week_starts)):
        weekly_rates_4.append(np.median(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'4',1)))
    weekly_rates_5=[]
    for week in range(0,len(week_starts)):
        weekly_rates_5.append(np.median(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'5',1)))
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Median Number of Invitations Sent vs Time')
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('median number of invites', fontsize=14, color='black', labelpad=15)
    plt.ylim((3.5,6.5))
    mc_all, = plt.plot(weekly_rates_all,color='%s' % colors[0],linewidth=2.5,label='All metacategories')
    mc_1, = plt.plot(weekly_rates_1,color='%s' % colors[1],linewidth=2.5,label='Metacategory 1')
    mc_2, = plt.plot(weekly_rates_2,color='%s' % colors[2],linewidth=2.5,label='Metacategory 2')
    mc_3, = plt.plot(weekly_rates_3,color='%s' % colors[3],linewidth=2.5,label='Metacategory 3')
    mc_4, = plt.plot(weekly_rates_4,color='%s' % colors[4],linewidth=2.5,label='Metacategory 4')
    mc_5, = plt.plot(weekly_rates_5,color='%s' % colors[5],linewidth=2.5,label='Metacategory 5')
    plt.legend([mc_all, mc_1, mc_2, mc_3, mc_4, mc_5], ['All metacategories','Metacategory 1','Metacategory 2','Metacategory 3','Metacategory 4','Metacategory 5'])
    plb.savefig('median_ni_vs_t_superimposed.pdf')
    #plb.show()

def plot_std_invites_per_week_bins(mcid):
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    #All metacategories
    if mcid.lower()=='all':
        linecolr=colors[0]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            val=np.std(requests_to_invites_all_mc_date_range("off",week_starts[week],week_ends[week],1))
            weekly_rates.append(val)
    #Given metacategory
    else:
        linecolr=colors[int(mcid)]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            val=np.std(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],mcid,1))
            weekly_rates.append(val)
    #print weekly_rates
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Std. Dev. Number of Invitations Sent vs Time, meta-category %s' % (mcid))
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('std. dev. number of invites', fontsize=14, color='black', labelpad=15)
    plt.ylim((0,10))
    plt.plot(weekly_rates,color='%s' % linecolr,linewidth=2.5)
    plb.savefig('std_ni_vs_t_metcat%s.pdf' % mcid)
    #plb.show()

def plot_std_invites_per_week_bins_superimposed():
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_rates_all=[]
    for week in range(0,len(week_starts)):
        weekly_rates_all.append(np.std(requests_to_invites_all_mc_date_range("off",week_starts[week],week_ends[week],1)))
    weekly_rates_1=[]
    for week in range(0,len(week_starts)):
        weekly_rates_1.append(np.std(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'1',1)))
    weekly_rates_2=[]
    for week in range(0,len(week_starts)):
        weekly_rates_2.append(np.std(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'2',1)))
    weekly_rates_3=[]
    for week in range(0,len(week_starts)):
        weekly_rates_3.append(np.std(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'3',1)))
    weekly_rates_4=[]
    for week in range(0,len(week_starts)):
        weekly_rates_4.append(np.std(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'4',1)))
    weekly_rates_5=[]
    for week in range(0,len(week_starts)):
        weekly_rates_5.append(np.std(requests_to_invites_given_mc_date_range("off",week_starts[week],week_ends[week],'5',1)))
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Std. Dev. Number of Invitations Sent vs Time')
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('std. dev. number of invites', fontsize=14, color='black', labelpad=15)
    plt.ylim((3.5,6.5))
    mc_all, = plt.plot(weekly_rates_all,color='%s' % colors[0],linewidth=2.5,label='All metacategories')
    mc_1, = plt.plot(weekly_rates_1,color='%s' % colors[1],linewidth=2.5,label='Metacategory 1')
    mc_2, = plt.plot(weekly_rates_2,color='%s' % colors[2],linewidth=2.5,label='Metacategory 2')
    mc_3, = plt.plot(weekly_rates_3,color='%s' % colors[3],linewidth=2.5,label='Metacategory 3')
    mc_4, = plt.plot(weekly_rates_4,color='%s' % colors[4],linewidth=2.5,label='Metacategory 4')
    mc_5, = plt.plot(weekly_rates_5,color='%s' % colors[5],linewidth=2.5,label='Metacategory 5')
    plt.legend([mc_all, mc_1, mc_2, mc_3, mc_4, mc_5], ['All metacategories','Metacategory 1','Metacategory 2','Metacategory 3','Metacategory 4','Metacategory 5'])
    plb.savefig('std_ni_vs_t_superimposed.pdf')
    #plb.show()

def num_loc_per_week_bins():
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    
    weekly_locations_all=[]
    weekly_locations_low=[]
    weekly_locations_med=[]
    weekly_locations_hig=[]
    for week in range(0,len(week_starts)):
        weekly_locations_all.append(locations_per_requesttime_all_mc_date_range(week_starts[week],week_ends[week]))
        weekly_locations_low.append(locations_per_requesttime_all_mc_date_range_pop(week_starts[week],week_ends[week],'low'))
        weekly_locations_med.append(locations_per_requesttime_all_mc_date_range_pop(week_starts[week],week_ends[week],'med'))
        weekly_locations_hig.append(locations_per_requesttime_all_mc_date_range_pop(week_starts[week],week_ends[week],'high'))
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Number of Unique Request Locations vs Time')
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('number of unique request locations', fontsize=14, color='black', labelpad=15)
    plt.ylim((0,130))
    locations_all, = plt.plot(weekly_locations_all,color='black',linewidth=2.5,label="All locations")
    locations_low, = plt.plot(weekly_locations_low,color='red',linewidth=2.5,label="Low-population")
    locations_med, = plt.plot(weekly_locations_med,color='blue',linewidth=2.5,label="Medium-population")
    locations_hig, = plt.plot(weekly_locations_hig,color='green',linewidth=2.5,label="High-population")
    plt.legend([locations_all, locations_low, locations_med, locations_hig], ['All locations','Low-population','Medium-population','High-population'])
    plb.savefig('nlocations_vs_t.pdf')

def num_cat_per_week_bins():
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    
    weekly_categories=[]
    for week in range(0,len(week_starts)):
        weekly_categories.append(categories_per_requesttime_all_mc_date_range(week_starts[week],week_ends[week]))
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Number of Unique Request Categories vs Time')
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('number of unique request categories', fontsize=14, color='black', labelpad=15)
    plt.ylim((60,130))
    categories, = plt.plot(weekly_categories,color='black',linewidth=2.5)
    plb.savefig('ncategories_vs_t.pdf')

def num_cat_per_day_bins(ret_series):
    days=["2013-07-01","2013-07-02","2013-07-03","2013-07-04","2013-07-05","2013-07-06","2013-07-07","2013-07-08","2013-07-09","2013-07-10","2013-07-11","2013-07-12","2013-07-13","2013-07-14","2013-07-15","2013-07-16","2013-07-17","2013-07-18","2013-07-19","2013-07-20","2013-07-21","2013-07-22","2013-07-23","2013-07-24","2013-07-25","2013-07-26","2013-07-27","2013-07-28","2013-07-29","2013-07-30","2013-07-31","2013-08-01","2013-08-02","2013-08-03","2013-08-04","2013-08-05","2013-08-06","2013-08-07","2013-08-08","2013-08-09","2013-08-10","2013-08-11","2013-08-12","2013-08-13","2013-08-14","2013-08-15","2013-08-16","2013-08-17","2013-08-18","2013-08-19","2013-08-20","2013-08-21","2013-08-22","2013-08-23","2013-08-24","2013-08-25","2013-08-26","2013-08-27","2013-08-28","2013-08-29","2013-08-30","2013-08-31"]
    
    daily_categories=[]
    for day in range(0,len(days)):
        daily_categories.append(categories_per_requesttime_all_mc_date_range(days[day],days[day]))
    if ret_series==0:
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Number of Unique Request Categories vs Time')
        plt.xlabel('day in range [07-01-2013, 08-31-2013]', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of unique request categories', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,80))
        categories, = plt.plot(daily_categories,color='black',linewidth=2.5)
        plb.savefig('ncategories_vs_t_day.pdf')
        plb.show()
        return
    else:
        return daily_categories
    
if __name__ == '__main__':
    
    connection=read_database.database_connect(sys.argv[1])
    
    if "help" in sys.argv or len(sys.argv)<3:
        print "The code can be run in the following ways:"
        print "Requests vs time for all meta-categories: python requests_basic_info.py DB_FILENAME 1"
        print "Requests vs time for a given meta-category: python requests_basic_info.py DB_FILENAME 1 MCID"
        print "Requests to invites for all meta-categories in a given date range: python requests_basic_info.py DB_FILENAME 2 '"'YYYY-MM-DD'"' '"'YYYY-MM-DD'"'"
        print "Requests to invites for a given meta-category in a given date range: python requests_basic_info.py DB_FILENAME 2 '"'YYYY-MM-DD'"' '"'YYYY-MM-DD'"' MCID"
        print "Mean invites per week: python requests_basic_info.py DB_FILENAME 3"
        print "Median invites per week: python requests_basic_info.py DB_FILENAME 4"
        print "Std. Dev. invites per week: python requests_basic_info.py DB_FILENAME 5"
        print "Number of unique request location ids per week: python requests_basic_info.py DB_FILENAME 6"
        print "Number of unique request category ids per day and per week: python requests_basic_info.py DB_FILENAME 7"
        
        
    elif sys.argv[2]=='1':  # requests vs time
        if len(sys.argv)==3:  #all metacategories
            requests_vs_time_all_mc("on")
        elif len(sys.argv)==4:  #given metacategory
            requests_vs_time_given_mc("on",sys.argv[3])
        else:
            print "Something went wrong, try this for help: python requests_basic_info.py help"
            
    elif sys.argv[2]=='2':  #requests to invites
        if len(sys.argv)==5:  #all metacategories
            requests_to_invites_all_mc_date_range("on",sys.argv[3],sys.argv[4],0)
        elif len(sys.argv)==6:  #given metacategory
            requests_to_invites_given_mc_date_range("on",sys.argv[3],sys.argv[4],sys.argv[5],0)
        else:
            print "Something went wrong, try this for help: python requests_basic_info.py help"
            
    elif sys.argv[2]=='3':
        plot_mean_invites_per_week_bins('all')
        plot_mean_invites_per_week_bins('1')
        plot_mean_invites_per_week_bins('2')
        plot_mean_invites_per_week_bins('3')
        plot_mean_invites_per_week_bins('4')
        plot_mean_invites_per_week_bins('5')
        plot_mean_invites_per_week_bins_superimposed()
        
    elif sys.argv[2]=='4':
        plot_median_invites_per_week_bins('all')
        plot_median_invites_per_week_bins('1')
        plot_median_invites_per_week_bins('2')
        plot_median_invites_per_week_bins('3')
        plot_median_invites_per_week_bins('4')
        plot_median_invites_per_week_bins('5')
        plot_median_invites_per_week_bins_superimposed()
        
    elif sys.argv[2]=='5':
        plot_std_invites_per_week_bins('all')
        plot_std_invites_per_week_bins('1')
        plot_std_invites_per_week_bins('2')
        plot_std_invites_per_week_bins('3')
        plot_std_invites_per_week_bins('4')
        plot_std_invites_per_week_bins('5')
        plot_std_invites_per_week_bins_superimposed()
        
    elif sys.argv[2]=='6':
        num_loc_per_week_bins()
        
    elif sys.argv[2]=='7':
        num_cat_per_week_bins()
        num_cat_per_day_bins(0)
        
    else:
        print "Something went wrong, try this for help: python requests_basic_info.py help"

