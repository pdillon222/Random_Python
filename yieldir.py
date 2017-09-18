#!/usr/local/bin/python3

__author__="James Dillon"

###################################regressdir.py##############################
###################################PARAMETERS:################################
# write a function that, given a directory, yields all the files it contains,#
# recursively. Make sure to catch PermissionError and distinguish between    #
# relative and absolute paths.                                               #
##############################################################################
##############################################################################

import os

def pathselection():
    '''
    Allows for user specification of directory, contents of which are to be recursively listed
    '''
    pathchoice=input("Please select a directory, for a list of all files and subdirectories within: ")
    return pathchoice

def checkdirperms(directory):
    '''
    Will throw an error, but allow for another input attempt if:
        >User does not have executable permissions to directory
        >User does not have read permissions for directory
        >Input is not an absolute path to a directory, or directory is not accessible from present location
        >Input is not a directory
    '''
    if not os.access(directory,os.F_OK): #check for existence of input
        print("Specified directory does not exist, please try again.")
        directory=checkdirperms(pathselection())
    elif not os.access(directory,os.R_OK): #check for read access by user
        print("You do not have read permissions for specified directory, please try another.")
        directory=checkdirperms(pathselection())
    elif not os.access(directory,os.X_OK): #check for executable permissions by user
        print("You do not have executable permissions for specified directory, please try another.")
        directory=checkdirperms(pathselection())
    elif not os.path.isdir(directory): #confirmation that input is a directory
        print("{} is not a directory, please try again.".format(directory))
        directory=checkdirperms(pathselection())
    return directory

def descend(path):
    '''
    Generator function will display contents of initial directory given as its argument
    Function will descend into any directories found (assuming user permissions permit)
    Function will recursively repeat this process until the end of each branch of the directory tree is found
    '''
    yield path 
    print("*Contents of {}:\n".format(path)) #initial contents of directory
    print("\n".join(list(map(lambda x: " "*5+os.path.abspath(path)+"/"+x,os.listdir(path))))+"\n") 
    for i in os.listdir(path):
        i = os.path.abspath(path)+"/"+i #abspath chops the parent directory, converging file and parent dir
        if os.path.isdir(i):
            try:
                print("**Attempting descent into {}--\n".format(i))
                yield from descend(i) #allows for recursion of generator object
            except PermissionError:
                print("\n!!Insufficient user permissions for directory {}, skipping.\n".format(i))          
 
descent=descend(checkdirperms(pathselection()))

while descent:
    try:
        next(descent)
    except StopIteration:
        break
