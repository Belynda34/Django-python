import requests
import pandas as pd
try:
    # event_api = requests.get('http://127.0.0.1:8000/eventpo/')
    # event_api.raise_for_status()
    # event_api_data = event_api.json()


    # df = pd.DataFrame(event_api_data.get('events',[]))

    # df.to_csv('dataset.csv',index=False)


    # Load the dataset
    df = pd.read_csv('dataset.csv')

    # Get an overview of the dataset
    # print(df.info())  # Displays column names, non-null counts, and data types
    # print(df.describe(include='all'))  # Summary statistics for numerical and categorical columns
    # print(df.head())  # Display the first few rows of the dataset
    # print(df.isnull().sum())  # Count null values in each column
    # print(df.describe(include='all'))



    # df.rename(columns={'name': 'event_name'}, inplace=True)
    # print(df.head())

    
    








    
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")














# attendees_api = requests.get('http://127.0.0.1:8000/attendees')
    # attendees_api.raise_for_status()
    # attendees_api_data = attendees_api.json()

    # df1 = pd.DataFrame(event_api_data.get('events', []))  
    # df2 = pd.DataFrame(attendees_api_data.get('attendees', []))

    # if 'event_id' not in df1.columns or 'event_id' not in df2.columns:
    #     raise ValueError("The required 'id' column is missing in one of the DataFrames.")

    # # print(event_api_data)
    # print(df2.columns)
    
    # merged_df = pd.merge(df1, df2, left_on = 'id', right_on= 'event_id', how = 'inner')
    # print(merged_df.shape)
    # dff = pd.mr













































