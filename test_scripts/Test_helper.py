

import sys, os 

def add_srcPath():
    s_thisPath = os.path.abspath(__file__)
    l_srcPath = s_thisPath.split("/")[:-2] + ["src"]
    sys.path.append( "/".join(l_srcPath) )
