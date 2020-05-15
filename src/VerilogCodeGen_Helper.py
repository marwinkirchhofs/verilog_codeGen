#!/usr/bin/env python3

# 
# helper declarations/functions for verilog code generator
#

from enum import Enum

class IndentObj:
    """ holds tabwidth and desiredIndentation to be used by all write functions to provide proper indentations and alignments """
    def __init__(self, tabwidth=4, desiredIndentation=24):
        self.__tabwidth = tabwidth
        self.__desiredIndentation = desiredIndentation

    def __str__(self):
        return "tabwidth: " + str(self.__tabwidth) + ", desiredIndentation: " + str(self.__desiredIndentation)

    def get_tabwidth(self):
        return self.__tabwidth
        
    def get_desiredTabIndentation(self):
        return self.__desiredIndentation


class HDL_Enum(Enum):
    VERILOG         = 1
    SYSTEMVERILOG   = 2

    def get_regType(self):
        """
        returns register type (reg or logic) according to language type
        """
        if self is HDL_Enum.VERILOG:
            return "reg"
        else:
            return "logic"


def get_tabbedString(elements, indentObj: IndentObj):
    """
    Returns a string containing the elements of elements in order separated by tab characters. This is useful to get equally-formatted strings for example for variable declarations and assignments.
    All but the last element are separated by one tab character. If possible (-> preceeding string not too long), the last element (presumably the variable identifier) is tabbed so that it has desiredIndentation relative to first character of the first element. 

    :elements: all elements to be put in the string as tupel 
    :tabwidth: tabwidth in characters as int
    :desiredIndentation: desired indentation of last element in characters relative to start of the string
    :returns: tabbed string as described
    """

    desiredTabIndentation = get_desiredTabIndentation(indentObj)

    list_elements = list(elements)

    # compute remaining tab characters 
    # (determines tab characters for each element in list_elements and subtracts them from desiredTabIndentation)
    remainingTabs = desiredTabIndentation - sum( map( lambda elem: int( len(elem) / indentObj.get_tabwidth() ) + 1, list_elements[:-1] ) )
    
    # insert all but last tabs
    for i in range (len(list_elements)-1, 0, -1):
        list_elements.insert(i, "\t")

    # insert remaining tabs
    for i in range(remainingTabs):
        list_elements.insert(-1, "\t")

    return "".join(list_elements)


def get_desiredTabIndentation(indentObj: IndentObj):
    """
    simple integer division to compute desired number of tabs 

    :returns: number of tab indentation as int
    """
    return int( indentObj.get_desiredTabIndentation() / indentObj.get_tabwidth() ) 

