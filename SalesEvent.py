'''
CS5001
Final project
Fall 2022
Chen Zhou
Sales Records in 2016 class
'''

class SalesEvent():
    '''
    Class: SalesEvent
    A class of property sales events.
    It incluses the properties' PIDs, sales records and latest values.
    It can interact with other classes to comapre values and calculate sales to assessment ratios 
    '''

    def __init__(self, pid, sales_record = [], latest_value = None):
        '''
        Constructor -- creates a property
        Parameters:
            self -- the current object
            pid -- the PID code of the property
            sales_record -- a list of lists of different sold time and sold price in order
            latest_value -- the latest sold price of the property
        Raise errors:
            TypeError -- the pid should be numbers connected by dashes
                         the sales_record should be a list
                         the latest_value should be an integer
            ValueError -- the latest_value should be positive
        '''
        if not pid.replace('-', '').isnumeric():
            raise TypeError("The pid should be numbers connected by dashes.")
        if not isinstance(sales_record, list):
            raise TypeError("The sales_record should be a list.")
        if not isinstance(latest_value, int):
            raise TypeError("The latest_value should be an integer.")
        if latest_value <= 0:
            raise ValueError("The latest value should be larger than 0.")

        self.pid = pid
        self.sales_record = sales_record
        self.value = latest_value 

    def number_of_sales(self):
        '''
        Method -- the number of sales records of a property
        Parameters:
            self -- the current object
        Returns an integer
        '''
        return len(self.sales_record)

    def __str__(self):
        '''
        Method -- print out the sales information of the property
        Parameters:
            self -- the current object
        Returns a string
        '''
        output = "The property {} had {} transactions in 2016, its latest price is {}.".format(self.pid, self.number_of_sales(), self.value)
        return output

    def __eq__(self, other):
        '''
        Method -- compares current sales event instance to another one
        Parameters:
            self -- the current object
            other -- other object
        Returns a Boolean: True if the current property's latest value is equal to the other property's latest value, False if not
        Raise errors:
            TypeError -- other should be SalesEvent when compare
        '''
        if not isinstance(other, SalesEvent):
            raise TypeError("other should be SalesEvent when compare")
        return self.value == other.value

    def __gt__(self, other):
        '''
        Method -- compares current sales event instance to another one
        Parameters:
            self -- the current object
            other -- other object
        Returns a Boolean: True if the current property's latest value is higher than the other property's latest value, False if not
        Raise errors:
            TypeError -- other should be SalesEvent when compare
        '''
        if not isinstance(other, SalesEvent):
            raise TypeError("other should be SalesEvent when compare")
        return self.value > other.value
