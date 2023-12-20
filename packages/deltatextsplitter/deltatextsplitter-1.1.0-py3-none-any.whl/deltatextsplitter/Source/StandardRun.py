"""
Module for the StandardRun-function, a member function of the documentclass.
"""

# Import python modules:
import os

# Add logging:
import logging

logger = logging.getLogger(__name__)


# Main function definition:
def StandardRun_documentclass(self, thedocument: str, FullProcess=0, testmode=False):
    """
    This function will execute a single run of documentclass,
    using the default values for the different directories.
    After we are done, we have generated excels for the current
    version of textsplitter and we have the relevant data in
    both the pandas-instances inside, so we can do calculations
    and comparison with them.

    # Parameters: thedocument: str: the specific name of the document
                  we execute the run for.
                  FullProcess: int: decides which parts of the process is executed.
                      0: everything is executed
                      1: we do not write outputs, but we do execute everything else.
                      2: not applicable for this run; use CompareOutComes instead.
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

    # Next, perform the execution:
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Appoint standard parameters")
    self.splitter.standard_params()
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Fire Process function")
    process_indicator = -1
    if FullProcess == 0:
        process_indicator = 0
    self.splitter.process(process_indicator)
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Fire PandasParser")
    self.PandasParser()

    # Finally, read & generate excels:
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Start Reading References")
    self.read_references()
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Start exporting outcomes")
    if FullProcess == 0:
        self.export_outcomes()

    # Then, compute the KPI:
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Start KPI-calculation")
    self.KPI_Calculation()
    logger.info("DELTATEXTSPLITTER: " + thedocument + " --> Finished")

    # Done.
