import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
from Source.deltatextsplitter import deltatextsplitter

# Definition of the Run-function:
def deltatextsplitter_fullrun():
    """
    # Function to run everything from deltatextsplitter.
    # Parameters: none (stored in the code & files)
    # Return: none (stored in the class)
    """

    # Generate the class:
    mydelta = deltatextsplitter()

    # Execute the run:
    mydelta.FullRun(2, False)
    # First Argument:
        # 0: Execute everything
        # 1: Skip the writing of output-files, but execute everything else
        # 2: use previously calculated & saved excels to compute KPI's
    # Second Argument: False=normal run, True=TestMode

    # Done.

if __name__ == '__main__':
    deltatextsplitter_fullrun()
