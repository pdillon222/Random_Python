#!/usr/bin/python3

__author__="James Dillon"

################################################################
#                                                              #
# Script to unfurl grouped lists of nodes from sinfo -R output #
# In order to get a full sequential list of downed nodes       #
#                                                              #
################################################################

import os,sys
from contextlib import redirect_stdout

#program was running with bugs on Edison.  Keeping testing line in Doc-String below in-case issues persist
'''
if os.uname()[1].startswith("edi"):
    print("Currently debugging program on Edison. {} will currently only run on Cori.  Please try again later".format(sys.argv[0]))
    exit()    
'''
def node_lists():
    '''
    function will create two seperate lists from sinfo -R output:
        >A standard list of nodes
        >A list of nodes grouped (by sinfo -R output) as ranges
    ''' 
    if 'unfurloutput' in os.listdir(): os.system('rm unfurloutput')
    os.system('sinfo -R >> unfurloutput')

    node_list=[node.rstrip() for node in open('unfurloutput','r').readlines() if "nid" in node]
    node_list=[node[node.index('nid'):] for node in node_list] 
    brack_list=[node for node in node_list if "[" in node] #master list of sequences and ranges
    ###############################################################################################
    node_list=[node for node in node_list if node not in brack_list] #node_list is ready for return
    range_list=[node for node in brack_list if "-" in node] #list of ranges
    brack_list=[node for node in brack_list if node not in range_list] #list of sequences only
    ################################node,sequence and range lists separated########################
    def brack_removal(listitem):
        # listitem=[item.replace("nid[","") for item in listitem if "nid[" in item]
        #listitem=[item.replace("]","") for item in listitem if "]" in item]
        listitem= list(map(lambda x: x.replace("nid[",""),map(lambda x: x.replace("]",""),listitem)))
        return listitem
    
    brack_list=brack_removal(brack_list)
    range_list=brack_removal(range_list)
    range_list=",".join(range_list)
    range_list=range_list.split(",")
    for i in range_list:
        if "-" not in i:
            brack_list.append(i)
    range_list=[node for node in range_list if "-" in node]
    brack_list=",".join(brack_list)
    brack_list=["nid"+node for node in brack_list.split(",")]
    node_list=node_list + brack_list
    
    return node_list,range_list


def expand_range(function):
    '''
    Expand nodes grouped as ranges
    takes in a function returning a list of formatted nodes
    and a list of nodes in ranges
    >returns a single list of node id's in sequential order
    '''
    node_list,range_list = function
    range_expand = []
    output_list = []
    range_list = [strings.split("-") for strings in range_list]
    for i in range_list:
        range_expand.append(list(range(int(i[0]),int(i[-1])+1)))
    for item in range_expand:
        for num in item:
            if len(str(num)) < 5:
                num = "0"*(5-len(str(num)))+str(num)
                output_list.append("nid"+num)
            else:
                output_list.append("nid"+str(num))
    return sorted(node_list + output_list)

if __name__ == "__main__":
    master_list = expand_range(node_lists())
    if 'nid' in master_list: master_list.remove("nid")
    os.system('rm unfurloutput')
    for node in master_list:
        print(node)
