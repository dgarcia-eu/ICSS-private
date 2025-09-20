SOME NOTES REGARDING THE ASSIGNMENT:

PART 1:
often forgotten:
- test upload to GitHub with the Name
	- only left a note since this is primarily a check for the students
	
PART 2: 
Task 5:
a)
POS:
- declare NA values directly with the import

NEG: 
- redundant arguments in the import function (here e.g.: na_values = "?" - since there are no ? as NAs in the CSV)
	- this is a hint that the student did not quite get the working of the argument

- import with absolute paths 

b) 
NEG: 
- renaming is not stored
	- e.g. forget to add 'inplace = true' in the rename function 

c) 
NEG:
- no argument as to WHY it is okay to drop the NA countries
- "N.A." rows are not detected and removed
	 - a small challenge in this subtask is that there are two types of NA encodings that both have to be accounted for

d) 
GENERAL:
- type conversions might work slightly different on different systems --> be slow to judge!
- keep avoidable errors in the code (technically a Style Question)
- working with the wrong dataset (not cleaned one)
- doubling functionality/code redundancy (e.g.: using unique and set to remove doubles)

POS:
- use known functions arguments to simplify the task 
	- e.g to_numeric() with errors="ignore"

NEG:
- percentage issues
	- name of the column and content do not match (name includes % and content is between 0 and 1)
	- divide to many times by hundred 
- forget to remove the transfer at least one column (column, remove percentage, ...)
	- technically this depends on the exact task - If it is not explicitly asked and the column is not used then this 'mistake' can be ignored

e) 
POS:
- solve all the matching issues (by hand)

NEG:
- NOT addressing the issue of falsely non-matching countries!
- join by hand -> should use the correct merge-statement (way more efficient)

f) 
GENERAL:
- what is lowest change?? (close to zero or as negative as possible)
NEG:
- not printing the result!

g) 
NEG:
- not providing percentage (but a value between 0 an 1)
- compute the share by hand (already exists - without a reason why the column is not use, this is code redundancy)

h) 
NEG:
- VERY COMMON: number on the y-axis and the label of the y-label do not operate on the same scale!
- keeping the billions as labels - hard to read
- calculate the group_by by hand - more error prone and probably less efficient
- results not ordered

i) 
POS:
- use log to display the interesting parts better

NEG:
- only a violin plot for one continent and not all together in one graph (-> we need this for comparison reasons)
- not clearly indicating which transformations have been added to the y-axis
- interpretation is lacking (not done or not mentioning enough noticeable metrics)
	- address the artifact that population cannot be zero (but the graph implies it)
- number on the y-axis and the label of the y-label do not operate on the same scale!
- keeping the billions as labels - hard to read






