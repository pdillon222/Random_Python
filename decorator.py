#!/usr/local/bin/python3

__author__="James Dillon"

################################################################
#########################decorator.py###########################
##                                                            ##
## Write a function that writes some text to a file, and then ##
## decorate it with behavior that checks beforehand whether   ##
## the process has write access to the file.                  ##
##                                                            ##
################################################################
################################################################

def write_access(function):
    '''
    Decorator function, will check write access of chosen text output file
    '''
    from os import access,F_OK,W_OK
    from os.path import isdir
    def writer(path):
        #check if file exists, but is not writable
        if (access(path,F_OK) and not access(path,W_OK)):
            print("You do not have write access to {}".format(path))
            exit()
        #check if path is a directory, not a file
        elif isdir(path):
            print("{} is a directory, not a file".format(path))
            exit()
        #if file does not exist, check whether or not there is write access to parent directory
        elif not access(path,F_OK):
            try:
                with open(path,'a') as p:
                    assert access(path, F_OK)
            except PermissionError:
                print("File {} can not be created because you do not have write access to the chosen directory".format(path))
                exit()
        result=function(path)
        return result 
    return writer    

@ write_access
def write_to_file(path):
    '''
    Function will write user input to input path
    '''
    with open(path,'a') as p:
        print(input("Please enter text you would like to add to {}: ".format(path)),file=p,end="\n")

write_to_file(input("Please input a qualified file path, or specify new file for text output: "))
