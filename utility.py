import pprint
import sys

def dd(*args):
    """
    Dump and die function to print variables and halt execution.
    """
    # Pretty print each argument
    for arg in args:
        pprint.pprint(arg)
    
    # Stop execution
    sys.exit()