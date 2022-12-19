'''
CS5001
Final project
Fall 2022
Chen Zhou

Visualise Vancouver property data
'''


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from functions import *


ENTRIES = 2
EXPLODE = 0.2
NO_EXPLODE = 0
FIG_LENTH = 12
FIG_WIDTH = 8
LINE_WIDTH = 1
EDGE_COLOUR = "white"
START_ANGLE = 90
LEGEND_TITLE = "SAR Range:"
LEGEND_LOCATION = "lower right"
WEDGE_TEXT_SIZE = 8
WEDGE_TEXT_WEIGHT = "bold"
PIE_TITLE = "Statistics on Sales to Assessment Ratio(SAR)"
WIDTH = 0.2
RANK = 1
SOLD_INDEX = 1
ASSESSED_INDEX = 2
RATIO_INDEX = 3
BAR_COLOUR1 = 'r'
BAR_EDGE_COLOUR = 'grey'
BAR_LABEL1 = 'Sold Price'
BAR_COLOUR2 = 'g'
BAR_LABEL2 = 'Assessed Value'
XLABEL = 'Ranking'
YLABEL = 'Price'
YLABEL2 = 'Ratios'
FONTWEIGHT = 'bold'
FONTSIZE = 15
ROTATION = 30
PLOT_LABEL = 'Ratio'
MARKER = '*'
RATIO_LOW = 0
RATIO_HIGH = 3
BAR_TITLE = "Properties with the Highest Sales to Assessment Ratios(SARs)"
LEGEND2 = "upper right"
LEGEND3 = "upper left"
SMALL_EXPLODE = 0.2
BIG_EXPLODE = 0.5
EDGE_COLOUR2 = 'black'
SOLD_TITLE = 'Number of Properties with Different Number of Transactions'
SOLD_LOCATION = 'left'


#Make a simple pie chart >>>
def get_multiple_sales_results():
    '''
    Function -- get_multiple_sales_results
        purpose:  run functions to get the different sales results
    Parameters:
        None
    Return:
        a dictionary from function multiple_sales_statistics
    '''
    sales_list = create_van_sales_list(open_csv(VAN_PROPERTY_SALES_RECORDS_2016)) 
    sales_dictionary = create_sales_records_dict(sales_list)   
    sales_dictionary_cleaned = clean_sales_records_dict(sales_dictionary)
    sales_class = add_sales_data_into_class(sales_dictionary_cleaned)    
    sales_dictionary = count_number_of_sales(sales_class)
    return sales_dictionary

def make_pie_chart_for_sales(sales_dictionary):
    '''
    Function -- make_pie_chart_for_sales
        purpose:  make a pie chart for sales statistics result
    Parameters:
        sales_dictionary -- data for the pie chart
    Return:
        a pie chart
    Error:
        TypeError -- the parameter must be a dictionary
        IndexError -- sales_dictionary must have at least 2 entries to create a pie chart
    '''
    if not isinstance(sales_dictionary, dict):
        raise TypeError("The parameter sales_dictionary must be a dictionary.")
    if len(sales_dictionary) < ENTRIES:
        raise IndexError("The parameter sales_dictionary must have at least 2 entries to create a pie chart.")
    fig, ax = plt.subplots(figsize =(FIG_LENTH, FIG_WIDTH))
    wp = { 'linewidth' : LINE_WIDTH, 'edgecolor' : EDGE_COLOUR2 }
    myexplode = [NO_EXPLODE, SMALL_EXPLODE, BIG_EXPLODE]
    wedges, texts, ratiotexts = ax.pie(list(sales_dictionary.values()), autopct = lambda pct: format(pct, list(sales_dictionary.values())), labels = list(sales_dictionary.keys()), explode = myexplode, shadow = False, wedgeprops = wp)
    ax.legend(loc = LEGEND_LOCATION)
    plt.setp(ratiotexts, size = WEDGE_TEXT_SIZE, weight = WEDGE_TEXT_WEIGHT)
    ax.set_title(SOLD_TITLE, fontweight = FONTWEIGHT, loc = SOLD_LOCATION)
    plt.show()
#Make a simple pie chart <<<


def get_sar():
    '''
    Function -- get_sar
        purpose:  run functions to get the SARs
    Parameters:
        None
    Return:
        a list of lists with PIDs, sales prices, assessed prices and sales to assessment ratios
    '''
    improvement_list = create_big_improvement_list(open_csv(BC_PROPERTY_TAX_2018))
    property_value_dictionary = create_bc_property_value_dict(open_csv(BC_PROPERTY_TAX_2016))
    property_dictionary_cleaned = clean_bc_property_value_dict(property_value_dictionary)
    assessed_value_dictionary = create_bc_assessed_value_dict(property_dictionary_cleaned)
    sales_list = create_van_sales_list(open_csv(VAN_PROPERTY_SALES_RECORDS_2016)) 
    sales_dictionary = create_sales_records_dict(sales_list)   
    sales_dictionary_cleaned = clean_sales_records_dict(sales_dictionary)
    property_dictionary = create_van_property_dict(assessed_value_dictionary, sales_list)
    property = add_property_data_into_class(property_dictionary)
    sales = add_sales_data_into_class(sales_dictionary_cleaned)   
    assessed_prices_list = create_sales_and_assessed_price_list(property, sales)
    comparison_list = calculate_sar_list(assessed_prices_list)   
    sar_list = sar_list_without_big_improvement(comparison_list, improvement_list)
    return sar_list


#Make a pie chart >>>
def get_sar_statistic_results(sar_list):
    '''
    Function -- get_sar_statistic_results
        purpose:  run functions to get the ratio statistics
    Parameters:
        sar_list -- a list of lists
    Return:
        a dictionary result from statistics_dictionary function
    '''
    dictionary = count_sar_dict(sar_list)
    return dictionary

def format(pct, allvalues):
    '''
    Function -- format
        purpose:  change the format of numbers from absolute to percentage
    Parameters:
        pct -- a number shown in pie chart
        allvalues -- a list of numbers
    Return:
        a string
    Error:
        ValueError -- 'pct' parameter must be a number
        TypeError -- 'allvalues' parameter must be a list of numbers
    '''
    if not isinstance(pct, (int, float)):
        raise ValueError("The 'pct' parameter must be a number.")
    if not isinstance(allvalues, list):
        raise TypeError("The 'allvalues' parameter must be a list of numbers.")
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def make_pie_chart_for_sar(sar_dict):
    '''
    Function -- make_pie_chart_for_sar
        purpose:  make a pie chart for SARs statistics result
    Parameters:
        sar_dict -- data for the pie chart
    Return:
        a pie chart
    Error:
        TypeError -- the parameter must be a dictionary
    '''
    if not isinstance(sar_dict, dict):
        raise TypeError("The 'sar_dict' parameter must be a dictionary.")
    fig1, ax1 = plt.subplots(figsize =(FIG_LENTH, FIG_WIDTH))
    myexplode = [NO_EXPLODE, NO_EXPLODE, NO_EXPLODE, EXPLODE]
    wp = { 'linewidth' : LINE_WIDTH, 'edgecolor' : EDGE_COLOUR }
    wedges, texts, ratiotexts = ax1.pie(list(sar_dict.values()), autopct = lambda pct: format(pct, list(sar_dict.values())), labels = list(sar_dict.keys()), startangle = START_ANGLE, explode = myexplode, shadow = True, wedgeprops = wp)
    ax1.legend(title = LEGEND_TITLE, loc = LEGEND_LOCATION)
    plt.setp(ratiotexts, size = WEDGE_TEXT_SIZE, weight = WEDGE_TEXT_WEIGHT)
    ax1.set_title(PIE_TITLE, fontweight = FONTWEIGHT)
    plt.show()
#Make a pie chart <<<


#Make a bar chart >>>
def rank_sar_results(sar_list):
    '''
    Function -- rank_sar_results
        purpose:  run functions to get the highest ratio ranking
    Parameters:
        sar_list -- a list of lists
    Return:
        a list from the funciton highest_ratio_property_list
    '''
    highest_ratio_list = rank_sar_list(sar_list)
    return highest_ratio_list

def make_bar_chart_for_ranking(ratio_list, top_n):
    '''
    Function -- make_bar_chart_for_ranking
        purpose:  make a bar chart for top SARs
    Parameters:
        ratio_list -- a list of top ratios
        top_n -- an interger based on user input
    Return:
        a bar chart
    Error:
        TypeError -- 'ratio_list' parameter must be a list
                     'top_n' parameter must be an integer
    '''
    if not isinstance(ratio_list, list):
        raise TypeError("The 'ratio_list' parameter must be a list.")
    if not isinstance(top_n, int):
        raise TypeError("The 'top_n' parameter must be an integer.")
    width = WIDTH
    fig2 = plt.subplots(figsize =(FIG_LENTH, FIG_WIDTH))
    ranks = list()
    sales_prices = list()
    assessed_prices = list()
    ratios = list()
    rank = RANK
    for item in ratio_list[:top_n]:
        ranks.append(f"#{rank}")
        sales_prices.append(item[SOLD_INDEX])
        assessed_prices.append(item[ASSESSED_INDEX])
        rank += 1
        ratios.append(item[RATIO_INDEX])
    ind = np.arange(len(sales_prices))
    plt.bar(ind, sales_prices, width, color = BAR_COLOUR1, edgecolor = BAR_EDGE_COLOUR, label = BAR_LABEL1)
    plt.bar(ind + width, assessed_prices, width, color = BAR_COLOUR2, edgecolor =BAR_EDGE_COLOUR, label = BAR_LABEL2)
    plt.xlabel(XLABEL, fontweight = FONTWEIGHT, fontsize = FONTSIZE)
    y_axis_formatter = ticker.StrMethodFormatter("{x:,.0f}")
    plt.gca().yaxis.set_major_formatter(y_axis_formatter)
    plt.ylabel(YLABEL, fontweight = FONTWEIGHT, fontsize = FONTSIZE)
    plt.xticks([r + width/2 for r in range(len(ranks))], ranks, rotation = ROTATION)
    plt.legend(loc = LEGEND2)
    plt.twinx()
    plt.plot(ind + width/2, ratios, marker = MARKER, label = PLOT_LABEL)
    plt.ylabel(YLABEL2, fontweight = FONTWEIGHT, fontsize = FONTSIZE)
    plt.ylim([RATIO_LOW, RATIO_HIGH])
    plt.title(BAR_TITLE, fontweight = FONTWEIGHT)
    plt.legend(loc = LEGEND3)
    plt.show() 
#Make a bar chart <<<