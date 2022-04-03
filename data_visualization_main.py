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
import graphical as grph
'''
 File Name: data_visualization_main.py
 Note: This module is the main method. It also answers the targetted questions and run the methods in `graphical.py`.
'''

""" ------------------------------------------------------------------------------------------ MAIN ------------------------------------------------------------------------------------------"""
print("This program will be providing charts and graph for daily new cases and deaths regarding to COVID-19 in Washington state.")

# CSV Dataset is read into a list
covidData_WA = grph.csvHandling("us-states-covid.csv") # return data type is a list of `WA_COVID` objects
#print(f"{covidData_WA.dates}\n\n{covidData_WA.cases}\n\n{covidData_WA.deaths}") # check list data


# Line Chart
grph.covid_lineplot(covidData_WA)


# Box Plot
grph.covid_boxplot(covidData_WA)


# 3 data related questions and answes (complexity)
grph.ans2ques(covidData_WA)