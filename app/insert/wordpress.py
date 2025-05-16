from datetime import datetime

import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

# Initialize VectorStore
vec = VectorStore()

# API endpoint you want to call
url = "https://event.bcc.no/wp-json/wp/v2/pages"

# Make the GET request
response = requests.get(url)

# Check the response
if response.status_code == 200:
    print("Success!")
    pages = response.json()

else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)

# Load the dataset
df = pd.DataFrame(pages)

# Prepare data for insertion
def prepare_record(row):
    """Prepare a record for insertion into the vector store.

    Args:
        row (pandas.Series): A row from the dataset containing an 'article' column.

    Returns:
        pandas.Series: A series containing the prepared record for insertion.

    Note:
        This function uses the current time for the UUID. To use a specific time,
        create a datetime object and use uuid_from_time(your_datetime).
    """

    content = row['content']
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "uid": row["id"],
                "created_at": datetime.now().isoformat(),
                "source": "event",
                "lang": "no"
            },
            "contents": content,
            "embedding": embedding,
        }
    )

records_df = df.apply(prepare_record, axis=1)

# Create tables and insert data
vec.create_tables()
vec.create_index()  # DiskAnnIndex
vec.create_keyword_search_index()  # GIN Index
vec.upsert(records_df)