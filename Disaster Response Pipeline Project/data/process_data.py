# import libraries
import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    - Loud data function

    Input:
    - disaster_messages.csv filepath
    - disaster_categories.csv filepath

    Output:
        df -> Load the datasets into pandas DataFrame after mergeing them on id column
    """
    # load the csv file of messages dataset
    messages = pd.read_csv(messages_filepath)
    
    # load the csv file of categories dataset
    categories = pd.read_csv(categories_filepath)
    
    # merge two datasets on Id column
    df = pd.merge(messages,categories,on='id')
    return df
    
    return merged_df


def clean_data(df):
    """
    - Clean Data function
    
    Input:
        df -> A dataframe with both messages and categories
    Outputs:
        df -> Cleaned dataframe
    """

    # Split `categories` into separate category columns 
    categories = df['categories'].str.split(';', expand=True)
    
    # select first row
    row = categories.loc[0]

    # use this row to extract a list of new column names for categories
    new_columns = [r[:-2] for r in row]

    # rename the columns of `categories`
    categories.columns = new_columns

    # convert category values to 0s or 1s
    for column in categories:

        # set each value to be the last character of the string
        categories[column] = categories[column].astype(str).str[-1]

        # convert column from string to numeric
        categories[column] = pd.to_numeric(categories[column])
    
    # Replace `categories` column in `df` with new category columns
    df.drop('categories', axis = 1, inplace = True)
    df = pd.concat([df, categories], axis=1)

    # the related column have values of 2, 
    # map the 2s to 1s
    df['related'] = df['related'].map({0:0,1:1,2:1})

    # drop the duplicates
    df.drop_duplicates(inplace=True)

    return df


def save_data(df, database_filename):
    """
    - Save Data into a database function
    
    Input:
        df -> Clean DataFrame
        database_filename -> filepath for the SQL database to stores the clean data into the specified database file path.
    Output:
        - None
    """
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('df', engine, index=False,if_exists='replace')
    pass  

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
