#!/usr/local/bin/python3

'''#!/data/data/com.termux/files/usr/bin/python3'''

__author__="James Dillon"

#############################################################
#############################################################
# /usr/abrick/resources/urantia: a book written by aliens...#
#...What is the greatest integer in this text?              #
# explore different methods for going about doing this      #
# test the speed of different methods:                      #
# re.search, re.sub, re.compile, str.replace, try/except    #
#############################################################
#############################################################

import cProfile

class TestMethods():

    def __init__(self,textfile):
        self.textfile = open(textfile,'r')

    def readlist(self):
        '''
        read file line by line
        list comprehension, replacing ',' with '' (removing commas)
        for loop, through list result w/ try except block converting strings to ints where viable
        '''
        self.textfile.seek(0)
        maxlist=[0]
        for line in self.textfile:
            for i in [stri.replace(',','') for stri in line.split()]:
                try:
                    if int(i) > maxlist[0]:
                        maxlist[0] = int(i)
                except ValueError:
                    continue
        return maxlist[0]

    def loadlinelist(self):
        '''   
        list comprehension generated from string file read() method, and re.findall()
        '''
        import re
        self.textfile.seek(0)
        return max([int(i) for i in re.findall(r'\d{1,}',self.textfile.read().replace(",",""))])

    def testfunction(self,function):
        cProfile.run(function)                

tester=TestMethods('urantia')#instantiating the TestMethods object with the urantia file as target
########################################
#Testing the readlist() method;should be fairly slow 
tester.testfunction('tester.readlist()')
print("Displaying function output: {}".format(tester.readlist()))
#Testing the loadlinelist method;should be fairly fast
tester.testfunction('tester.loadlinelist()')
print("Displaying function output: {}".format(tester.loadlinelist()))

