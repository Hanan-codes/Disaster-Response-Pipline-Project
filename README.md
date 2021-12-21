# Disaster-Response-Pipline-Project
### Summary 
The main task in this project is to analyze disaster data from [Figure Eight](https://www.figure-eight.com/) to build a model for an API that classifies disaster messages.
### Project Components
There are three components for this project.

1. ETL Pipeline
- process_data.py:\
Loads the messages and categories datasets\
Merges the two datasets\
Cleans the data\
Stores it in a SQLite database

2. ML Pipeline 
- train_classifier.py: \
Loads data from the SQLite database\
Splits the dataset into training and test sets\
Builds a text processing and machine learning pipeline\
Trains and tunes a model using GridSearchCV\
Outputs results on the test set\
Exports the final model as a pickle file\
3. Flask Web App 
- The main page 
<img width="1538" alt="Screen Shot 2021-12-21 at 9 45 49 PM" src="https://user-images.githubusercontent.com/84443038/146994513-7eb91676-432e-45bb-aac8-724caca2c9e9.png">
- Result page after calssifying the massage "I am Hungry"
<img width="1538" alt="Screen Shot 2021-12-21 at 9 45 34 PM" src="https://user-images.githubusercontent.com/84443038/146994625-eaa0d323-a146-4aa2-b30e-35fbff83c830.png">


### Files Descriptions

	- README.md: read me file
	- Disaster Response Pipeline Project
		- \app
			- run.py: flask file to run the app
		- \templates
			- master.html: main page of the web application 
			- go.html: result web page
		- \data
			- disaster_categories.csv: categories dataset
			- disaster_messages.csv: messages dataset
			- DisasterResponse.db: disaster response database
			- process_data.py: ETL process
		- \models
			- train_classifier.py: classification code
### Dependencies
-I used Python 3.8 \
-Machine Learning Libraries: NumPy, SciPy, Pandas, Sciki-Learn\
-Natural Language Process Libraries: NLTK\
-SQLlite Database Libraqries: SQLalchemy\
-Web App and Data Visualization: Flask, Plotly\
### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

