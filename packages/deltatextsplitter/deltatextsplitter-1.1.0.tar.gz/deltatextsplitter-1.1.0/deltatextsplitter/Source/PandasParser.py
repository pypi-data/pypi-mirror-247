"""
Module for the PandasParser-function, a member function of the documentclass.
"""

# Import Python base-functionality:

# Import third-party software:
import pandas

# import relevant parts from pdftextsplitter:
from pdftextsplitter import texttype
from pdftextsplitter import enum_type

# Import Human-readable conversions:
from .Human_Readable import get_maintype
from .Human_Readable import get_headlines_type
from .Human_Readable import get_enumtype


# Main function definition:
def PandasParser_documentclass(self):
    """
    This function will transform the outcomes of a pdftextsplitter-analysis
    into a pandas dataframe, as created in the documentclass.

    NOTE: The user must take care that there is actually some output to parse
    in the splitter-instance. So run self.splitter.process() before this
    function!

    # Parameters: None (taken from the class.)
    # Return: None (stored in the class.)
    """

    # Before we do anything: clear out the pandas dataframe:
    self.outcomes = pandas.DataFrame(columns=self.columns)

    # Begin by verifying that there is some content to parse:
    if len(self.splitter.textalineas) == 0:
        print("You cannot run this function if the splitter-instance")
        print("has no textalineas-content. provide one by running")
        print("process() on the splitter-instance yourself first.")
    else:
        # then, we can proceed. Loop over the textalineas:
        alineaindex = -1

        for alinea in self.splitter.textalineas:
            # First indrease the index:
            alineaindex = alineaindex + 1

            # begin by extracting types:
            maintype = get_maintype(alinea.alineatype)
            subtype = "Unknown"
            if maintype == "Headline":
                subtype = get_headlines_type(alinea.textlevel)
            elif maintype == "Enumeration":
                subtype = get_enumtype(alinea.enumtype)

            # Begin by creating a single line of the pandas dataframe:
            ThisRow = {
                "NativeID": alinea.nativeID,
                "Version": self.splitter.VERSION,
                "Documentname": self.splitter.get_documentname(),
                "Title": alinea.texttitle,
                "MainType": maintype,
                "SubType": subtype,
                "Cascadelevel": alinea.textlevel,
                "parentID": alinea.parentID,
            }

            # Add it to the existing pandas dataframe.
            self.outcomes.loc[alineaindex] = pandas.Series(ThisRow)

            # That should do the trick!
