#!/usr/local/bin/python3

__author__="James Dillon"

import cProfile, sys, os, threading 
from concurrent import futures
from functools import partial

###########################################################
######################threadpool.py######################## 
########################################################### 
##                                                       ##
##  Show whether process parallelism makes a multi-grep  ## 
##  faster than thread parallelism or no parallelism     ##
##                                                       ##
###########################################################
###########################################################
###########################################################

pool=futures.ThreadPoolExecutor()

#Handling initial arguments
#############################################################################################################
#immediately exit program with usage message if no arguments entered
if sys.argv[0].startswith("./"): strp_arg = str(sys.argv[0])[2:]
if len(sys.argv) < 3:
    print('\n','ERROR!!--{sys:} USAGE: python3 {sys:} \
"search string" file1 [file2 file3 file4]'.format(sys=strp_arg))
    print("Please run {} with at least two arguments: \
\n   1): a string of text to be searched for \
\n   2): at least 1 readable file as an argument\n".format(strp_arg))                                       
    exit()                                                                                                  
                                                                                                              
#list that has been checked for file existence as well as read permissions                                  
sys_trim=[filer for filer in sys.argv[2:] if os.access(filer,os.F_OK) == True and os.access(filer,os.R_OK)] 

#list of arguments that are either not readable, or non-existent
fail_list=[failer for failer in sys.argv[2:] if failer not in sys_trim]

#argument 1 as a search string
search_string=str(sys.argv[1])
##############################################################################################################

# print(sys_trim,"\n",search_string) #file validation is working at this point

class ThreadProfile():
    '''
    ThreadProfile contains methods for parallel file processing  
    '''
    def __init__(self,iterable,parse_string):
        '''iterable should be a (surprise, surprise) an iterable object'''
        self.iterable = iterable 
        self.parse_string = parse_string
    
    def pmessage(self,method):
        prnt_strng = "Emulating 'grep -n' on chosen files.  '{}' being searched via {}".format(search_string,method)
        return "{}\n*{}*\n{}".format("*"*(len(prnt_strng)+2),prnt_strng,"*"*(len(prnt_strng)+2))    
    
    def num_grep(self,parse_string,target_file):
        '''
        create a dictionary mapping line number, and line text containing search string
        '''
        print("\nMatching lines found in {}:".format(target_file))
        with open(target_file,'r') as reader:
            print({"Line "+str(num+1):word.rstrip() for num,word in enumerate(reader.readlines()) if parse_string in word})            
    def thread_spinT(self):
        '''
        spin up some threads, using a function to parse files for specific text
        '''
        print(obj.pmessage("individual threads per file"))
        threads = [threading.Thread(target=self.num_grep, args=(self.parse_string,t_file)) for t_file in self.iterable]  
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join() 
        
    def poolmapT(self):
        pool=futures.ThreadPoolExecutor()
        print(obj.pmessage("thread pool method"))
        mapfunc = partial(self.num_grep, self.parse_string)
        print(pool.map(mapfunc,self.iterable))

    def profile_func(self,function):
        cProfile.run(str(function))

#instantiate the object as obj
obj=ThreadProfile(sys_trim,search_string)

if __name__=="__main__":
     print('\n'*2)
     if len(sys_trim)==0:
        print("You have selected files that either do not exist, or are not readable by user:","\n",fail_list)
        exit()
     for method in dir(obj):
        #loop will check obj methods for those ending in 'T', will run cProfile only on these obj methods
        if method[-1] == "T":
            method = "obj."+method+"()"
            cProfile.run(method) 
