SOME NOTES REGARDING THE ASSIGNMENT:

######################## REMARK ########################
# OLD_a03_Correction_Guidelines.txt are from 2023, 
# when the task were graded using points.
########################################################

--------------------------------- Task 1
a) aka Task 1.1
POS:
- One function, for calling the API (instead of in every method again)
- recognize that there are several pages of dog-breeds

NEG:
- API URL outside the class
- mixing up class and object method 
	- not initializing an object for testing
- no init method
- no testing at all
- not using self.attribute when appropriate
- not storing object information (that vary with instance) in the instance
- facts do not change with each call of the fact-method


b) aka Task 1.2
Error Ideas:
    - API connection error
    - Invalid breed name
    - Invalid method called
POS:
- 

NEG:
- no testing of the errors
	- insufficient testing of the errors
- only one type of error handling

---- Task 2.1 ----------------------------------------
a) replace_mentions()
POS:
- regex even catches hashtags that might be attached to each other!
- define regex pattern in a variable
- dropping unnecessary columns

NEG:
- the regex replacing usernames also replaces email-domains (e.g. test@uni-konstanz.de --> test@user)

b) extract_hashtags()

c) remove_urls()
NEG:
- keep the "www." part
- not all urls matched

---- Task 2.2 ----------------------------------------
a) normalize_text()

b) tokenize_text()
POS:
- handeling special characters (e.g.: ')
- using regex instead of .split()

NEG:
- removing # & @

c) remove_stopwords()
POS:
- remove additional uninformative characters and strings from clean_token
NEG:
- stopwords are not removed (e.g. because of newline characters)

---- Task 2.3 (Bonus) ----------------------------------------
NEG:
- not printing the top 10 lists
- not excluding the @user token
- having identical words more than once in the wordcloud
- only visualizing the top 10 words in the clouds

POS:
- removing meaningless words after first look at the cloud
- removing words that we know will be overpowering due to design (@user or #cdcwhisteblower)
- tweaking the first visualization to improve the message

---- Task 3 ----------------------------------------
a) aka 3.1
POS:
- adding addtional functionalities
	- save button
	- counter/pprocess bar
	- fixed text frame
	- loading the file from the computer file system
	- colored buttons
	- help-window
	
NEG:
- file creation and opening process outside the app
- message lingering when they are no longer needed
- error when the coding session is finished (this is technically not an error - congratulations message would have been more appropriate or option to close the process
- unnecessary buttons (e.g. extra 'next' button instead of adding the functionalities to the label-buttons)
- loading all the data into the app instead of just the sampled data
- output file is not generated automatically by the app, but has to be prepared manually beforehand
- uninformative title of the app
- missing instruction text in the app
- no check whether the 150 tweets have been reached
- functunality issues (e.g. App never works on the first try)

b) aka 3.2 
NEG:
- drawing random samples without a seed
- not running the app on the preprocessed data

POS: 
- (manually) store the file into the filesystem

---- Task 4 ----------------------------------------
a) aka 4.1
NEG:
- calculate the polarity score on the tokens and not the whole text
	- wrongly aggregate VADER scores
	
b) aka 4.2 
Guiding style questions:
When does it make sense to display shares vs absolute numbers?
Which graph type is most appropriate?

POS:
- add context info

NEG:
- unconventional color choices (neg = green & pos = red)
- running VADER only on the sample

c) aka 4.3
POS:
- using a heatmap/confusion matrix
- a quick intepretation
- drop undecidable values for the heatmap
