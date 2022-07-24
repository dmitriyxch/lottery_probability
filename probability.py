
#fast version of hypergeometric distribution
from scipy.stats import hypergeom
import numpy as np
import scipy.stats
import math
import matplotlib.pyplot as plt

def laplace_f(x):
	return scipy.stats.norm.cdf(x)-0.5
	
def func_1(k,n,p,q):
    l = laplace_f( (k-n*p) / math.sqrt(n*p*q))
    #print((k-n*p) / math.sqrt(n*p*q))
    return l


def draw_plot(total_tickets,total_win_tickets, bought_tickets, calc_for_tickets):
    
    probability = total_win_tickets/total_tickets
    [M, n, N] = [total_tickets, total_win_tickets, bought_tickets]
    rv = hypergeom(M, n, N)
    x = np.arange(0, calc_for_tickets)
    pmf_dogs = rv.pmf(x)

    geom_prob_dict = {}
    geom_prob_dict_cum = {}
    cnt = 0
    i_cum = 0
    for i in pmf_dogs:
        i_cum += i
        r_or_more =  1-i_cum
        if cnt == 0:
            geom_prob_dict[-1] = {'label':'No Win','value':i}
            geom_prob_dict_cum[-1] = {'label':'No Win','value':i}
            
            geom_prob_dict[cnt] = {'label':'=>1','value':1-i}
            geom_prob_dict_cum[cnt] = {'label':'=>1','value':1-i}
        else:
            geom_prob_dict[cnt] = {'label':'='+str(cnt),'value':i}
            geom_prob_dict_cum[cnt] = {'label':'='+str(cnt),'value':r_or_more}

        cnt += 1
    

    trials = 0
    trials_cumulative = 0

    bernuli_prob_dict_cumilative = {}
    bernuli_prob_dict = {}

    for i in range(calc_for_tickets):
        trials_cumulative += scipy.stats.binom.pmf(i, bought_tickets, probability)
        trials = scipy.stats.binom.pmf(i, bought_tickets, probability)
        r_or_more =  1-trials_cumulative
        r_exact = 1-trials
        if i == 0:
            bernuli_prob_dict_cumilative[-1] = {'label':'No Win','value':trials}
            bernuli_prob_dict_cumilative[0] = {'label':'=>1','value':r_or_more}
            
            bernuli_prob_dict[-1] = {'label':'No Win','value':trials}
            bernuli_prob_dict[0] = {'label':'=>1','value':r_exact}
            
        else:
            bernuli_prob_dict_cumilative[i] = {'label':'=>'+str(i),'value':r_or_more}
            bernuli_prob_dict[i] = {'label':'=>'+str(i),'value':trials}

    # De Moivre–Laplace theorem
    #https://www.berdov.com/works/teorver/integralnaya-teorema-muavra-laplasa/
    #https://ru.stackoverflow.com/questions/542603/%D0%9A%D0%B0%D0%BA-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%B8-%D0%BB%D0%B0%D0%BF%D0%BB%D0%B0%D1%81%D0%B0-python

   
    q_prob = 1 - probability

    print(str(bought_tickets*probability*q_prob) + "=>10???")

    laplace_prob_dict = {}
    range_tickets = range(1,calc_for_tickets)
    for i in range_tickets:
        p = func_1(total_win_tickets,bought_tickets,probability,q_prob) - func_1(i,bought_tickets,probability,q_prob)
        if i == 1:
            laplace_prob_dict[0] = {'label':'No Win','value':1-p}
        laplace_prob_dict[i] = {'label':'>='+str(i),'value':p}

    parse_arr(laplace_prob_dict,'De Moivre–Laplace theorem')

    parse_arr(bernuli_prob_dict,'Bernuli',bernuli_prob_dict_cumilative)
    parse_arr(geom_prob_dict,'Hypergeometric distribution',geom_prob_dict_cum)


def print_plot(labels,y,title,labels2 = [],y2 = []):
    shift = 0
    if len(labels2):
        shift = 0.35/1.8
        
    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    p1 = ax.bar(x+shift, y,0.35, label='tickets')
    #plt.set_xticks(x,labels = labels)
    fig.set_size_inches(13, 7)
    ax.bar_label(p1, padding=3)
    
    if len(labels2):
        
        p2 = ax.bar(x-shift, y2, 0.35, label='tickets2')
        ax.bar_label(p2, padding=3)
        
    #rects1 = ax.bar(x - width/2, men_means, width, label='Men')
    #rects2 = ax.bar(x + width/2, women_means, width, label='Women')
    plt.xticks(x,labels = labels)
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_ylabel('probability')
    ax.set_title(title)
    fig.tight_layout()
    ax.legend()
    plt.show(block=False)


def parse_arr(array_plot ,title, array_plot2 = []):
    labels = []
    x = []
    y = []
    labels2 = []
    x2 = []
    y2 = []
    for arr in array_plot:
        #print(arr)
        labels.append(array_plot[arr]['label'])
        y.append(round(float(array_plot[arr]['value']),2))
        x.append(float(arr))
        
    for arr2 in array_plot2:
        #print(arr)
        labels2.append(array_plot2[arr2]['label'])
        y2.append(round(float(array_plot2[arr2]['value']),2))
        x2.append(float(arr2))
    
    if labels2: 
        print_plot(labels,y, title, x2,y2)
    else:
        print_plot(labels,y, title)


total_tickets = int(input('How many tickets total?: '))
total_win_tickets = int(input('How many tickets can win in lottery?: '))
bought_tickets = int(input('How many tickets you bought?: '))
calc_for_tickets = int(input('How many tickets you want to calculate?: '))

draw_plot(total_tickets,total_win_tickets, bought_tickets, calc_for_tickets)
    
input('press any key to close')


