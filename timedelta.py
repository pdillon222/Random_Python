#!/usr/local/bin/python3

__author__="James Dillon"
##############################################################
##########################PARAMETERS##########################
##                                                          ##
## Calculate the time elapsed between consecutive events in ##
## the Apache access log                                    ##
##                                                          ##
##############################################################
##############################################################

import datetime, calendar, re

#create generator object of Apache access log file
f = (line.rstrip() for line in open('/var/www/logs/access_log'))

#will utilize hash table of month abbreviations per integer equivalent
month_dict={v:i for i,v in enumerate(list(calendar.month_abbr))}

#will be transformed into a que for elapsed calculations
lst = []

def pushpop(entry,structure):
    #function will transform empty list into a que
    #adds to front, exits back
    #will allow for calculation, resulting in timedelta object
    if len(structure) == 2:
        structure.insert(0,entry)
        structure.pop()
    else:
        structure.insert(0,entry)

def log_iterate(iterations):
    #transform the log entries, to extract time info and message info
    for i in range(iterations):
        try:
            proceed = next(f)
            proceed = re.split('.*(\[.*?")\s.*',proceed)[1]
            dateform = re.split('.*\[(.*) .*\].*',proceed)[1].replace('/',':').split(':')
            for i in [2,1,0,3,4,5]:
                dateform.append(dateform[i])
            dateform = dateform[6:]
            dateform[1] = month_dict[dateform[1]]
            dateform = [int(i) for i in dateform]
            dateform = datetime.datetime(*dateform) #convert to datetime object
            log_tuple=(dateform,proceed)
            pushpop(log_tuple,lst)
            if len(lst) == 2:
                print(lst[-1][1],lst[-1][0])
                print("^"*5)
                print(lst[0][1],lst[0][0])
                print("Time Elapsed =",lst[0][0]-lst[-1][0],"\n","*"*5)
            else:
                print("Time elapsed between current date/time and initial log event: {}{}{}".format(lst[0][-1],"= \n",datetime.datetime.now()-lst[0][0]))
        except StopIteration:
            break

def iter_prompt():
    #catch user input error, force integer input
    try:
        iterations = int(input("How many log entries would you like to calculate time differences for: "))
    except:
        print("Please enter integers only")
        iterations = iter_prompt()
    return iterations

def parsefile():
    #allow for the generator to be consecutively accessed
    log_iterate(iter_prompt())
    while True:
        prompt = input("Would you like to calculate more times between log events?[Y|N]: ")
        if prompt.upper() == "Y":
            log_iterate(iter_prompt())
        else:
            break
parsefile()

