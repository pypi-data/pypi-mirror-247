"""
Module for the FullRun-function, a member function of the deltatextsplitter-class.
"""

# import python modules:
import os
import math

# import subclasses:
from .documentclass import documentclass


# Main function definition:
def FullRun_deltatextsplitter(self, FullProcess=0, TestMode=False):
    """
    This function will execute a StandardRun over all pdf documents
    inside the pdfs-folder. It will simply locate all documents
    and execture a run over each filename.

    # Parameters: TestMode: Bool: Decides which paths to specify for writing
                  the files. False=normal; True=testmode.
                  FullProcess: int: Decides which part of the process is executed:
                  0: everything
                  1: the documents are re-processed, but outputs (html, xlsx, txt, etc is not saved)
                  2: the documents are not reprocessed; results are calculated based on previous outputs.
    # Returns: None: Stored in the class.
    """

    # Reset KPI's:
    self.structure_kpi = 0.0
    self.structure_kpi_sigma = 0.0
    self.cascade_kpi = 0.0
    self.cascade_kpi_sigma = 0.0

    # Obtain the directory where the script is stored:
    saved_directory = os.path.dirname(os.path.realpath(__file__))

    # Find all PDFs in the folder:
    pdfpath = saved_directory + "/../pdfs/"
    if TestMode:
        pdfpath = "../Inputs/"
    filenames = os.listdir(pdfpath)

    # Remove the ".pdf" and the wrong files:
    selected_filenames = []
    for filename in filenames:
        if ".pdf" in filename:
            selected_filename = filename.replace(".pdf", "")

            if not (("UNFIT" in selected_filename) or ("THESAME" in selected_filename)):
                selected_filenames.append(selected_filename)

    # Next, perform the full run over all files:
    for filename in selected_filenames:
        # Create the class:
        thisdoc = documentclass()

        # Perform the run:
        print("---- Processing document <" + filename + ">---------")
        if not (FullProcess == 2):
            thisdoc.StandardRun(filename, FullProcess, TestMode)
        else:
            thisdoc.CompareOutcomes(filename, TestMode)

        # Append the class:
        self.documentarray.append(thisdoc)

        # Add KPI's:
        self.structure_kpi = self.structure_kpi + thisdoc.structure_kpi
        self.structure_kpi_sigma = (
            self.structure_kpi_sigma + thisdoc.structure_kpi * thisdoc.structure_kpi
        )
        self.cascade_kpi = self.cascade_kpi + thisdoc.cascade_kpi
        self.cascade_kpi_sigma = self.cascade_kpi_sigma + thisdoc.cascade_kpi * thisdoc.cascade_kpi

    # Finally, calculate averages & standard deviations:
    if len(selected_filenames) > 0:
        # Average calculation:
        self.structure_kpi = self.structure_kpi / (len(selected_filenames))
        self.cascade_kpi = self.cascade_kpi / (len(selected_filenames))

        # Calculations of <x^2>:
        self.structure_kpi_sigma = self.structure_kpi_sigma / (len(selected_filenames))
        self.cascade_kpi_sigma = self.cascade_kpi_sigma / (len(selected_filenames))

        # Calculation of Variance = <x^2> - <x>^2:
        self.structure_kpi_sigma = (
            self.structure_kpi_sigma - self.structure_kpi * self.structure_kpi
        )
        self.cascade_kpi_sigma = self.cascade_kpi_sigma - self.cascade_kpi * self.cascade_kpi

        # Calculation of standard deviation:
        self.structure_kpi_sigma = math.sqrt(self.structure_kpi_sigma)
        self.cascade_kpi_sigma = math.sqrt(self.cascade_kpi_sigma)

    # Print results:
    print("")
    print(
        "FULL STRUCTURE KPI(%) = "
        + str(100.0 * self.structure_kpi)
        + " +/- "
        + str(100.0 * self.structure_kpi_sigma)
    )
    print(
        "FULL CASCADE KPI(%)   = "
        + str(100.0 * self.cascade_kpi)
        + " +/- "
        + str(100.0 * self.cascade_kpi_sigma)
    )
    print("")

    for thisdoc in self.documentarray:
        print(
            thisdoc.splitter.documentname
            + ": structure(%) = "
            + str(100.0 * thisdoc.structure_kpi)
            + " & cascade(%) = "
            + str(100.0 * thisdoc.cascade_kpi)
        )
    print("")
