'''
 Author: sonik.-
 Date: March 21, 2022
 Purpose: This program reads in data from us-states-covid.csv (https://github.com/nytimes/covid-19-data) and provides the following data visualizations.
            (1) Line chart of total COVID cases in the Washington
            (2) Box Plot of total cases (Peak)
 Question answered: This program aims to answer the following questions:
            (1) Total COVID-19 cases in the Washington state
            (2) The trend of COVID-19 in the Washington state
            (3) The most dangerous and safest time during COVID in the Washington state
'''
import datetime
import traceback
import pandas as pd 

from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

#import seaborn as sns
#from matplotlib.ticker import ScalarFormatter
#from datetime import MAXYEAR, MINYEAR, datetime
#from datetime import MAXYEAR, MINYEAR
'''
 File Name: graphical.py
 Note: This module provides a class and methods to better organize extracted data and generate charts/graphs respectively.
'''

"""The class WA_COVID contain attributes that are associated with COVID dates, cases, and deaths in the WA state

:param dates: a list of formatted dates
:type dates: an instance of datetime
:param cases: a list which contains COVID cases per day in the WA state
:type cases: int
:param deaths: a list which contains COVID deaths per day in the WA state
:type deaths: int
"""
class WA_COVID :
    def __init__(self, dates, cases, deaths) : # list (dates), list (int), list (int)
        self.dates = dates
        self.cases = cases
        self.deaths = deaths


"""Takes in a file path to the targetted .csv file which contains the data of COVID-19 and perform the following:
    (1) Checks whether the path is valid by checking its data type (match str)
    (2) Open the given file
        (a) saved the csv header into "head".
        (b) check whether the header contains the keyword: "cases", "dates" and "deaths"; else, warn the user that the given dataset might have missed something.
    (3) Extract data from the given csv file using for loop
        (a) check whether the input stream contains the state "washington".
        (b) if true, extract dates, cases, and deaths to the corresponding list.
        (c) if false, move on to the next input stream.
    (4) Return a list of objects (WA_COVID)

:param path: a string that contains a path to the targetted csv file which contains COVID data in the US.
:type path: str or unicode
:returns: a list of WA_COVID objects
:rtype: WA_COVID
"""
def csvHandling(path) :
    if (not isinstance(path, str)) : # checks if the parameter is a string before proceeds (guard clause)
        #print #sys.exit(-1)
        raise TypeError("Wrong file path data type, please use a string that contains the file path (either: absolute / relative).")
    
    # initialize local variables
    dates, cases, deaths = [], [], []

    with open(path, "r") as data_file:
        head = data_file.readline().strip().casefold().split(",")
    
        # checks if the csv file contains "cases" and "date" by checking header
        if ("cases" not in head) and ("date" not in head) and ("deaths" not in head) :
            print("Given dataset missing either \"cases\", \"dates\" and \"deaths\". Careful that the outcome might not as ideal.") # just a warning

        for row in data_file : # manually loop through `data_file`
            temp = row.split(",")
            if temp[head.index("state")].casefold() == "washington".casefold() : # filter: lines that only contain washington state
                try : # specifically catch formatting exception (ValueError)
                    dates.append(datetime.datetime.strptime(temp[head.index("date".casefold())], "%Y-%m-%d"))
                except ValueError:
                    print("\033[4m","Date does not match format \"Year-Month-Date\" (ValueError), details see below:","\033[0m")
                    traceback.print_exc()

                cases.append(int(temp[head.index("cases".casefold())]))
                deaths.append(int(temp[head.index("deaths".casefold())]))   
    data_file.close()

    return WA_COVID(dates, cases, deaths);


"""Generate a scaled line chart which contains primary and secondary y-axis (cases and deaths respectively)
Note: Two y-axis scales will be generated for two y-axis.

:param dates: a list of datetime objects which contain date
:type dates: datetime
:param cases: a list which contains COVID cases per day in the WA state
:type cases: int
:param deaths: a list which contains COVID deaths per day in the WA state
:type deaths: int
:returns: void
:rtype: void
"""
def lineChartPlot_scaled(dates, cases, deaths) : # date and case
    # plot line graph
    fig, ax1 = plt.subplots(figsize=(24,18))

    # line chart settings
    plt.grid(True)
    #plt.gcf().set_size_inches(9,6)
    plt.xlabel("Dates") # set x label text

    plt.title("COVID Cases and Deaths per Day in the Washington states", fontweight="bold") # set chart title
    ax1.ticklabel_format(style='plain', axis='y') # remove scientific notation

    # reduce empty space at the front and end on the x-axis
    plt.xlim(xmin=min(dates) - datetime.timedelta(days=3), xmax=max(dates) + datetime.timedelta(days=8))

    # first y-axis - cases (ax1)
    a1, = ax1.plot(dates, cases, color="#1900ff")
    ax1.set_ylabel("Cases")
    ax1.fill_between(dates, cases, alpha=0.6)
    ax1.set_ylim(ymin=0, ymax=max(cases)+1000)

    # second y-axis - deaths (ax2)
    ax2 = ax1.twinx()
    a2, = ax2.plot(dates, deaths, color="#444444", linestyle="--")
    ax2.set_ylabel("Deaths")
    ax2.set_ylim(ymin=0)

    # format x-axis interval text in 'YYYY-mm'
    ax1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%b-%d'))
    for label in ax1.get_xticklabels(which='major') : # rotates and right-aligns the x labels so they don't crowd each other
        label.set(rotation=30, horizontalalignment='right')

    
    # display legend
    plt.legend((a1, a2), ["Cases per Day","Deaths per Day"], loc="upper left")

    plt.show()


"""Generate a unscaled line chart which contains primary and secondary y-axis (cases and deaths respectively)
Note: Two y-axis will share the primary y-axis scale.

:param dates: a list of datetime objects which contain date
:type dates: datetime
:param cases: a list which contains COVID cases per day in the WA state
:type cases: int
:param deaths: a list which contains COVID deaths per day in the WA state
:type deaths: int
:returns: void
:rtype: void
"""
def lineChartPlot(dates, cases, deaths) :
    # plot line graph
    fig, ax = plt.subplots(figsize=(24,18))

    # line chart settings
    plt.grid(True) # show grid
    #plt.gcf().set_size_inches(12,8) # set size(w, h)
    plt.xlabel("Dates") # set x label text 
    plt.ylabel("Cases and Deaths") # set y label text
    plt.title("COVID Cases and Deaths per Day in the Washington states", fontweight="bold") # set chart title
    ax.ticklabel_format(style='plain', axis='y') # remove scientific notation
    
    # reduce empty space at the front and end on the x-axis
    plt.xlim(xmin=min(dates) - datetime.timedelta(days=3), xmax=max(dates) + datetime.timedelta(days=8))
    
    # plotting the first y-axis - cases
    plt.plot_date(dates, cases, color="#5a7d9a", label="Cases", linestyle="solid", markersize=1.6)
    ax.fill_between(dates, cases, alpha=0.5)

    # plotting the second y-axis - deaths
    plt.plot(dates, deaths, color="#FF0000", linestyle="--", label="Deaths")
    ax.set_ylim(ymin=0, ymax=max(cases)+1000)

    # format x-axis interval text in 'YYYY-mm'
    ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%b'))
    for label in ax.get_xticklabels(which='major') : # rotates and right-aligns the x labels so they don't crowd each other
        label.set(rotation=30, horizontalalignment='right')
    
    plt.legend()
    plt.show()


"""Generate a Box Plot (Box-N-Whiskers) to determine if there is an outlier data value in the given dataset.
:param cases: a list which contains COVID cases per day in the WA state
:type cases: int
:param deaths: a list which contains COVID deaths per day in the WA state
:type deaths: int
"""
def box_N_whiskerPlot(cases, deaths) : # notch=True
    data = {"New Cases Per Day": [list(map(int, cases))], 
            "New Deaths Per Day": [list(map(int, deaths))]}

    df = pd.DataFrame(data)

    fig, axs = plt.subplots(1, len(df.columns), figsize=(18,10))
    
    plt.suptitle("Box-N-Whiskers Plot for COVID Cases and Deaths in WA")

    for i, ax in enumerate(axs.flat) :
        ax.grid(visible=True)
        ax.set_title(df.columns[i], fontweight="bold")

        ax.boxplot(df.iloc[:, i], 1, showmeans=True) # remove the parameter 1 if want the basic plot
        ax.tick_params(axis='y')
    
    plt.show()


"""Line plot with desccription & provided which describe the data visualization
:param covidData: a list of WA_COVID objects
:type covidData: WA_COVID
:returns: void
:rtype: void
"""
def covid_lineplot(covidData) : # 
    lineChartPlot(covidData.dates, covidData.cases, covidData.deaths)
    print("*Due to the death rate being really low compared to the new cases and it is hard to observe [12,210 (death) : 1,436,187 (cases)]; an independent y-axis scale (scaled) for the secondary y-axis line graph is also available.*")
    lineChartPlot_scaled(covidData.dates, covidData.cases, covidData.deaths)
    print("\033[4m"+f"The data and the x and y-axis: (line chart)"+"\033[0m")
    print(f"\t•	The data represents the number of new COVID cases and deaths in Washington state on a daily basis for the period {covidData.dates[covidData.cases.index(min(covidData.cases))].strftime('%d, %b %Y')}-{covidData.dates[covidData.cases.index(max(covidData.cases))].strftime('%d, %b %Y')}")
    print("\t•	The x-axis (horizontal) represents the time period (time series).")
    print("\t•	The y-axis on the left and the solid blue line represents the number of cases.")
    print("\t•	The y-axis on the right and the dashed red / grey line represents the number of deaths.")
    print("\t•	The y-axis scale (vertical): y1 is measuring cases per day, y2 is measuring deaths per day.\n")


"""Box Plot to determine if there is outliers data value by checking IQR (upper limits and lower limits)
:param covidData: a list of WA_COVID objects
:type covidData: WA_COVID
:returns: void
:rtype: void
"""
def covid_boxplot(covidData) :
    box_N_whiskerPlot(covidData.cases, covidData.deaths)
    print("There are outliners located at the interval of (4855, 63640) in the boxplot of daily new cases in WA.")
    print("There are outliers located at the interval of (-73, -54) and (56, 135) in the boxplot of daily new deaths in WA.\n")


"""Question Answering (**Ask at least two questions that require more than just returning the count of some data item**)
:param covidData: a list of WA_COVID objects
:type covidData: WA_COVID
"""
def ans2ques(covidData) :
    print("\033[4m"+f"Data visualization and statistics of COVID-19 in Washington state:"+"\033[0m")
    print("\tQ1: \x1B[3mTotal COVID-19 cases in the Washington state.\x1B[0m")
    print(f"\t  A:The total COVID cases in Washington state are {sum(covidData.cases)}, and the total deaths due to COVID are {sum(covidData.deaths)}.\n")

    print("\tQ2: \x1B[3mThe trend of COVID-19 in the Washington state.\x1B[0m")
    print("\t  A:From the chart, there is a downward trend after the peak (global maximum) on Dec 2022-Fed 2022.\n")

    print("\tQ3: \x1B[3mThe most dangerous and safest time during COVID in the Washington state.\x1B[0m")
    print(f"\t  A:The highest new cases per day is {max(covidData.cases)} on {covidData.dates[covidData.cases.index(max(covidData.cases))].strftime('%d, %b %Y')}.")
    print(f"\t\t  • From the line chart, there were three waves of COVID in Washington states (concave up & local maximum): (1) Nov 2020-Jan 2021 (2) July 2021-Oct 2021 (3) Dec 2022-Feb 2022")
    print("\t\t  • The safest time during COVID in the Washington state is at the beginning of the pandemic (global minimum).\n")

    print("• \033[4m"+f"COVID Death Rate in WA: {sum(covidData.deaths)/sum(covidData.cases) * 100}%"+"\033[0m") # 12,210 (death) / 1,436,187 (cases) * 100%