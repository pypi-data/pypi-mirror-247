"""
Module for classdefinition of documentclass
"""

# Import Python base-functionality:

# Import third-party software:
import pandas

# Import functionality from pdftextsplitter
from pdftextsplitter import textsplitter

# Import class member functions:
from .PandasParser import PandasParser_documentclass
from .StandardRun import StandardRun_documentclass
from .CompareOutcomes import CompareOutcomes_documentclass
from .KPI_Calculation import KPI_Calculation_documentclass


# Class definition
class documentclass:
    """
    This class handles the evaluation of a single PDF document. The document
    is analyzed using pdftextsplitter and then the outcomes are compared
    against known references. The references must be supplied in the form
    of excel-files, which can then be read into a pandas dataframe.
    The class also provides functionality to transform the relevant information
    from the pdftextsplitter analysis into a similar pandas dataframe,
    so that the two frames can be compared.
    """

    # ------------------------------------------------------------------------------------

    # Definition of the default-constructor:
    def __init__(self):
        # Class members; the instance of pdftextsplitter:
        self.splitter = textsplitter()

        # provide columns definition:
        self.columns = [
            "NativeID",
            "Version",
            "Documentname",
            "Title",
            "MainType",
            "SubType",
            "Cascadelevel",
            "parentID",
        ]

        # The dataframe for storing the references:
        self.references = pandas.DataFrame(columns=self.columns)

        # The dataframe for storing the textsplitter outcomes:
        self.outcomes = pandas.DataFrame(columns=self.columns)

        # A pandas dataframe holding the metadata about the columns
        self.metadata = pandas.DataFrame()

        # Outputpath for writing the excels:
        self.outputpath = "./"

        # Path for retrieving the references:
        self.referencepath = "./"

        # Placeholder for the KPI's for this document:
        self.structure_kpi = 0.0
        self.cascade_kpi = 0.0

    # Definition of simple member functions:
    def export_outcomes(self):
        """
        Writes the outcomes-dataframe to an excel:
        """
        filename = self.outputpath + self.splitter.documentname + "_outcomes.xlsx"
        self.outcomes.to_excel(filename, index=False)

    def read_references(self):
        """
        Reads the references-dataframe from an excel:
        """
        filename = self.referencepath + self.splitter.documentname + "_references.xlsx"
        self.references = pandas.read_excel(io=filename, usecols=self.columns)

    def read_outcomes(self):
        """
        Reads the outcomes-dataframe from an excel:
        """
        filename = self.outputpath + self.splitter.documentname + "_outcomes.xlsx"
        self.outcomes = pandas.read_excel(io=filename, usecols=self.columns)

    # Definition of complex member functions:
    PandasParser = PandasParser_documentclass
    StandardRun = StandardRun_documentclass
    CompareOutcomes = CompareOutcomes_documentclass
    KPI_Calculation = KPI_Calculation_documentclass
