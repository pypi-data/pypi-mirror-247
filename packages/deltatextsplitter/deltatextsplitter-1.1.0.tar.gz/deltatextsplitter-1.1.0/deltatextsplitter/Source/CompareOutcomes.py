"""
Module for the CompareOutcomes-function, a member function of the documentclass.
"""

# Import python modules:
import os


# Main function definition:
def CompareOutcomes_documentclass(self, thedocument: str, testmode=False):
    """
    This function will calculate KPI-values without actually generating
    output excels. It assumes the output excel is already present.
    This is much faster then executing a StandardRun, but only works
    if the output excels already have been generated before (by a StandardRun).

    # Parameters: thedocument: str: the specific name of the document
                  we execute the run for.
                  testmode: Bool: Decides which paths to specify for writing
                  the files. False=normal; True=testmode.
    # Returns: None: Stored in the class.
    """

    # Obtain the directory where the script is stored:
    saved_directory = os.path.dirname(os.path.realpath(__file__))

    # We begin by specifying the directories:
    self.splitter.set_documentpath(saved_directory + "/../pdfs/")
    self.splitter.set_documentname(thedocument)
    self.splitter.set_outputpath(saved_directory + "/../outs/")
    self.outputpath = saved_directory + "/../kpis/current/"
    self.referencepath = saved_directory + "/../refs/"

    # Adapt for testing if needed:
    if testmode:
        self.splitter.set_documentpath("../Inputs/")
        self.splitter.set_documentname(thedocument)
        self.splitter.set_outputpath("../Calc_Outputs/")
        self.outputpath = "../Calc_Outputs/"
        self.referencepath = "../True_Outputs/"

    # Next, read the Excels:
    self.read_references()
    self.read_outcomes()

    # Then, compute the KPI:
    self.KPI_Calculation()

    # Done.
