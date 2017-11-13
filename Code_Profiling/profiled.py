#!/usr/local/bin/python3

'''#!/data/data/com.termux/files/usr/bin/python3'''

__author__="James Dillon"

#########################################################
#######################Parameters########################
#########################################################
##                                                     ##
## Implement a relatively fast method and a relatively ##
## slow method which both do the same work, and use    ## 
## profile or cProfile to time them.                   ##
##                                                     ##
#########################################################
#######################profile.py########################
#########################################################

import cProfile

class ProfTest():
    '''
    Object ProfTest will provide 3 separate methods for creating a list of the cubed roots of
    integers in range 1:10.  Final method will allow for cProfile testing of the various
    methods employed.    
    '''
    def __init__(self,iterable):
        '''iterable should be a range object'''
        self.iterable = iterable 
    
    def pmessage(self,method):
        prnt_strng = "Constructing a list of the cubed root of integers in range 1:5000 via {}".format(method)
        return "{}\n*{}*\n{}".format("*"*(len(prnt_strng)+2),prnt_strng,"*"*(len(prnt_strng)+2))    
        
    def for_testT(self):
        '''method to be tested, "T" added to end to be caught later'''
        lst = []
        print(ProfTest.pmessage(self,"for loop")) 
        for i in self.iterable:
            lst.append(i**(1.0/3))
        return lst        

    def while_testT(self):
        '''while method to be tested, "T" added to end to be caught later'''
        lst = []
        print(ProfTest.pmessage(self,"while loop w/ counter"))
        counter = 0
        while counter < len(list(self.iterable)):
            counter += 1
            lst.append(counter**(1.0/3))
        return lst       
 
    def comp_testT(self):
        '''comprehension method to be tested, "T" added to end to be caught later''' 
        print(ProfTest.pmessage(self,"list comprehension"))
        return [i**(1.0/3) for i in self.iterable]

    def profile_func(self,function):
        cProfile.run(str(function))

#instantiate the object as obj
obj=ProfTest(range(1,5000))

if __name__=="__main__":
     #as a reminder, using __name__=="__main__" allows object to be imported w/out being implicitly run
     print('\n'*2)
     for method in dir(obj):
        #loop will check obj methods for those ending in 'T', will run cProfile only on these obj methods
        if method[-1] == "T":
            method = "obj."+method+"()"
            cProfile.run(method)  
