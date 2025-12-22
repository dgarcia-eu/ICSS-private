SOME NOTES REGARDING THE ASSIGNMENT:


---- Task 1  ----------------------------------------
a) aka Task 1.1 (naiive window-function)
POS:
- input type checking
- track time while processing (e.g. with tqdm)
- providing the pseudocode for the function

NEG:
- keep the event itself in the window-function return
- function assuming order (without checking it and or ensuring it)
- using another id column besides event_id_cnty
- function has no output

b) aka Task 1.2 (optimized function)
POS:
- checking the results by matching the dictionary key and values from Task 1.1/a) and Task 1.2/b

NEG: 
- not stopping/starting the comparison once the difference is higher than the window size (given a sorted input)

c) aka Task 1.3 (plot time difference)
NEG:
- display the runtime in several graphs instead of one
- not generating enough data for the plot (e.g. only two window sizes)
- using plots that are not optimal for the data at hand (e.g. here barplot)

---- Task 2.1 ----------------------------------------
a) Selection Sort
POS: 
- creating a function to test the function 

NEG:
- function does not return the results

b) Merge Sort
NEG:
- function does not return the results
- upper bound of range wrongly defined (one test missing)

c) Comparison and visualization
POS: 
- check with log-scales as well

NEG:
- display the runtime in several graphs instead of one

---- Task 2.2 ----------------------------------------
a) Comparison

b) Visualization

---- Task 3 ----------------------------------------
a) aka 3.1 (Schema)
POS:
- keep an extra table for the ratings

NEG:
- not using the director_id

b) aka 3.2 (Implemented Schema)

c) aka 3.3 (load data)?
POS: 
- thorough data cleaning
- Converting a string representation of a list to an actual list (ast.literal_eval)
- DB input checking

NEG:
- using wrong ids
- mismatch of data type in python and the data type expected bey the DB via the schema
- creating a new key-column instead of using the provided/identified primary key columns

d) aka 3.4 (Query the DB)
(i) Queries 1a & 1b + Visualization
POS:
- visualize both lines in one plot - using a two y-axis approach

NEG:
- visualize both lines in one plot and only using one y-axis (due to the difference in scale a two-y-axis approach works better)
- not adding the constraints into the query (ideally in the WHERE-clause)

(ii) Queries 2a & 2b
GERNERAL COMMENT: The challenge here is a "double join genre + AND" (variations are possible, but this is imho the most straight forward solution to this) to get all movies that belong to both the Western and the Drama genre (a movie can belong to several genres!)

NEG:
- duplicates in the result


(iii) Query 3

(iv) Queries 4a & 4b + Visualization
POS:
- adding the exact numbers on to the graph 

NEG:
- unsorted values in the visualization
- keeping unnecessary columns in SELECT

(v) Reflection
Ideas: 
-  which movies are rated at all
- from which cultural backgrounds do they come
- are they a representative sample of all movies that are released (in terms of culture, genre, date etc.)
- who are the voters/raters etc...
- data cleaning issues

NEG:
- only reflect on issues generated through the data cleaning process

---- Task 4 ----------------------------------------
a) aka 4.1 

b) aka 4.2
(i) Query 1
NEG:
- not connect to the country table (only returns the country code) 

(ii) Query 2a & 2b
POS:
- spot inconsistencies (some countries are counted towards several continents here)

NEG:
- returns highly populated countries instead of CONTINENTS
- not connecting to the continent table for the area value

(iii) Query 3

