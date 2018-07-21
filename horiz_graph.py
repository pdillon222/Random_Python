#!/usr/bin/python3
import random,sys

def horizontal_graph(values):
    '''
    Function creates a horizontal graph through ASCII display
    showing bar plot distribution of 40 random values in range 1:sys.argv[1]
    Distribution is randomized and should average near sys.argv[1]//2 
    '''
    crnt_height = max(values)
    print("#"*(len(values)+6))
    for i in range(1,max(values)+1):
        prnt_strng=["*" if x >= crnt_height else " " for x in values]
        if len(str(crnt_height))==1:
            print("0"+str(crnt_height)+":","".join(prnt_strng),"#")
        else:
            print(str(crnt_height)+":","".join(prnt_strng ),"#")
        crnt_height-=1
    print("   ","="*len(values),"#","\n","#"*(len(values)+5))
    print(values)

if __name__=="__main__":
    if len(sys.argv) != 2:
        points = input("Please enter an integer from 20--100 (inclusive): ")
        horizontal_graph([random.randint(1,40) for _ in range(1,int(points))])
    else:
        horizontal_graph([random.randint(1,40) for _ in range(1,int(sys.argv[1]))])
