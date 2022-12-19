'''
CS5001
Final project
Fall 2022
Chen Zhou

Functions clean Vancouver property data,
parse data into objects,
compare sold value with assessed value,
analyse top anomalous sales in prices and number of transactions
'''

VAN_PROPERTY_SALES_RECORDS_2016 = 'https://openhousing.ca/wp-content/uploads/2022/11/vanresales2016.csv'
BC_PROPERTY_TAX_2016 = 'https://opendata.vancouver.ca/explore/dataset/property-tax-report-2016-2019/download/?format=csv&refine.report_year=2016&timezone=America/Los_Angeles&lang=en&use_labels_for_header=true&csv_separator=%3B'
BC_PROPERTY_TAX_2018 = 'https://opendata.vancouver.ca/explore/dataset/property-tax-report-2016-2019/download/?format=csv&refine.report_year=2018&timezone=America/Los_Angeles&lang=en&use_labels_for_header=true&csv_separator=%3B'


FIRST_CONTENT_LINE = 1
LAST_CONTENT_LINE = -1
PID_COLUMN = 0
BIG_IMPROVEMENT_COLUMN = 25
BIG_IMPROVEMENT_YEAR = '2016'
LAND_VALUE_COLUMN = 17
IMPROVEMENTS_LALUE_COLUMN = 18
LAND_VALUE_INDEX = 0
IMPROVEMENT_VALUE_INDEX = 1
SALES_CONTENT_FIRST_LINE = 50
ADDRESS_COLUMN = 1
SOLD_DATE_COLUMN = 2
SOLD_PRICE_COLUMN = 3
CONTENT_START = 1
CONTENT_END = -1
PID_INDEX = 0
ADDRESS_INDEX = 1
SOLD_DATE_INDEX = 2
SOLD_PRICE_INDEX = 3
ASSESSED_VALUE_INDEX = 0
LAST_LIST = -1
LATEST_VALUE_INDEX = 1
SOLD_INDEX = 1
ASSESSED_INDEX = 2
RATIO_INDEX = 3
REVERSE = -1
EXTREMELY_HIGH_RATIO = 100
TOP_RANKING = 1
SALES_NUMBER_INDEX = 1
ONE_SALES = 1
RATIO_INDEX = 3
ONE_POINT_FIVE_TIMES_THE_RATIO = 1.5
ONE_POINT_TWENTY_FIVE_TIMES_THE_RATIO = 1.25
ONE_TIME_THE_RATIO = 1.0
FIRST_PART = '< 1.0'
SECOND_PART = '1.0 - 1.25'
THIRD_PART = '1.25 - 1.5'
FOURTH_PART = '> 1.5'
TOP_TEN = 10
COUNT_START = 0
ONE_TIME = 1
TWICE = 2
THREE_TIMES = 3

import requests
from requests.exceptions import HTTPError
from dateutil import parser
from Property import Property
from SalesEvent import SalesEvent


def open_csv(data_link):
    '''
    Function -- open_csv
        purpose: read the content of .csv file online
    Parameters:
        data_link -- a string of online .csv file link
    Return:
        the content in the .csv file
    Error:
        ValueError -- data_link must be a string
        HTTPError -- HTTP error occur in opening the web url
        ConnectionError -- Connection error occurred in opening the web url
    '''
    try:
        if not isinstance(data_link, str):
            raise ValueError("data_link must be a string")
        response = requests.get(data_link)
        content = response.text
        return content
    except HTTPError:
        raise HTTPError("HTTP error occurred in opening: ", data_link)
    except ConnectionError:
        raise ConnectionError("Connection error occurred: ", data_link) 


# This part is to clean the data from BC_PROPERTY_TAX_2016 and calculate the assessed values>>>
def create_bc_property_value_dict(property_data):
    '''
    Function -- create_bc_property_value_dict
        purpose: create a dictionary of property values in BC
    Parameters:
        property_data -- a string containing the data from a CSV file
    Return:
        a dictionary with PIDs as keys and land_values and improvements_values as values
    Error:
        TypeError -- the parameter should be a string
        IndexError -- not enough data in the property tax file
    '''
    if not isinstance(property_data, str):
        raise TypeError ("The parameter of create_bc_property_value_dict should be a string.")
    property_value_dict = {}
    property_list = property_data.split('\n')
    for line in property_list[FIRST_CONTENT_LINE: LAST_CONTENT_LINE]:
        line_list = line.split(';')
        if len(line_list) <= IMPROVEMENTS_LALUE_COLUMN:
            raise IndexError('Not enough data in the property tax file. Check for missing values in the file.')
        pid = line_list[PID_COLUMN]
        land_value = line_list[LAND_VALUE_COLUMN].replace(',', '')
        improvements_value = line_list[IMPROVEMENTS_LALUE_COLUMN].replace(',', '')
        property_value_dict[pid] = [land_value] + [improvements_value]
    return property_value_dict  

def clean_bc_property_value_dict(property_dict):
    '''
    Function -- clean_bc_property_value_dict
        purpose: delete bad data whose price columns are not numeric
    Parameters:
        property_dict -- a dictionary uncleaned
    Return:
        a cleaned dictionary with PIDs as keys and land_values and improvements_values as values
    Error:
        TypeError -- the parameter should be a dictionary
    '''  
    if not isinstance(property_dict,dict):
        raise TypeError("Function clean_bc_property_value_dict takes a dictionary")      
    keys = property_dict.keys()
    bad_data_keys = list()
    for pid in keys:
        if not property_dict[pid][LAND_VALUE_INDEX].isnumeric():
            bad_data_keys += [pid]
    for bad_key in bad_data_keys:
        del property_dict[bad_key]
    return property_dict

def create_bc_assessed_value_dict(cleaned_property_dict):
    '''
    Function -- create_bc_assessed_value_dict
        purpose: add land_values and improvements_values to get assessed_values
    Parameters:
        cleaned_property_dict -- a dictionary cleaned
    Return:
        a dictionary with PIDs as keys and assessed_values integers as values
    Error:
        TypeError -- the parameter should be a dictionary
        ValueError -- land value and improvement value should be numbers.
        Index Error -- not enough data in the property value dictionary
    '''  
    if not isinstance(cleaned_property_dict,dict):
        raise TypeError("Function create_bc_assessed_value_dict takes a dictionary")
    assessed_value_dict = dict()
    try:
        for pid in cleaned_property_dict.keys():
            if len(cleaned_property_dict[pid]) <= IMPROVEMENT_VALUE_INDEX:
                raise IndexError('Not enough data in the property value dictionary.')
            assessed_value = int(cleaned_property_dict[pid][LAND_VALUE_INDEX]) + int(cleaned_property_dict[pid][IMPROVEMENT_VALUE_INDEX])
            assessed_value_dict[pid] = assessed_value
        return assessed_value_dict
    except ValueError:
        raise ValueError('Land value and improvement value should be numbers.')
# This part is to clean the data from BC_PROPERTY_TAX_2016 and calculate the assessed values <<<


# This part is to clean the data from VAN_PROPERTY_SALES_RECORDS_2016 >>>
def create_van_sales_list(sales_data):
    '''
    Function -- create_van_sales_list
        purpose: make sales records in Vancouver into a list of lists
    Parameters:
        sales_data -- strings from a .csv file
    Return:
        a list of lists with PIDs, addresses, sold_dates as strings and sold_prices as integers
    Error:
        TypeError -- the parameter should be a string
        ValueError -- dates and prices should be in the right format
        IndexError -- not enough data in the Vancouver sales records file
    '''
    if not isinstance(sales_data, str):
        raise TypeError ("The parameter of create_van_sales_list should be a string.")
    sales = list()
    sales_data_list = sales_data.split('\n')
    try:
        for line in sales_data_list[SALES_CONTENT_FIRST_LINE: LAST_CONTENT_LINE]: #The first 51 lines in the VAN_PROPERTY_SALES_RECORDS_2016 file are duplictates and with format errors.
            line_list = line.split('","')
            if len(line_list) <= SOLD_PRICE_COLUMN:
                raise IndexError('Not enough data in the Vancouver sales records file.')            
            pid = line_list[PID_COLUMN].replace('"', '')       
            address = line_list[ADDRESS_COLUMN]
            date = parser.parse(line_list[SOLD_DATE_COLUMN]).strftime('%d-%m-%Y')
            sold_price = int(line_list[SOLD_PRICE_COLUMN][CONTENT_START: CONTENT_END].replace(',', ''))
            sales += [[pid] + [address] + [date] + [sold_price]]
        return sales
    except ValueError:
        raise ValueError("Something is wrong in the sales data")

def create_sales_records_dict(van_sales_list):
    '''
    Function -- create_sales_records_dict
        purpose: a dictionary of Vancouver property sales records
    Parameters:
        van_sales_list -- a list of lists
    Return:
        a dictionary with PIDs as keys and a list of property sold times and prices lists as values
    Error:
        TypeError -- the parameter should be a list
        IndexError -- not enough data in the Vancouver sales records list
    '''
    if not isinstance(van_sales_list, list):
        raise TypeError("The parameter of function create_sales_records_dict should be a list")
    sales_records_dic = dict()
    for i in range(len(van_sales_list)):
        if len(van_sales_list[i]) <= SOLD_PRICE_INDEX:
            raise IndexError('Not enough data in the Vancouver sales records list.') 
        if van_sales_list[i][PID_INDEX] not in sales_records_dic.keys():
            sales_records_dic[van_sales_list[i][PID_INDEX]] = [[van_sales_list[i][SOLD_DATE_INDEX]] + [van_sales_list[i][SOLD_PRICE_INDEX]]]
        else:
            sales_records_dic[van_sales_list[i][PID_INDEX]].append([van_sales_list[i][SOLD_DATE_INDEX]] + [van_sales_list[i][SOLD_PRICE_INDEX]])
    return sales_records_dic

def clean_sales_records_dict(sales_records_dic):
    '''
    Function -- clean_sales_records_dict
        purpose: clean the dictionary of Vancouver property sold records, put the sold times in order, remove duplicates
    Parameters:
        sales_records_dic -- a dictionary
    Return:
        a dictionary with PIDs as keys and a list of lists of property sold times(from earlier to later) and prices as values without duplicates
    Error:
        TypeError -- the parameter should be a dictionary
    '''
    if not isinstance(sales_records_dic, dict):
        raise TypeError("The parameter of function clean_sales_records_dict should be a dictionary")
    for key, value in sales_records_dic.items():
        value_new = list()
        [value_new.append(x) for x in value if x not in value_new]
        value_new_sorted = sorted(value_new)
        sales_records_dic[key] = value_new_sorted
    return sales_records_dic
# This part is to clean the data from VAN_PROPERTY_SALES_RECORDS_2016 <<<


# This part is to combine the data from two files together and put it in different classes >>>
def create_van_property_dict(bc_assessed_value_dict, van_sales_list):
    '''
    Function -- create_van_property_dict
        purpose: make a dictionary of Vancouver property data
    Parameters:
        bc_assessed_value_dict -- a dictionary of BC propperty records
        van_sales_list -- a list of sales records in Vancouver
    Return:
        a dictionary of PIDs as keys and assessed values and addresses as values
    Error:
        TypeError -- the first parameter should be a dictionary
                     the second parameter should be a list
        IndexError -- not enough data in the Vancouver sales records list
    '''  
    if not isinstance(bc_assessed_value_dict, dict):
        raise TypeError("The first parameter of function create_van_property_dict should be a dictionary")
    if not isinstance(van_sales_list, list):
        raise TypeError("The second parameter of function create_van_property_dict should be a list")
    van_property_dict = dict()
    for i in range(len(van_sales_list)):
        if len(van_sales_list[i]) <= ADDRESS_INDEX:
            raise IndexError('Not enough data in the Vancouver sales records list.')
        if van_sales_list[i][PID_INDEX] in bc_assessed_value_dict.keys():
            van_property_dict[van_sales_list[i][PID_INDEX]] = [bc_assessed_value_dict[van_sales_list[i][PID_INDEX]]] + [van_sales_list[i][ADDRESS_INDEX]]
    return van_property_dict

def add_property_data_into_class(van_property_dict):
    '''
    Function -- add_property_data_into_class
        purpose: put Vancouver property data into a class
    Parameters:
        van_property_dict -- a dictionary
    Return:
        a dictionary of Property class objects
    Error:
        TypeError -- the parameter should be a dictionary
    '''
    if not isinstance(van_property_dict, dict):
        raise TypeError("The first parameter of function add_property_data_into_class should be a dictionary")
    property_dictionary = dict()
    for pid, value in van_property_dict.items():
        property_dictionary[pid] = Property(pid, value[ASSESSED_VALUE_INDEX], value[ADDRESS_INDEX])
    return property_dictionary

def add_sales_data_into_class(sales_records_dict_cleaned):
    '''
    Function -- add_sales_data_into_class
        purpose: put Vancouver sales records data into a class
    Parameters:
        sales_records_dict_cleaned -- a dictionary
    Return:
        a dictionary of SalesEvent class objects
    Error:
        TypeError -- the parameter should be a dictionary
        IndexError -- not enough data in the selling record
    '''
    if not isinstance(sales_records_dict_cleaned, dict):
        raise TypeError("The first parameter of function add_sales_data_into_class should be a dictionary")
    records_dictionary = dict()
    for pid, value in sales_records_dict_cleaned.items():
        if len(value[LAST_LIST]) <= LATEST_VALUE_INDEX:
            raise IndexError('Not enough data in the selling record.')
        records_dictionary[pid] = SalesEvent(pid, value, value[LAST_LIST][LATEST_VALUE_INDEX])
    return records_dictionary
# This part is to combine the data from two files together and put it in different classes <<<


# This part is for a rapid data visualization with objects from one class >>>
def count_number_of_sales(sales_event_class):
    '''
    Function -- count_number_of_sales
        purpose: make a dictionary of diffrent sold times for data visualization
    Parameters:
        sales_event_class -- a dictionary of SalesEvent class objects
    Return:
        a dictionary with strings of different sold times as keys and the mumber of properties of different sold times as values
    Error:
        TypeError -- the parameter should be a dictionary
                     the item in the list should be class objects
    '''
    if not isinstance(sales_event_class, dict):
        raise TypeError("The parameter of function count_number_of_sales should be a dictionary")
    one_time = COUNT_START
    twice = COUNT_START
    three_times = COUNT_START
    more_times = COUNT_START
    sales_statistics = dict()
    for item in sales_event_class.values():
        if not isinstance(item, SalesEvent):
            raise TypeError("The item in the list should be class objects")
        if item.number_of_sales() == ONE_TIME:
            one_time += 1
        elif item.number_of_sales() == TWICE:
            twice += 1
        elif item.number_of_sales() == THREE_TIMES:
            three_times += 1
        elif item.number_of_sales() > THREE_TIMES:
            more_times += 1
    if one_time > COUNT_START:
        sales_statistics['one_time'] = one_time
    if twice > COUNT_START:
        sales_statistics['twice'] = twice
    if three_times > COUNT_START:
        sales_statistics['three_times'] = three_times
    if more_times > COUNT_START:
        sales_statistics['more_times'] = more_times
    return sales_statistics
# This part is for a rapid data visualization with objects from one class <<<


# This part is to use objects from twe classes to prepare the data for SAR visualization >>>
def create_sales_and_assessed_price_list(property_class, sales_event_class):
    '''
    Function -- create_sales_and_assessed_price_list
        purpose: put sales price and assessed price of each property together as a list
    Parameters:
        property_class -- a dictionary
        sales_event_class -- a dictionary
    Return:
        a list of lists with PIDs, sales prices and assessed prices
    Error:
        TypeError -- the parameters should be a dictionary
                     the values in the parameters should be class objects
        IndexError -- not enough data in the SalesEvent class
    '''
    if not isinstance(property_class, dict):
        raise TypeError("The first parameter of function create_sales_and_assessed_price_list should be a dictionary")
    if not isinstance(sales_event_class, dict):
        raise TypeError("The second parameter of function create_sales_and_assessed_price_list should be a dictionary")  
    sales_and_assessed_list = list()
    for key, value in sales_event_class.items():
        if key in property_class.keys():
            if not isinstance(value, SalesEvent):
                raise TypeError("The values in the parameters should be class objects.")
            for i in range(len(value.sales_record)):
                if not isinstance(property_class[key], Property):
                    raise TypeError("The values in the parameters should be class objects.")
                if len(value.sales_record[i]) <= SOLD_INDEX:
                    raise IndexError('Not enough data in the SalesEvent class.')
                sales_and_assessed_list.append([key] + [value.sales_record[i][SOLD_INDEX]] + [property_class[key].value])
    return sales_and_assessed_list

def calculate_sar_list(sales_and_assessed_prices_list):
    '''
    Function -- calculate_sar_list
        purpose: calculate the sales to assessment ratios
    Parameters:
        sales_and_assessed_price_list -- a list of lists
    Return:
        a list of lists with PIDs, sales prices, assessed prices and sales to assessment ratios
    Error:
        TypeError -- the parameter should be a list
        ValueError -- the values should be numbers
        ZeroDivisionError -- the assessed value should not be zero
        IndexError -- not enough data in the sales and assessed list
    '''
    if not isinstance(sales_and_assessed_prices_list, list):
        raise TypeError("The parameter of function calculate_sar_list should be a list")
    sar_list = list()
    try:
        for price_list in sales_and_assessed_prices_list:
            price_ratio = int(price_list[SOLD_INDEX]) / int(price_list[ASSESSED_INDEX])
            price_ratio = float(format(price_ratio, '.3f'))
            price_list.append(price_ratio)
            sar_list += [price_list]   
        return sar_list
    except IndexError:
        raise IndexError('Not enough data in the sales and assessed list.')
    except ValueError:
        raise ValueError("The values should be numbers")
    except ZeroDivisionError:
        raise ZeroDivisionError("The assessed value should not be zero")

def create_big_improvement_list(property_data):
    '''
    Function -- create_big_improvement_list
        purpose: make a list of properties which made big improvement in 2016 using the 2018 BC property file
    Parameters:
        property_data -- strings of contents in a .csv file
    Return:
        a list of strings
    Error:
        TypeError -- the parameter should be a string
        IndexError -- not enough data in the property tax file
    '''
    if not isinstance(property_data, str):
        raise TypeError ("The parameter should be a string.")
    big_improvement_list = list()
    property_tax_list = property_data.split('\n')
    for line in property_tax_list[FIRST_CONTENT_LINE: LAST_CONTENT_LINE]:
        line_list = line.split(';')
        if len(line_list) <= BIG_IMPROVEMENT_COLUMN:
            raise IndexError('Not enough data in the property tax file.')
        pid = line_list[PID_COLUMN]
        big_improvement_year = line_list[BIG_IMPROVEMENT_COLUMN]
        if big_improvement_year == BIG_IMPROVEMENT_YEAR:
            big_improvement_list.append(pid)
    return big_improvement_list

def sar_list_without_big_improvement(sar_list, big_improvement_list):
    '''
    Function -- sar_list_without_big_improvement
        purpose: delete the properties which made big improvements in 2016
    Parameters:
        sar_list -- a list of lists
        big_improvement_list -- a list
    Return:
        a list of lists with PIDs, sales prices, assessed prices and sales to assessment ratios
    Error:
        TypeError -- the first parameter should be a list
                     the second parameter should be a list
                     the ratio should be a float
        IndexError -- not enough data in the sar list
    '''
    if not isinstance(sar_list, list):
        raise TypeError("The first parameter of function sar_list_without_big_improvement should be a list")
    if not isinstance(big_improvement_list, list):
        raise TypeError("The second parameter of function sar_list_without_big_improvement should be a list")
    new_list = list()
    try:
        for comparison in sar_list:       
            if comparison[PID_INDEX] not in big_improvement_list:
                if comparison[RATIO_INDEX] < EXTREMELY_HIGH_RATIO: # There is an obvious bad data with very low land price(2 dollars)
                    new_list.append(comparison)
        return new_list
    except IndexError:
        raise IndexError("Not enough data in the sar list.")
    except TypeError:
        raise TypeError("The ratio should be a float")

def count_sar_dict(sar_list_without_big_improvement):
    '''
    Function -- count_sar_dict
        purpose:  make a dictionary about statistic of different sales to assessment ratios in 2016
                  Later for data visualization use
    Parameters:
        sar_list_without_big_improvement -- a list of lists
    Return:
        a dictionary with different ratio strings as keys and number of properties as values
    Error:
        TypeError -- the parameter should be a list
                     the ratio should be a float
        IndexError -- not enough data in the sar list
    '''
    if not isinstance(sar_list_without_big_improvement, list):
        raise TypeError("The parameter of count_sar_dict should be a list")
    sar_dictionary = dict()
    first_part = list()
    second_part = list()
    third_part = list()
    fourth_part = list()
    try:
        for comparison_list in sar_list_without_big_improvement:
            if comparison_list[RATIO_INDEX] > ONE_POINT_FIVE_TIMES_THE_RATIO:
                fourth_part += [comparison_list]
            elif comparison_list[RATIO_INDEX] >= ONE_POINT_TWENTY_FIVE_TIMES_THE_RATIO:
                third_part += [comparison_list]
            elif comparison_list[RATIO_INDEX] >= ONE_TIME_THE_RATIO:
                second_part += [comparison_list]
            elif comparison_list[RATIO_INDEX] < ONE_TIME_THE_RATIO:
                first_part += [comparison_list]
    except IndexError:
        raise IndexError('Not enough data in the sar list.')
    except TypeError:
        raise TypeError("The ratio should be a float")
    sar_dictionary[FIRST_PART] = len(first_part)
    sar_dictionary[SECOND_PART] = len(second_part)
    sar_dictionary[THIRD_PART] = len(third_part)
    sar_dictionary[FOURTH_PART] = len(fourth_part)
    return sar_dictionary

def rank_sar_list(sar_list_without_big_improvement):
    '''
    Function -- rank_sar_list
        purpose: sort the sales to assessment ratios from the highest to the lowest
    Parameters:
        sar_list_without_big_improvement -- a list of lists
    Return:
        a list of lists with PIDs, sales prices, assessed prices and sales to assessment ratios, in the order from highest sales to assessment ratio to the lowest
    Error:
        TypeError -- the parameter should be a list
        ValueError -- the ratio should be a number
        IndexError -- not enough data in the sar list
    '''
    if not isinstance(sar_list_without_big_improvement, list):
        raise TypeError("The parameter of function rank_sar_list should be a list")
    try:
        sorted_list = sorted(sar_list_without_big_improvement, key = lambda x: float(x[RATIO_INDEX]), reverse=True)   
        return sorted_list
    except IndexError:
        raise IndexError('Not enough data in the sar list.')
    except ValueError:
        raise ValueError("The ratio should be a number")
# This part is to use objects from twe classes to prepare the data for SAR visualization <<<