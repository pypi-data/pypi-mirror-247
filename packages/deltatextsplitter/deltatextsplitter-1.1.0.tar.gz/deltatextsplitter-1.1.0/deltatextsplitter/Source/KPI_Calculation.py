"""
Module for the KPI_Calculation-function, a member function of the documentclass.
"""

# Import 3rd-party software:
from thefuzz import fuzz


# Main function definition:
def KPI_Calculation_documentclass(self, verbose_option=0):
    """
    Once both pandas dataframes (references and outcomes)
    have been filled with the appropriate column structure,
    this function will compare them and calculate the KPI.

    One method of filling the dataframes is using the
    StandardRun-function of the documentclass, but any method
    that fills the dataframes can be used.

    # Parameters: verbose_option: int: Decides how much information is printed on the screen.
    # Returns: None: Stored in the class.

    """

    # Define parameters for KPI-Calculation:
    fuzzy_threshold = 80.0

    # Begin by declaring the variables we need:
    false_positives = 0  # Number of structure items that are found by textsplitter (outcomes), but are not present in the references.
    true_negatives = 0  # Number of structure elements that are not/incorrect found by textsplitter (outcomes), but are present in references.
    true_positives = (
        0  # Number of appriorpraite matches between the textsplitter (outcomes) and the references.
    )
    true_total = 0  # Total number of structure elements in the references.
    cascade_max_counter = (
        0  # Counter of every time we found a match REGARDLESS of the cascadelevel.
    )
    cascade_counter = 0  # Counter of every time we found a match AND the cascade level matches.

    # Begin by looping over the outcomes, to generate an array that identifies
    # whether we found a match to the references or not:
    outcomes_track_array = []
    for index, row in self.outcomes.iterrows():
        outcomes_track_array.append(False)

    # Next, ignite the parent-loop over the references:
    for ref_index, ref_row in self.references.iterrows():
        # Extract the quantities that we need:
        ref_title = str(ref_row["Title"])
        ref_maintype = str(ref_row["MainType"])
        ref_cascade = int(ref_row["Cascadelevel"])

        # Next, we need to perform fuzzy matching to the titles of the outcomes:
        current_fuzzy_match = 0.0
        max_fuzzy_match = 0.0
        max_fuzzy_index = -1
        matched_title = ""
        matched_maintype = ""
        matched_cascade = -1
        matched_index_diff = 999999999

        # So loop over the outcomes:
        for out_index, out_row in self.outcomes.iterrows():
            # Extract the quantities that we need:
            out_title = str(out_row["Title"])
            out_maintype = str(out_row["MainType"])
            out_cascade = int(out_row["Cascadelevel"])
            out_index_diff = abs(ref_index - out_index)

            # In case we are dealing with an enumeration, cap the titles:
            working_ref_title = ref_title
            working_out_title = out_title

            if ref_maintype == "Enumeration":
                # Split into words:
                working_ref_title_array = working_ref_title.split()
                working_out_title_array = working_out_title.split()
                working_ref_title_length = len(working_ref_title_array)
                working_out_title_length = len(working_out_title_array)

                # Calculate the minimum:
                min_length = len(working_ref_title_array)
                if min_length > len(working_out_title_array):
                    min_length = len(working_out_title_array)

                # Limit the titles:
                working_ref_title_array = working_ref_title_array[0:min_length]
                working_out_title_array = working_out_title_array[0:min_length]

                working_ref_title = ""
                for word in working_ref_title_array:
                    working_ref_title = working_ref_title + word + " "

                working_out_title = ""
                for word in working_out_title_array:
                    working_out_title = working_out_title + word + " "

                # Done.

            # Perform fuzzy matching:
            current_fuzzy_match = fuzz.ratio(working_ref_title, working_out_title)

            # Search for the maximum:
            if current_fuzzy_match > max_fuzzy_match:
                # This is STRICTLY bigger. then, we always replace the match
                # with the new candidate, as this is simply a better match.
                max_fuzzy_match = current_fuzzy_match
                max_fuzzy_index = out_index
                matched_index_diff = out_index_diff
                matched_title = out_title
                matched_maintype = out_maintype
                matched_cascade = out_cascade

            elif current_fuzzy_match == max_fuzzy_match:
                # This is equality. If the new candidate has an equal match
                # but not a better one, we only replace it if the index
                # difference is smaller then the previous answer. This is
                # important, as one may encounter multiple matches in case
                # of a TOC: one inside the TOc and one as the real chapter title.
                if out_index_diff < matched_index_diff:
                    # only then, make the replacement:
                    max_fuzzy_match = current_fuzzy_match
                    max_fuzzy_index = out_index
                    matched_index_diff = out_index_diff
                    matched_title = out_title
                    matched_maintype = out_maintype
                    matched_cascade = out_cascade

        # -----------------------------------------
        # Close the loop over the second dataframe:

        # Give some output:
        if verbose_option >= 2:
            print("Reference Title           = " + ref_title)
            print("Reference Index           = " + str(ref_index))
            print("Reference Cascade         = " + str(ref_cascade))
            print("Matched Outcomes Title    = " + matched_title)
            print("Matched Outcomes MainType = " + matched_maintype)
            print("Matched Outcomes Cascade  = " + str(matched_cascade))
            print("Matched Outcomes Index    = " + str(max_fuzzy_index))
            print("Fuzzy Match Ratio         = " + str(max_fuzzy_match))

        # Decide if we found a match:
        if max_fuzzy_index >= 0:
            if max_fuzzy_match >= fuzzy_threshold:
                # Next, require additional KPI-demands:
                if ref_maintype == matched_maintype:
                    # Then, we count it as a match:
                    outcomes_track_array[max_fuzzy_index] = True
                    cascade_max_counter = cascade_max_counter + 1

                    if not (ref_cascade == matched_cascade):
                        cascade_counter = cascade_counter + 1

                    printstr = ""
                    for tracked in outcomes_track_array:
                        if tracked:
                            printstr = printstr + "1"
                        else:
                            printstr = printstr + "0"
                        printstr = printstr + " "
                    if verbose_option >= 2:
                        print(printstr)

        # Count the number of elements in the dataframe:
        true_total = true_total + 1
        if verbose_option >= 2:
            print("")

    # -----------------------------------------
    # That is all that we need inside the loop. Close it.

    # Next, calculate the quantities:
    for tracked in outcomes_track_array:
        if tracked:
            true_positives = true_positives + 1

    false_positives = len(outcomes_track_array) - true_positives
    true_negatives = true_total - true_positives

    # Then, calculate the KPI:
    self.structure_kpi = 0.0
    if (false_positives + true_total) > 0:
        self.structure_kpi = 1.0 - (false_positives + true_negatives) / (
            false_positives + true_total
        )

    self.cascade_kpi = 0.0
    if cascade_max_counter > 0:
        self.cascade_kpi = 1.0 - cascade_counter / cascade_max_counter

    if verbose_option >= 1:
        print("true_total      = " + str(true_total))
        print("true_positives  = " + str(true_positives))
        print("false_positives = " + str(false_positives))
        print("true_negatives  = " + str(true_negatives))
        print("Structure KPI   = " + str(self.structure_kpi))
        print("Cascade KPI     = " + str(self.cascade_kpi))
