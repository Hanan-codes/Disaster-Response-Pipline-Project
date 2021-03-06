# import libraries
import sys
import pandas as pd
import nltk 
import re
import pickle

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split,  GridSearchCV 
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

from sqlalchemy import create_engine

nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger','stopwords'])

def load_data(database_filepath):
    """
    - Load Data Function
    
    Input:
        database_filepath -> path to the database
    Output:
        X -> feature DataFrame
        Y -> label DataFrame
        category_names -> A list of category names 
    """
    
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('df', engine)
    X = df['message']
    Y = df.iloc[:,4:]
    
    category_names = Y.columns

    return X,Y,category_names


def tokenize(text):
    """
    Tokenize function
    
    Input:
        text -> list of text from the messages column 
    Output:
        clean_tokens -> tokenized and clean text 
    """
    # regex for URLs to be replaced with a placeholder
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex,text)

    for url in detected_urls:
        text = text.replace(url,"urlplaceholder")
    
    words = word_tokenize(text)

    # remove stop words
    stopwords_en = stopwords.words("english")
    words = [word for word in words if word not in stopwords_en]

    # lemmatization
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(word) for word in words]

    return clean_tokens



def build_model():
    """
    Build Model function
    
    Input: 
    - None 
    Output: 
    - Classification model
    
    """
    # create a pipeline
    pipeline = Pipeline([
        ('vect',CountVectorizer(tokenizer = tokenize)),
        ('tfidf',TfidfTransformer()),
        ('clf',MultiOutputClassifier(RandomForestClassifier(n_jobs=-1)))    
    ])
    # parameters of Grid search
    parameters = {
                'vect__min_df': [1, 5],
                'tfidf__use_idf': [True, False],
                'clf__estimator__n_estimators':[10,20],
                'clf__estimator__min_samples_split': [2, 3]
                }

    model = GridSearchCV(pipeline,cv=3, param_grid=parameters,verbose=2)

    return model


def evaluate_model(model, X_test, Y_test, category_names):
    """
    Evaluate Model function
    Input:
        model -> Classification model
        X_test -> test features
        Y_test -> test labels
        category_names -> label names 
    Output: 
        - None
    """

    # predict the categroy of message
    Y_pred = model.predict(X_test)
    # convert ndarray to dataframe
    Y_pred = pd.DataFrame(Y_pred)

    # rename the columns of dataframe
    Y_pred.columns = category_names

    print(classification_report(Y_test,Y_pred, target_names = category_names))


def save_model(model, model_filepath):
    """
    Save Model as pickle file function 
    
    Input:
        model -> Classification model
        model_filepath -> path to save .pkl file
    """
    filename = model_filepath
    pickle.dump(model, open(filename, 'wb'))
    pass



def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()