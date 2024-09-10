from django.http import HttpResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from .models import CsvUpload

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return HttpResponse("No file uploaded.")
        file = request.FILES['file']
        try:
            data_df = pd.read_csv(file)
            data_df = data_df.where(pd.notnull(data_df), None)
            df_json = data_df.to_dict(orient='records')
         
            for row in df_json:
                CsvUpload.objects.create(
                    name=row.get('name'),
                    tsc_number=row.get('tsc_number'),
                    region =row.get('region'),
                    email=row.get('email')
                )
            return HttpResponse("CSV Uploaded and Data Inserted")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("An error occurred while processing the CSV file.")
    return HttpResponse("Invalid request method")

