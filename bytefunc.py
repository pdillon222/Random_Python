#!/usr/local/bin/python3

__author__="James Dillon"

##########################################################################################
##########################################################################################
##  Write a program that expects as its argument the path to another Python program.    ##
##  Indicate how many unique bytecodes are used in it, and which one is the most common ##
##########################################################################################
##########################################################################################

import dis

def getprog(pyprog):
    '''
    Ensure the user is selecting a Python file
    '''
    while pyprog.upper()[-2]+pyprog.upper()[-1] != 'PY':
        pyprog=getprog(input("Not a recognized python program,try again: "))
    return pyprog

def bytecodes(program):
    '''
    Break chosen program down into bytecodes
    Count number of instances for each
    Return count display, and bytecode w/ max count
    '''
    #implement the count dictionary
    collect_dict = {}
    for line in dis.Bytecode((open(program,'r').read())):
        if line[0]+"="+str(line[1]) not in collect_dict:
            collect_dict[line[0]+"="+str(line[1])]=1
        else:
            collect_dict[line[0]+"="+str(line[1])]+=1
    return program, collect_dict, max([(v,k) for k,v in collect_dict.items()])
    
progname,code_dict,maxcode=bytecodes(getprog(input("Please enter a readable path to a python file: ")))
########################################################################################################
###############################################_Print_Section_##########################################
########################################################################################################
print("*"*20)                                                                                         ##
print("* Unique bytecodes and counts in {}: ".format(progname))                                      ##
print("*"*20)                                                                                         ##
for k,v in code_dict.items():                                                                         ##
    print("{};count = {}".format(k,v))                                                                ##
print("*"*20)                                                                                         ##
print("* The most common bytecode is {}, its count is: {}".format(maxcode[1],maxcode[0]))           ##  
print("*"*20)                                                                                         ##
########################################################################################################
########################################################################################################
########################################################################################################
