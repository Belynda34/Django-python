import requests
import pandas as pd
try:
    event_api = requests.get('http://127.0.0.1:8000/events')
    event_api.raise_for_status()
    event_api_data = event_api.json()

    df = pd.DataFrame(event_api_data.get('events', []))

    df_part1_rows = df.iloc[:len(df)//2]  
    df_part2_rows = df.iloc[len(df)//2:]  


    num_columns = len(df.columns)
    df_part1_columns = df.iloc[:, :num_columns//2]  
    df_part2_columns = df.iloc[:, num_columns//2:] 

    # df_part1_columns.to_csv('df_part1_columns.csv', index=False)
    # df_part2_columns.to_csv('df_part2_columns.csv', index=False)


    # df_part1_rows.to_csv('df_part1_rows.csv', index=False)
    # df_part2_rows.to_csv('df_part2_rows.csv', index=False)


    concatenated_df_rows = pd.concat([df_part1_rows, df_part2_rows])
    concatenated_df_columns = pd.concat([df_part1_columns, df_part2_columns], axis=1) 

    # concatenated_df_rows.to_csv('concatenated_events_rows.csv', index=False)
    # concatenated_df_columns.to_csv('concatenated_events_columns.csv', index=False)


    df = pd.read_csv('concatenated_events_columns.csv')


    print(df.shape)
    


    # print("CSV file has been successfully created!")

    

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")








