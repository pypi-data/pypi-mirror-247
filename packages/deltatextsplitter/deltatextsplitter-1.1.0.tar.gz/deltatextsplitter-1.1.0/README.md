# DeltaTextsplitter package

This package is meant to provide an objective evaluation of the performance of the
[pdftextsplitter](https://pypi.org/project/pdftextsplitter/) package in terms of
KPI's.
<br />
<br />
The package includes a set of test documents with references in the form of excel-files.
These reference-files are human-produces excel-files containing the structure of
the test documents that the pdftextsplitter package should have recognised. This can then
be compared to the actual output of the pdftextsplitter package, so that the performance
of the package can be evaluated.
<br />
<br />
The performance is evaluated in terms of the following two KPI's <br />
structure KPI = 1 - (fp + tn)(fp + tt) <br />
where tt = true total, the total number of structure elements in the reference-file,
fp = false positive, the number of structure elements that are present in the output, but not in the reference-file,
and tn = true negative, meaning tn = tt - tp, where tp = true positive,
the number of matching structure elements between the reference-file and the actual outcome.
Two structure elements are said to match if the fuzzy match ratio of their titles is >=80.0
(determined with the package [thefuzz](https://pypi.org/project/thefuzz/)) and their main structure types are equal.
<br />
<br />
cascade kpi = 1 - uc/tp <br />
where uc = unequal cascades, a subset of the above number tp where the cascade levels
of the reference-file and the outcome of the package do not match.
<br />
<br />
With these two KPI's, it is possible to quantify improvements made to the pdftextsplitter
package by calculating KPI's for each released version of pdftextsplitter.

### Getting started

The KPI calculation can be performed efficiently by entering the following commands:
from deltattextsplitter import documentclass <br />
mydelta = deltattextsplitter()
mydelta.FullRun()
<br />
<br />
The KPI's will then be printed, but can also be retrieved from: <br />
mydelta.structure_kpi <br />
mydelta.cascade_kpi <br />
The KPI's per test document can also be retrieved from: <br />
mydelta.documentarray[index].splitter.documentname <br />
mydelta.documentarray[index].structure_kpi <br />
mydelta.documentarray[index].cascade_kpi <br />
There are 12 testdocuments in total.
<br />
<br />
The FullRun-command is very CPU-intensive, as it needs to process all the test documents
with the pdftextsplitter-package (in dummy-mode). Once this has been done, one could
speed up the process of subsequent calculations by entering <br />
mydelta.FullRun(False,False) <br />
to skip the pdftextsplitter-execution and only redo the KPI-calculation.

