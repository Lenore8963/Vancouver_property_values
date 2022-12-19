'''
CS5001
Final project
Fall 2022
Chen Zhou

Property 2016 class
'''

class Property():
    '''
    Class: Property
    A class of properties.
    It incluses the properties' PIDs, assessed values and addresses.
    It can comapre values and calculate sales to assessment ratios 
    '''

    def __init__(self, pid, value, address):
        '''
        Constructor -- creates a property
        Parameters:
            self -- the current object
            pid -- the PID code of the property
            value -- the assessed value of the property
            address -- the address of the property
        Raise errors:
            TypeError -- the pid should be numbers connected by dashes
                         the value should be an integer
                         the address should be a string
            ValueError -- the value should be positive
        '''
        if not pid.replace('-', '').isnumeric():
            raise TypeError("The pid should be numbers connected by dashes.")
        if not isinstance(value, int):
            raise TypeError("The value should be an integer.")
        if not isinstance(address, str):
            raise TypeError("The address should be a string.")
        if value <= 0:
            raise ValueError("The value should be larger than 0.")
        self.pid = pid
        self.value = value
        self.address = address
    
    def __str__(self):
        '''
        Method -- print out the information of the property
        Parameters:
            self -- the current object
        Returns a string
        '''
        output = "The property {} locating at {} had an assessed value of {}.".format(self.pid, self.address, self.value)
        return output

    def __eq__(self, other):
        '''
        Method -- compares current property instance to another one
        Parameters:
            self -- the current object
            other -- other object
        Returns a Boolean: True if the current property's value equals to the other property's value, False if not
        Raise errors:
            TypeError -- other should be Property when compare
        '''
        if not isinstance(other, Property):
            raise TypeError("other should be Property class object when compare")
        return self.value == other.value

    def __gt__(self, other):
        '''
        Method -- compares current property instance to another one
        Parameters:
            self -- the current object
            other -- other object
        Returns a Boolean: True if the current property's value is higher than the other property's value, False if not
        Raise errors:
            TypeError -- other should be Property when compare
        '''
        if not isinstance(other, Property):
            raise TypeError("other should be Property when compare")
        return self.value > other.value
