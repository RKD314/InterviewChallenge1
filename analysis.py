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
import scipy.stats as stats
import matplotlib.gridspec as gridspec

#Helper function
def convert_time_to_datetime(time_string):
    (year,month,daytime)=time_string.split("-")
    (day,time)=daytime.split(" ")
    (hour,min,secdec)=time.split(":")
    
    microsec=float(secdec)%1.0
    sec=float(secdec)-microsec
    
    microsec=microsec*1000000.
    
    converted_time=datetime.datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), int(microsec))
    
    return converted_time
#i2q daily and weekly series
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
        plt.ylim((0,0.6))
        plt.hist(num_quotes_per_invite,range=(0,3),bins=3,normed=0,facecolor='red',alpha=0.2)
        plb.savefig('invites_to_quotes_counts_%s_to_%s.pdf' % (date1,date2))
    quotes=float(sum(num_quotes_per_invite))
    invites=float(len(num_quotes_per_invite))
    return float(quotes/invites)
def plot_i2q_rate_week_bins(ret_series):
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_rates=[]
    for week in range(0,len(week_starts)):
        weekly_rates.append(invites_to_quotes_all_mc_date_range("off",week_starts[week],week_ends[week]))
    if ret_series==0:
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Invitation to Quote Rate vs Time')
        plt.xlabel('week in range [07-01-2013, 09-01-2013]', fontsize=14, color='black', labelpad=10)
        plt.ylabel('invite-to-quote rate', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,1.0))
        plt.plot(weekly_rates,color='black',linewidth=2.5)
        plb.savefig('i2qr_vs_t_week.pdf')
        return
    else:
        return weekly_rates
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
        plb.savefig('i2qr_vs_t_day.pdf')
        return
    else:
        return day_rates
#unique category IDs daily and weekly series
def categories_per_requesttime_all_mc_date_range(date1,date2):
    if date1==date2:
        sql_categoryid_requests="select category_id from requests where date(creation_time) = '%s';" % date1
    else:
        sql_categoryid_requests="select category_id from requests where creation_time >= date('%s') and creation_time <= date('%s');" % (date1,date2)
    categoryid_requests=read_database.read_data(connection, sql_categoryid_requests)
    return len(set(categoryid_requests))
def num_cat_per_week_bins(ret_series):
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_categories=[]
    for week in range(0,len(week_starts)):
        weekly_categories.append(categories_per_requesttime_all_mc_date_range(week_starts[week],week_ends[week]))
    if ret_series==0:
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Number of Unique Request Categories vs Time')
        plt.xlabel('week in range [07-01-2013, 08-31-2013]', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of unique request categories', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,80))
        categories, = plt.plot(weekly_categories,color='black',linewidth=2.5)
        plb.savefig('ncategories_vs_t_week.pdf')
        return
    else:
        return weekly_categories
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
#quotes given daily and weekly series
def quotes_per_time(date1,date2):
    if date1==date2:
        sql_quotes_time="select sent_time from quotes where date(sent_time) = '%s';" % date1
    else:
        sql_quotes_time="select sent_time from quotes where sent_time >= date('%s') and sent_time <= date('%s');" % (date1,date2)
    quotes_time=read_database.read_data(connection, sql_quotes_time)
    return len(quotes_time)
def quotes_per_week(ret_series):
    week_starts=["2013-07-01","2013-07-08","2013-07-15","2013-07-22","2013-07-29","2013-08-05","2013-08-12","2013-08-19","2013-08-26"]
    week_ends  =["2013-07-07","2013-07-14","2013-07-21","2013-07-28","2013-08-04","2013-08-11","2013-08-18","2013-08-25","2013-09-01"]
    weekly_quotes=[]
    for week in range(0,len(week_starts)):
        weekly_quotes.append(quotes_per_time(week_starts[week],week_ends[week]))
    if ret_series==0:
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Number of Quotes vs Time')
        plt.xlabel('week in range [07-01-2013, 08-31-2013]', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of quotes', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,1600))
        quotes, = plt.plot(weekly_quotes,color='black',linewidth=2.5)
        plb.savefig('nquotes_vs_t_week.pdf')
        return
    else:
        return weekly_quotes
def quotes_per_day(ret_series):
    days=["2013-07-01","2013-07-02","2013-07-03","2013-07-04","2013-07-05","2013-07-06","2013-07-07","2013-07-08","2013-07-09","2013-07-10","2013-07-11","2013-07-12","2013-07-13","2013-07-14","2013-07-15","2013-07-16","2013-07-17","2013-07-18","2013-07-19","2013-07-20","2013-07-21","2013-07-22","2013-07-23","2013-07-24","2013-07-25","2013-07-26","2013-07-27","2013-07-28","2013-07-29","2013-07-30","2013-07-31","2013-08-01","2013-08-02","2013-08-03","2013-08-04","2013-08-05","2013-08-06","2013-08-07","2013-08-08","2013-08-09","2013-08-10","2013-08-11","2013-08-12","2013-08-13","2013-08-14","2013-08-15","2013-08-16","2013-08-17","2013-08-18","2013-08-19","2013-08-20","2013-08-21","2013-08-22","2013-08-23","2013-08-24","2013-08-25","2013-08-26","2013-08-27","2013-08-28","2013-08-29","2013-08-30","2013-08-31"]
    daily_quotes=[]
    for day in range(0,len(days)):
        daily_quotes.append(quotes_per_time(days[day],days[day]))
    if ret_series==0:
        fig = plt.figure(facecolor='white')
        ax1 = plt.subplot(111)
        plt.title('Number of Quotes vs Time')
        plt.xlabel('day in range [07-01-2013, 08-31-2013]', fontsize=14, color='black', labelpad=10)
        plt.ylabel('number of quotes', fontsize=14, color='black', labelpad=15)
        plt.ylim((0,300))
        quotes, = plt.plot(daily_quotes,color='black',linewidth=2.5)
        plb.savefig('nquotes_vs_t_day.pdf')
        return
    else:
        return daily_quotes
def poly1fit_with_ci_and_uncert(x,y,xtitle,ytitle,filename,yerr_in,ret_mod_vals):
    if len(yerr_in)==0:
        yerr=map(lambda z: (math.sqrt(y[z])), range(0,len(y)))
    else:
        yerr=yerr_in
    x, y, yerr = np.asarray(x), np.asarray(y), np.asarray(yerr)
    n = y.size
    p, cov = np.polyfit(x, y, 1, w=1/yerr, cov=True)  # coefficients and covariance matrix
    yfit = np.polyval(p, x)                           # evaluate the polynomial at x
    if ret_mod_vals==1:
        return yfit
    perr = np.sqrt(np.diag(cov))     # standard-deviation estimates for each coefficient
    R2 = np.corrcoef(x, y)[0, 1]**2  # coefficient of determination between x and y
    resid = y - yfit
    chi2red = np.sum((resid/yerr)**2)/(n - 2)  # Chi-square reduced
    s_err = np.sqrt(np.sum(resid**2)/(n - 2))  # standard deviation of the error (residuals)
    
    x2 = np.linspace(np.min(x), np.max(x), 100)
    y2 = np.linspace(np.min(yfit), np.max(yfit), 100)
    # Confidence interval for the linear fit:
    t_95 = stats.t.ppf(0.95, n - 2)
    t_685 = stats.t.ppf(0.685, n - 2)
    #ci = t * s_err * np.sqrt(    1/n + (x2 - np.mean(x))**2/np.sum((x-np.mean(x))**2))
    # Prediction interval for the linear fit:
    pi_95 = t_95 * s_err * np.sqrt(1 + 1/n + (x2 - np.mean(x))**2/np.sum((x-np.mean(x))**2))
    pi_685 = t_685 * s_err * np.sqrt(1 + 1/n + (x2 - np.mean(x))**2/np.sum((x-np.mean(x))**2))
    # Plot
    plt.figure(facecolor='white',figsize=(10, 5))
    plt.fill_between(x2, y2+pi_95, y2-pi_95, color=[1, 0, 0, 0.07], edgecolor='')
    plt.fill_between(x2, y2+pi_685, y2-pi_685, color=[0, 0, 1, 0.1], edgecolor='')
    plt.errorbar(x, y, yerr=yerr, fmt = 'bo', ecolor='b', capsize=0)
    plt.plot(x, yfit, 'r', linewidth=3, color=[1, 0, 0, .8])
    plt.xlabel('%s' % xtitle, fontsize=14,labelpad=10)
    plt.ylabel('y: %s' % ytitle, fontsize=14,labelpad=10)
    plt.title('$y = %.2f \pm %.2f + (%.3f \pm %.3f)x \; [R^2=%.2f,\, \chi^2_{red}=%.1f]$'
              %(p[1], perr[1], p[0], perr[0], R2, chi2red), fontsize=20, color=[0, 0, 0], y=1.02)  
    plt.xlim((-0.25, float(n-1)+.25))
    plt.tight_layout()
    plt.savefig('%s' % filename)
    return


if __name__ == '__main__':
    
    connection=read_database.database_connect(sys.argv[1])
    
    
    if sys.argv[2]=='trend':
        qvt=quotes_per_week(1)
        x_qvt=range(0,len(qvt))
        poly1fit_with_ci_and_uncert(x_qvt,qvt,'week in range [07-01-2013, 09-02-2013]','number of quotes','nquotes_t_week_lin_fit.pdf',[],0)
        
        i2q=plot_i2q_rate_week_bins(1)
        x_i2q=range(0,len(i2q))
        spc_yerr=[0.029988007195203354, 0.028386647790182976, 0.028082797815086526, 0.026793191107712166, 0.027607881518711637, 0.02711630722733202, 0.02842102114016023, 0.02748248549646564, 0.02748248549646564]
        poly1fit_with_ci_and_uncert(x_i2q,i2q,'week in range [07-01-2013, 09-02-2013]','invite to quote ratio','i2q_t_week_lin_fit.pdf',spc_yerr,0)
        
        cat=num_cat_per_week_bins(1)
        x_cat=range(0,len(cat))
        poly1fit_with_ci_and_uncert(x_cat,cat,'week in range [07-01-2013, 09-02-2013]','unique category ids','ncats_t_week_lin_fit.pdf',[],0)
        
    elif sys.argv[2]=='period_qvt':
        qvt_act=quotes_per_day(1)
        qvt_corrected=mlab.detrend_linear(np.asarray(qvt_act))
        fig = plt.figure(facecolor='white',figsize=(12,5))
        ax1 = plt.subplot(1,2,1)
        plt.title('Number of Quotes vs Time', fontsize=12)
        plt.xlabel('day in range [07-01-2013, 09-01-2013]', fontsize=12, color='black')
        plt.ylabel('number of quotes', fontsize=12, color='black', labelpad=15)
        plt.ylim((0,300))
        plt.plot(qvt_act,color='black',linewidth=2.0)
        ax2 = plt.subplot(1,2,2)
        plt.psd(qvt_corrected)
        plt.tight_layout()
        plb.savefig('qvt_periodicity.pdf')
        plb.show()
        
    elif sys.argv[2]=='period_cat':
        cat_act=num_cat_per_day_bins(1)
        cat_corrected=mlab.detrend_linear(np.asarray(cat_act))
        fig = plt.figure(facecolor='white',figsize=(12,5))
        ax1 = plt.subplot(1,2,1)
        plt.title('Number of Categories vs Time', fontsize=12)
        plt.xlabel('day in range [07-01-2013, 09-01-2013]', fontsize=12, color='black')
        plt.ylabel('number of unique request categories', fontsize=12, color='black', labelpad=15)
        plt.ylim((30,70))
        plt.plot(cat_act,color='black',linewidth=2.0)
        ax2 = plt.subplot(1,2,2)
        plt.psd(cat_corrected)
        plt.tight_layout()
        plb.savefig('cat_periodicity.pdf')
        plb.show()
        
    elif sys.argv[2]=='period_i2q':
        i2q_act=plot_i2q_rate_day_bins(1)
        i2q_corrected=mlab.detrend_linear(np.asarray(i2q_act))
        fig = plt.figure(facecolor='white',figsize=(12,5))
        ax1 = plt.subplot(1,2,1)
        plt.title('Invites to Quotes vs Time', fontsize=12)
        plt.xlabel('day in range [07-01-2013, 09-01-2013]', fontsize=12, color='black')
        plt.ylabel('invite to quote rate', fontsize=12, color='black', labelpad=15)
        plt.ylim((0.4,0.7))
        plt.plot(i2q_act,color='black',linewidth=2.0)
        ax2 = plt.subplot(1,2,2)
        plt.psd(i2q_corrected)
        plt.tight_layout()
        plb.savefig('i2q_periodicity.pdf')
        plb.show()
        
    elif sys.argv[2]=='co_i2q_cat':
        i2q_act=plot_i2q_rate_day_bins(1)
        i2q_corrected=mlab.detrend_linear(np.asarray(i2q_act))
        cat_act=num_cat_per_day_bins(1)
        cat_corrected=mlab.detrend_linear(np.asarray(cat_act))
        fig = plt.figure(facecolor='white',figsize=(12,5))
        ax1 = plt.subplot(111)
        plt.title('Coherence between i2q and n_cat', fontsize=12)
        plt.cohere(i2q_corrected, cat_corrected, NFFT=16)
        plt.tight_layout()
        plb.savefig('i2q_cat_cohere.pdf')
        plb.show()

    elif sys.argv[2]=='co_qvt_cat':
        qvt_act=quotes_per_day(1)
        qvt_corrected=mlab.detrend_linear(np.asarray(qvt_act))
        cat_act=num_cat_per_day_bins(1)
        cat_corrected=mlab.detrend_linear(np.asarray(cat_act))
        fig = plt.figure(facecolor='white',figsize=(12,5))
        ax1 = plt.subplot(111)
        plt.title('Coherence between qvt and n_cat', fontsize=12)
        plt.cohere(qvt_corrected, cat_corrected, NFFT=16)
        plt.tight_layout()
        plb.savefig('qvt_cat_cohere.pdf')
        plb.show()

    elif sys.argv[2]=='co_qvt_i2q':
        qvt_act=quotes_per_day(1)
        qvt_corrected=mlab.detrend_linear(np.asarray(qvt_act))
        i2q_act=plot_i2q_rate_day_bins(1)
        i2q_corrected=mlab.detrend_linear(np.asarray(i2q_act))
        fig = plt.figure(facecolor='white',figsize=(12,5))
        ax1 = plt.subplot(111)
        plt.title('Coherence between qvt and i2q', fontsize=12)
        plt.cohere(qvt_corrected, i2q_corrected, NFFT=16)
        plt.tight_layout()
        plb.savefig('qvt_i2q_cohere.pdf')
        plb.show()




