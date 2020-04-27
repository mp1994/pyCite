# Import Libs
import requests
from lxml import html
import time
from progressBar import *

def getNumberOfCitations(keyword, year):

    # Base URL
    page_URL = "https://scholar.google.com/scholar"
    
    # Add the query
    page_URL = page_URL + "?q=" + keyword.replace(' ', '+') + '&hl=en&as_sdt=0%2C5'
    
    # Check the Years Interval
    if type(year) is list:       
        if len(year) == 2:
            year_low = min(year)
            year_high = max(year)
    else:
        year_low = year_high = year
    
    page_URL = page_URL + "&as_ylo=" + str(year_low) + "&as_yhi=" + str(year_high)

    # Get the web content
    page = requests.get(page_URL)
    tree = html.fromstring(page.content)

    # Get the Number of Results
    n = tree.xpath('//div[@class="gs_ab_mdw"]/text()')
    if len(n) == 0:
        print("WARNING: nothing found.")
        if tree.xpath('//div[@id="infoDiv"]/text()')[0][1:18] == 'This page appears':
            return -1
        else:
            return 0
    n = n[0].split()[1]
    
    if len(n) >= 5:
        # Handle the thousands separator ("." or "," depending on the language)
        if n[len(n)-4] == '.':
            n = n.split('.')
        elif n[len(n)-4] == ',':
            n = n.split(',')
        n = int(n[0])*1000 + int(n[1])
    else:
        n = int(n)
    
    #print(n)
    
    return n
    
def getPubsPerYear(keyword, year_low, year_high):

    n_pubs = []
    
    print(">> Query: " + keyword + " from " + str(year_low) + " to " + str(year_high) + "...")
    
    YEAR = range(year_low, year_high+1, 1)
    pBar = progressBar(len(YEAR))
    
    for year in YEAR:
        n_pubs.append(getNumberOfCitations(keyword, year))
        # Delay to avoid multiple-requests detection
        pBar.update()
        time.sleep(1)
        if n_pubs[len(n_pubs)-1] == -1:
            print("WARNING: further requests on this IP address are blocked from the server. Please re-try in a while...")
            return 
            
    return n_pubs
    
def makeFigure(data, years, kw):

    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    matplotlib.rcParams.update({'font.size': 16})

    nkw = min([len(data), len(data[0])])

    # Plot
    x = np.arange(years[0], years[1]+1, 1)
    #plt.plot(x, np.transpose(data))
    
    for i in range(0, nkw, 1):
        plt.plot(x, data[i], label=kw[i])
    
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.xticks(np.append(np.arange(years[0],years[1],5),years[1]))
    #plt.grid()
    
    # Legend
    if nkw > 1:
        plt.legend()
    
    plt.show()

if __name__ == '__main__':
    
    # Get user-input
    '''kw = input('Insert keyword(s) [separated by a space]: ')
    yr = input('Insert the year limit: ')
    n = getNumberOfCitations(kw, yr)
    print("Number of citations = " + str(n))'''
    
    n_multi_rob = getPubsPerYear("robotic exoskeleton", 2000, 2019)
    #print(n_multi)
    
    n_multi_exo = getPubsPerYear("exoskeleton", 2000, 2019)
        
    makeFigure([n_multi_rob, n_multi_exo], [2000, 2019], ["robotic exoskeleton", "exoskeleton"])

    
    