SOME NOTES REGARDING THE ASSIGNMENT:

######################## REMARK ########################
# OLD_a02_Correction_Guidelines.txt are from 2023, 
# when the task were graded using points.
########################################################

--------------------------------- Task 1
a)

b)
POS:
- differentiate between 0 points and grey cells (NaN)

NEG:
- never building a function for the extraction
- forget to remove the newline character

c)
POS:
- some testing prints after the extraction

NEG:
- overwriting of extracted information

--------------------------------- Task 2
Pos:
- clean the songwriter table (is not needed later on, but it in actual projects this would be nice to have

NEG:
- table is nested in a list (by default when using read_html, very easy to fix)

--------------------------------- Task 3
a)
POS:
- use a function to encode to "url-style"
- going back to html for the exact name/link of the artist
- manually change the wrong urls (its not the smoothest solution - not really a negative but also not really a positive...)

NEG:
- did not check whether the returned page age is reasonable
- manually add the urls of the correct artists
- manually change the wrong urls (its not the smoothest solution - not really a negative but also not really a positive...)

b) 
POS:
- add a naiive regression line to the plot
- checking the distribution
- age on x and score on y

NEG:
- not calculating a correlation metric (only visual analytics)
- unclear where in the graph the ESC took place
- not clearly stating what the scale and references for the labels are
- no visualization

--------------------------------- Task 4
a)
POS:
- building the graph from the adjacency matrix

NEG:
- if data has been stored in a csv earlier, it is better to have an import csv line for subsequent tasks using this file
- swapped edge direction

b)
POS:
- show different versions of the graph
- use country abbreviations + legend for better readability

NEG:
- very clustered plots
- visualize an unexplained metric
- hard-coding nodes
- very little visualization featured presented
- using an undirected graph
- not indicating whether a country is giving or receiving
- no visualization of the overall points
- no indication of the edge weight in the visualization

--------------------------------- Bonus
a)
POS:
- noticed that: Macedonia was renamed to North Macedonia in 2019 

NEG:
- grouping by hand... (probably inefficient and very error prone)

b) visualization
POS:
- remove outliers (for better readability)
- anything (color, size, boldness) that improved communication of the graph's message

NEG:
- using Kamada-Kawai-Layout and not inverting the weights
- wrong/not intuitive direction of the edge
- not using a directed graph

c) interpretation
NEG:
- not interpreting the Kamada-Kawai-Layout distance correctly (common follow up error)
