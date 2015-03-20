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
import scipy.stats
import matplotlib.gridspec as gridspec


def convert_time_to_datetime(time_string):
    (year,month,daytime)=time_string.split("-")
    (day,time)=daytime.split(" ")
    (hour,min,secdec)=time.split(":")
    
    microsec=float(secdec)%1.0
    sec=float(secdec)-microsec
    
    microsec=microsec*1000000.
    
    converted_time=datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), int(microsec))
    
    return converted_time

def invites_vs_time_all_mc(plot_on_or_off):
    sql_invites_time="select sent_time from invites;"
    invites_time=read_database.read_data(connection, sql_invites_time)
        
    invites_converted_time=[]
    for timedate in invites_time:
        invites_converted_time.append(convert_time_to_datetime(str(timedate[0])))
        
    if plot_on_or_off.lower()=='on':
        hfmt = dts.DateFormatter('%m/%d')
        fig = plt.figure(facecolor='white',figsize=(15,6))
        
        ax1 = plt.subplot(1,2,1)
        plt.title('Invites over time (daily)', y=1.02)
        plt.xlabel('invite sent time [day]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of invites', fontsize=14, color='black', labelpad=15)
        plt.axis([dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0)),0,600])
        plt.hist(dts.date2num(invites_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=64, normed=0, facecolor='red', alpha=0.15)
        ax1.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU, SA)))
        ax1.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)
        
        ax2 = plt.subplot(1,2,2)
        plt.title('Invites over time (weekly)', y=1.02)
        plt.xlabel('invite sent time [week]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of invites', fontsize=14, color='black', labelpad=15)
        plt.axis([dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0)),0,3200])
        plt.hist(dts.date2num(invites_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=9, normed=0, facecolor='red', alpha=0.15)
        ax2.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU)))
        ax2.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)        
        
        plb.savefig('invites_over_time_daily_and_weekly.pdf')
        #plb.show()
        
    print "The first recorded invite took place at %s" % min(invites_converted_time)
    print "The last recorded invite took place at %s" % max(invites_converted_time)
    print "There were %i invites total" % len(invites_converted_time)
    
    return

def invites_vs_time_given_mc(plot_on_or_off, mcid):
    sql_invites_time="select sent_time from invites join requests_new on invites.request_id=requests_new.request_id where meta_category_id=%s;" % mcid
    invites_time=read_database.read_data(connection, sql_invites_time)
        
    invites_converted_time=[]
    for timedate in invites_time:
        invites_converted_time.append(convert_time_to_datetime(str(timedate[0])))
        
    if plot_on_or_off.lower()=="on":
        hfmt = dts.DateFormatter('%m/%d')
        fig = plt.figure(facecolor='white',figsize=(15,6))
        
        ax1 = plt.subplot(1,2,1)
        plt.title('Invites over time (daily), meta-category %s' % mcid, y=1.02)
        plt.xlabel('invite sent time [day]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of invites', fontsize=14, color='black', labelpad=15)
        plt.xlim((dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0))))
        plt.hist(dts.date2num(invites_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=64, normed=0, facecolor='red', alpha=0.15)
        ax1.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU, SA)))
        ax1.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)
        
        ax2 = plt.subplot(1,2,2)
        plt.title('Invites over time (weekly), meta-category %s' % mcid, y=1.02)
        plt.xlabel('invite sent time [week]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of invites', fontsize=14, color='black', labelpad=15)
        plt.xlim((dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0))))
        plt.hist(dts.date2num(invites_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=9, normed=0, facecolor='red', alpha=0.15)
        ax2.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU)))
        ax2.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)        
        
        plb.savefig('invites_over_time_daily_and_weekly_metcat%s.pdf' % mcid)
        #plb.show()
        
    print "The first recorded invite took place at %s" % min(invites_converted_time)
    print "The last recorded invite took place at %s" % max(invites_converted_time)
    print "There were %i invites total" % len(invites_converted_time)
    
    return

def invites_to_quotes_all_mc_date_range(plot_on_or_off,date1,date2):
    if date1==date2:
        sql_inviteid_quotes="select invites.invite_id from invites join quotes on invites.invite_id=quotes.invite_id where date(invites.sent_time) = '%s';" % date1
        sql_inviteid_noquote="select 0 from invites left join quotes on invites.invite_id=quotes.invite_id where quote_id is null and date(invites.sent_time) = '%s';" % date1
    else:
        sql_inviteid_quotes="select invites.invite_id from invites join quotes on invites.invite_id=quotes.invite_id where invites.sent_time >= date('%s') and invites.sent_time <= date('%s');" % (date1,date2)
        sql_inviteid_noquote="select 0 from invites left join quotes on invites.invite_id=quotes.invite_id where quote_id is null and invites.sent_time >= date('%s') and invites.sent_time <= date('%s');" % (date1,date2)
    inviteid_quotes=read_database.read_data(connection, sql_inviteid_quotes)
    
    dict_invites_quotes={}
    for inv in inviteid_quotes:
        if inv in dict_invites_quotes:
            dict_invites_quotes[inv]+=1
        else:
            dict_invites_quotes.setdefault(inv,1)
                
    num_quotes_per_invite=[]
    map(lambda z: num_quotes_per_invite.append(z[0]),read_database.read_data(connection, sql_inviteid_noquote))
    for invi in dict_invites_quotes:
        num_quotes_per_invite.append(dict_invites_quotes[invi])
        
    if plot_on_or_off.lower()=='on':
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Invitations to quotes, [%s, %s]' % (date1,date2))
        plt.xlabel('number of quotes for a given invite', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of invitations', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,1500))
        plt.hist(num_quotes_per_invite,range=(0,3),bins=3,normed=0,facecolor='red',alpha=0.2)
        plb.savefig('invites_to_quotes_counts_%s_to_%s.pdf' % (date1,date2))
        #plb.show()
        
    quotes=float(sum(num_quotes_per_invite))
    invites=float(len(num_quotes_per_invite))
    #print "The quote to invite ratio is: %2f" % float(quotes/invites)
    return float(quotes/invites)

def invites_to_quotes_given_mc_date_range(plot_on_or_off,date1,date2,mcid):
    sql_inviteid_quotes="select A.invite_id from (select * from invites join requests_new on invites.request_id=requests_new.request_id) as A join quotes on A.invite_id=quotes.invite_id where A.sent_time >= date('%s') and A.sent_time <= date('%s') and meta_category_id=%s;" % (date1,date2,mcid)
    inviteid_quotes=read_database.read_data(connection, sql_inviteid_quotes)
    
    sql_inviteid_noquote="select 0 from (select * from invites join requests_new on invites.request_id=requests_new.request_id) as A left join quotes on A.invite_id=quotes.invite_id where quote_id is null and A.sent_time >= date('%s') and A.sent_time <= date('%s') and meta_category_id=%s;" % (date1,date2,mcid)
    
    dict_invites_quotes={}
    for inv in inviteid_quotes:
        if inv in dict_invites_quotes:
            dict_invites_quotes[inv]+=1
        else:
            dict_invites_quotes.setdefault(inv,1)
                
    num_quotes_per_invite=[]
    map(lambda z: num_quotes_per_invite.append(z[0]),read_database.read_data(connection, sql_inviteid_noquote))
    for invi in dict_invites_quotes:
        num_quotes_per_invite.append(dict_invites_quotes[invi])
        
    if plot_on_or_off.lower()=='on':
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Invitations to quotes, [%s, %s], meta-category %s' % (date1,date2,mcid))
        plt.xlabel('number of quotes for a given invite', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of invitations', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,1.0))
        plt.hist(num_quotes_per_invite,range=(0,3),bins=3,normed=1,facecolor='red',alpha=0.2)
        plb.savefig('invites_to_quotes_counts_%s_to_%s_metcat%s.pdf' % (date1,date2,mcid))
        #plb.show()
        
    quotes=float(sum(num_quotes_per_invite))
    invites=float(len(num_quotes_per_invite))
    #print "The quote to invite ratio is: %2f" % float(quotes/invites)
    return float(quotes/invites)

def plot_i2q_rate_week_bins(mcid):
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    #All metacategories
    if mcid.lower()=='all':
        linecolr=colors[0]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            weekly_rates.append(invites_to_quotes_all_mc_date_range("off",week_starts[week],week_ends[week]))
    #Given metacategory
    else:
        linecolr=colors[int(mcid)]
        weekly_rates=[]
        for week in range(0,len(week_starts)):
            weekly_rates.append(invites_to_quotes_given_mc_date_range("off",week_starts[week],week_ends[week],mcid))
    #print weekly_rates
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Invitation to Quote Rate vs Time, meta-category %s' % (mcid))
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('invite-to-quote rate', fontsize=14, color='black', labelpad=15)
    plt.ylim((0,1.0))
    plt.plot(weekly_rates,color='%s' % linecolr,linewidth=2.5)
    plb.savefig('i2qr_vs_t_metcat%s.pdf' % (mcid))
    #plb.show()

def plot_i2q_rate_week_bins_superimposed():
    colors=['black','red','green','blue','orange','purple']
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_rates_all=[]
    for week in range(0,len(week_starts)):
        weekly_rates_all.append(invites_to_quotes_all_mc_date_range("off",week_starts[week],week_ends[week]))
    weekly_rates_1=[]
    for week in range(0,len(week_starts)):
        weekly_rates_1.append(invites_to_quotes_given_mc_date_range("off",week_starts[week],week_ends[week],'1'))
    weekly_rates_2=[]
    for week in range(0,len(week_starts)):
        weekly_rates_2.append(invites_to_quotes_given_mc_date_range("off",week_starts[week],week_ends[week],'2'))
    weekly_rates_3=[]
    for week in range(0,len(week_starts)):
        weekly_rates_3.append(invites_to_quotes_given_mc_date_range("off",week_starts[week],week_ends[week],'3'))
    weekly_rates_4=[]
    for week in range(0,len(week_starts)):
        weekly_rates_4.append(invites_to_quotes_given_mc_date_range("off",week_starts[week],week_ends[week],'4'))
    weekly_rates_5=[]
    for week in range(0,len(week_starts)):
        weekly_rates_5.append(invites_to_quotes_given_mc_date_range("off",week_starts[week],week_ends[week],'5'))
    fig = plt.figure(facecolor='white')
    ax1 = plt.subplot(111)
    plt.title('Invitation to Quote Rate vs Time')
    plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
    plt.ylabel('invite-to-quote rate', fontsize=14, color='black', labelpad=15)
    plt.ylim((0.35,1.15))
    mc_all, = plt.plot(weekly_rates_all,color='%s' % colors[0],linewidth=2.5,label='All metacategories')
    mc_1, = plt.plot(weekly_rates_1,color='%s' % colors[1],linewidth=2.5,label='Metacategory 1')
    mc_2, = plt.plot(weekly_rates_2,color='%s' % colors[2],linewidth=2.5,label='Metacategory 2')
    mc_3, = plt.plot(weekly_rates_3,color='%s' % colors[3],linewidth=2.5,label='Metacategory 3')
    mc_4, = plt.plot(weekly_rates_4,color='%s' % colors[4],linewidth=2.5,label='Metacategory 4')
    mc_5, = plt.plot(weekly_rates_5,color='%s' % colors[5],linewidth=2.5,label='Metacategory 5')
    plt.legend([mc_all, mc_1, mc_2, mc_3, mc_4, mc_5], ['All metacategories','Metacategory 1','Metacategory 2','Metacategory 3','Metacategory 4','Metacategory 5'])
    plb.savefig('i2qr_vs_t_superimposed.pdf')
    #plb.show()

def plot_i2q_rate_day_bins(ret_series):
    days=["2013-07-01","2013-07-02","2013-07-03","2013-07-04","2013-07-05","2013-07-06","2013-07-07","2013-07-08","2013-07-09","2013-07-10","2013-07-11","2013-07-12","2013-07-13","2013-07-14","2013-07-15","2013-07-16","2013-07-17","2013-07-18","2013-07-19","2013-07-20","2013-07-21","2013-07-22","2013-07-23","2013-07-24","2013-07-25","2013-07-26","2013-07-27","2013-07-28","2013-07-29","2013-07-30","2013-07-31","2013-08-01","2013-08-02","2013-08-03","2013-08-04","2013-08-05","2013-08-06","2013-08-07","2013-08-08","2013-08-09","2013-08-10","2013-08-11","2013-08-12","2013-08-13","2013-08-14","2013-08-15","2013-08-16","2013-08-17","2013-08-18","2013-08-19","2013-08-20","2013-08-21","2013-08-22","2013-08-23","2013-08-24","2013-08-25","2013-08-26","2013-08-27","2013-08-28","2013-08-29","2013-08-30","2013-08-31"]
    day_rates=[]
    for day in range(0,len(days)):
        day_rates.append(invites_to_quotes_all_mc_date_range("off",days[day],days[day]))
    if ret_series==0:
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Invitation to Quote Rate vs Time')
        plt.xlabel('day in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
        plt.ylabel('invite-to-quote rate', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,0.8))
        plt.plot(day_rates,color='black',linewidth=2.5)
    
        #ax2 = plt.subplot(1,2,2)
        #plt.psd(day_rates)
    
        plb.savefig('i2qr_vs_t_days.pdf')
        return
    else:
        return day_rates

def categories_per_requesttime_all_mc_date_range(date1,date2):
    if date1==date2:
        sql_categoryid_requests="select category_id from requests where date(creation_time) = '%s';" % date1
    else:
        sql_categoryid_requests="select category_id from requests where creation_time >= date('%s') and creation_time <= date('%s');" % (date1,date2)
    categoryid_requests=read_database.read_data(connection, sql_categoryid_requests)
    return len(set(categoryid_requests))

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
        print "Invites vs time for all meta-categories: python invites_basic_info.py DB_FILENAME 1"
        print "Invites vs time for a given meta-category: python invites_basic_info.py DB_FILENAME 1 MCID"
        print "Invites to quotes for all meta-categories in a given date range: python invites_basic_info.py DB_FILENAME 2 '"'YYYY-MM-DD'"' '"'YYYY-MM-DD'"'"
        print "Invites to quotes for a given meta-category in a given date range: python invites_basic_info.py DB_FILENAME 2 '"'YYYY-MM-DD'"' '"'YYYY-MM-DD'"' MCID"
        print "Invite to quote rate in weekly bins over different meta-categories: python invites_basic_info.py DB_FILENAME 3"
        print "Invite to quote rate in weekly bins over different meta-categories, superimposed plot: python invites_basic_info.py DB_FILENAME 4"
        print "Invite to quote rate in daily bins over all meta-categories: python invites_basic_info.py DB_FILENAME 5"
    
    elif sys.argv[2]=='1':  # invites vs time
        if len(sys.argv)==3:  #all metacategories
            invites_vs_time_all_mc("on")
        elif len(sys.argv)==4:  #given metacategory
            invites_vs_time_given_mc("on",sys.argv[3])
        else:
            print "Something went wrong, try this for help: python invites_basic_info.py help"
            
    elif sys.argv[2]=='2':  #invites to quotes
        if len(sys.argv)==5:  #all metacategories
            invites_to_quotes_all_mc_date_range("on",sys.argv[3],sys.argv[4])
        elif len(sys.argv)==6:  #given metacategory
            invites_to_quotes_given_mc_date_range("on",sys.argv[3],sys.argv[4],sys.argv[5])
        else:
            print "Something went wrong, try this for help: python invites_basic_info.py help"
            
    elif sys.argv[2]=='3':
        plot_i2q_rate_week_bins('all')
        plot_i2q_rate_week_bins('1')
        plot_i2q_rate_week_bins('2')
        plot_i2q_rate_week_bins('3')
        plot_i2q_rate_week_bins('4')
        plot_i2q_rate_week_bins('5')
        
    elif sys.argv[2]=='4':
        plot_i2q_rate_week_bins_superimposed()
        
    elif sys.argv[2]=='5':
        plot_i2q_rate_day_bins(0)
        
    else:
        print "Something went wrong, try this for help: python invites_basic_info.py help"
