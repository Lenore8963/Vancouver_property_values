'''
CS5001
Final project
Fall 2022
Chen Zhou

Driver of Vancouver property data analysis
Main menu
'''

from data_visualization import *

BACK = 'B'
RANK_FIRST = 1
RANK_ONE_HUNDREDTH = 100
QUIT = 'Q'
PRINT_MENU = 'P'
BACKGROUND = 'B'
RANKING = 'R'
STATISTIC = 'S'
TRANSACTION = 'T'


def print_menu():
    '''
    Function -- print_menu
        purpose:  print out a main menu for the user
    Parameters:
        None
    Return:
        None
    '''
    print("""Here are some interesting findings of Vancouver properties in 2016:
Type "P" to print this menu again!
Type "B" to read the background info again!
Type "T" to get the Statistics on different sold times!
Type "S" to get the Statistics on SAR!
Type "R" to check the rankings of SAR!
Type "Q" to quit!
""")

def print_background():
    '''
    Function -- print_background
        purpose:  print out some background information of this project for the user
    Parameters:
        None
    Return:
        None
    '''
    print("""What is PID? This is a unique code for every property in British Columbia!
What is SAR? This is Sales to Assessment Ratio! 
We use it to measure the difference between sold prices and government assessed values.
And it's a good way to spot an anomalous sale!
Maybe someone is using real estate for illegal profit, who knows!
""")

def show_rankings():
    '''
    Function -- show_rankings
        purpose:  show a bar chart of ranking results based on user options
    Parameters:
        None
    Return:
        None
    '''
    option = input("""How many results would you like to check(1 - 100)?
(recommend: integers from 1 to 50.)
Enter "B" to get back to the main menu.\n""")
    while option != BACK:
        if not option.isdigit():
            option = input("I'm sorry, that's not a valid option. Please enter a positive integer.\n")
        elif int(option) > RANK_ONE_HUNDREDTH:
            option = input("I'm sorry, that's not a valid option. Please enter an integer between 1 to 100.\n")
        elif int(option) >= RANK_FIRST:
            print("Please wait a moment, this may take some time.")
            sar = get_sar()
            ranking_list = rank_sar_results(sar)
            make_bar_chart_for_ranking(ranking_list, int(option))
            option = input("""How many results would you like to check?
(recommend: integers from 1 to 50.)
Enter "B" to get back to the main menu.\n""")
        else:
            option = input("I'm sorry, that's not a valid option. Please enter a positive integer.\n")
    run_menu()  

def run_menu():
    '''
    Function -- run_menu
        purpose:  show some property results based on user options
    Parameters:
        None
    Return:
        None
    '''
    print_menu()
    print_background()
    option = input("Which option would you like?\n")
    while option != QUIT:
        if option == PRINT_MENU:
            print_menu()
            option = input("Which option would you like?\n")
        elif option == BACKGROUND:
            print_background()
            option = input("Which option would you like?\n")
        elif option == TRANSACTION:
            print("Please wait a moment, this may take some time.")
            statistic = get_multiple_sales_results()
            make_pie_chart_for_sales(statistic)
            option = input("Which option would you like?\n")
        elif option == STATISTIC:
            print("Please wait a moment, this may take some time.")
            sar = get_sar()
            graph_dict = get_sar_statistic_results(sar)
            make_pie_chart_for_sar(graph_dict)
            option = input("Which option would you like?\n")
        elif option == RANKING:
            show_rankings()
            option = input("Which option would you like?\n")
        else:
            option = input("I'm sorry, that's not a valid option. Please choose from the valid menu choices.\n")
    print("Good bye!")

def main():
    run_menu()
    
if __name__ == "__main__":
    main()
