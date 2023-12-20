"""
Module to hold the conversions from enumerations to human-readable strings.
"""

# Import Python base-functionality:

# import relevant parts from pdftextsplitter:
from pdftextsplitter import texttype
from pdftextsplitter import enum_type


# Function definition of converting enumerations:
def get_maintype(enum_identifcation: texttype) -> str:
    """
    Converts the main texttype (headlines, enumeration, etc.)
    from a python enumeration into a human-readable string.

    # Parameters: enum_identifcation: texttype: the enumeration to convert.
    # Returns: str: the human-readable string:
    """

    # Begin by declaring the answer:
    answer = "Unknown"

    # Move through all options:
    if enum_identifcation == texttype.TITLE:
        answer = "Title"
    elif enum_identifcation == texttype.FOOTER:
        answer = "Header/Footer"
    elif enum_identifcation == texttype.BODY:
        answer = "Body"
    elif enum_identifcation == texttype.HEADLINES:
        answer = "Headline"
    elif enum_identifcation == texttype.ENUMERATION:
        answer = "Enumeration"

    # Return the answer:
    return answer


# Function definition of converting enumerations:
def get_headlines_type(cascadelevel: int) -> str:
    """
    Converts the cascadelevel into a human-readable string like
    chapter, section, etc.

    NOTE: This function can only be used IF the maintype is
    identified as a Headline/texttype.HEADLINES.

    # Parameters: cascadelevel: int: the cascadelevel to convert.
    # Returns: str: the human-readable string:
    """

    # Begin by declaring the answer:
    answer = "Unknown"

    # Move through all options:
    if cascadelevel == 0:
        answer = "Title"
    elif cascadelevel == 1:
        answer = "Chapter"
    elif cascadelevel == 2:
        answer = "Section"
    elif cascadelevel == 3:
        answer = "Subsection"
    elif cascadelevel == 4:
        answer = "Subsubsection"
    elif cascadelevel > 4:
        answer = "Higher_Order"

    # Return the answer:
    return answer


# Function definition of converting enumerations:
def get_enumtype(enum_identifcation: enum_type) -> str:
    """
    Converts the enumeration-type (an python-enumeration)
    into a human-readable string like Bigroman, Bigletter, etc.

    NOTE: This function can only be used IF the maintype is
    identified as an Enumeration/texttype.ENUMERATION.

    # Parameters: enum_identifcation: enum_type: the enumeration to convert.
    # Returns: str: the human-readable string:
    """

    # Begin by declaring the answer:
    answer = "Unknown"

    # Move through all options:
    if hasattr(enum_type, "BIGROMAN"):
        if enum_identifcation == enum_type.BIGROMAN:
            answer = "Bigroman"
    if hasattr(enum_type, "SMALLROMAN"):
        if enum_identifcation == enum_type.SMALLROMAN:
            answer = "Smallroman"
    if hasattr(enum_type, "BIGLETTER"):
        if enum_identifcation == enum_type.BIGLETTER:
            answer = "Bigletter"
    if hasattr(enum_type, "SMALLLETTER"):
        if enum_identifcation == enum_type.SMALLLETTER:
            answer = "Smallletter"
    if hasattr(enum_type, "DIGIT"):
        if enum_identifcation == enum_type.DIGIT:
            answer = "Digit"
    if hasattr(enum_type, "DIGITDOT"):
        if enum_identifcation == enum_type.DIGITDOT:
            answer = "Digit"
    if hasattr(enum_type, "DIGITBRACKET"):
        if enum_identifcation == enum_type.DIGITBRACKET:
            answer = "Digit"
    if hasattr(enum_type, "SIGNMARK"):
        if enum_identifcation == enum_type.SIGNMARK:
            answer = "Signmark"
    if hasattr(enum_type, "ARTICLE"):
        if enum_identifcation == enum_type.ARTICLE:
            answer = "Article"
    if hasattr(enum_type, "ANNEX"):
        if enum_identifcation == enum_type.ANNEX:
            answer = "Annex"

    # Return the answer:
    return answer
