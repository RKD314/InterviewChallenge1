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

if __name__ == '__main__':
    
    connection=read_database.database_connect(sys.argv[1])
    
    if sys.argv[2]=='1':    #Check the distribution of quotes by time
        sql_quotes_time="select sent_time from quotes;"
        quotes_time=read_database.read_data(connection, sql_quotes_time)
        
        quotes_converted_time=[]
        for timedate in quotes_time:
            quotes_converted_time.append(convert_time_to_datetime(str(timedate[0])))
        
        hfmt = dts.DateFormatter('%m/%d')
        fig = plt.figure(facecolor='white',figsize=(15,6))
        
        ax1 = plt.subplot(1,2,1)
        plt.title('Quotes over time (daily)', y=1.02)
        plt.xlabel('quote sent time [day]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of quotes', fontsize=14, color='black', labelpad=15)
        plt.axis([dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0)),0,350])
        plt.hist(dts.date2num(quotes_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=64, normed=0, facecolor='purple', alpha=0.15)
        ax1.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU,SA)))
        ax1.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)
        
        ax2 = plt.subplot(1,2,2)
        plt.title('Quotes over time (weekly)', y=1.02)
        plt.xlabel('quote sent time [week]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of quotes', fontsize=14, color='black', labelpad=15)
        plt.axis([dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0)),0,1700])
        plt.hist(dts.date2num(quotes_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=9, normed=0, facecolor='purple', alpha=0.15)
        ax2.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU)))
        ax2.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)        
        
        plb.savefig('quotes_over_time_daily_and_weekly.pdf')
        #plb.show()
        
        print "The first recorded quote took place at %s" % min(quotes_converted_time)
        print "The last recorded quote took place at %s" % max(quotes_converted_time)
        print "There were %i quotes total" % len(quotes_converted_time)

    elif sys.argv[2]=='2':    #Check the distribution of quotes by time for metacategory
        sql_quotes_time="select A.sent_time from (select quotes.sent_time,request_id from quotes join invites on quotes.invite_id=invites.invite_id) as A join requests_new on A.request_id=requests_new.request_id where meta_category_id=%s;" % sys.argv[3]
        quotes_time=read_database.read_data(connection, sql_quotes_time)
        
        quotes_converted_time=[]
        for timedate in quotes_time:
            quotes_converted_time.append(convert_time_to_datetime(str(timedate[0])))
        
        hfmt = dts.DateFormatter('%m/%d')
        fig = plt.figure(facecolor='white',figsize=(15,6))
        
        ax1 = plt.subplot(1,2,1)
        plt.title('Quotes over time (daily), meta-category %s' % sys.argv[3], y=1.02)
        plt.xlabel('quote sent time [day]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of quotes', fontsize=14, color='black', labelpad=15)
        plt.xlim((dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0))))
        plt.hist(dts.date2num(quotes_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=64, normed=0, facecolor='purple', alpha=0.15)
        ax1.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU,SA)))
        ax1.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)
        
        ax2 = plt.subplot(1,2,2)
        plt.title('Quotes over time (weekly), meta-category %s' % sys.argv[3], y=1.02)
        plt.xlabel('quote sent time [week]', fontsize=14, color='black', labelpad=20)
        plt.ylabel('number of quotes', fontsize=14, color='black', labelpad=15)
        plt.xlim((dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,3,0,0,0))))
        plt.hist(dts.date2num(quotes_converted_time),range=(dts.date2num(datetime.datetime(2013,7,1,0,0,0)),dts.date2num(datetime.datetime(2013,9,2,0,0,0))),bins=9, normed=0, facecolor='purple', alpha=0.15)
        ax2.xaxis.set_major_locator(dts.WeekdayLocator(byweekday=(TU)))
        ax2.xaxis.set_major_formatter(hfmt)
        plt.xticks(rotation='vertical')
        plt.subplots_adjust(bottom=.2)        
        
        plb.savefig('quotes_over_time_daily_and_weekly_metcat%s.pdf' % sys.argv[3])
        
        print "The first recorded quote took place at %s" % min(quotes_converted_time)
        print "The last recorded quote took place at %s" % max(quotes_converted_time)
        print "There were %i quotes total" % len(quotes_converted_time)

