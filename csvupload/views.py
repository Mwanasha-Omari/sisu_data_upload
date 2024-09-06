
from django.http import HttpResponse
import pandas as pd
import json
import psycopg2
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['file']
        data_df = pd.read_csv(file)        
        # Replace NaN values with None (which becomes null in JSON)
        data_df = data_df.where(pd.notnull(data_df), None)        
        # Convert DataFrame to list of dictionaries (records)
        df_json = data_df.to_dict(orient='records')
        # Debugging: print JSON data
        print("JSON Data:")
        print(df_json)
        try:
            conn = psycopg2.connect(dbname='detailsdatabase', user='detailsuser',password='@codehive2024',host='localhost',port='5432'
            )
            cur = conn.cursor()
            # Ensure table creation
            cur.execute('''
                CREATE TABLE IF NOT EXISTS json_data (
                    id SERIAL PRIMARY KEY,
                    data JSONB
                )
            ''')
            insert_query = 'INSERT INTO json_data (data) VALUES (%s)'
            for record in df_json:
                json_data = json.dumps(record)  # Convert record to JSON string
                cur.execute(insert_query, (json_data,))
            conn.commit()
            cur.close()
            conn.close()
            return HttpResponse("CSV Uploaded and Data Inserted")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("An error occurred while processing the CSV file.")
    return HttpResponse("Invalid request method")


