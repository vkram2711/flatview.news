import uuid

import requests
import json
from datetime import datetime

# Define the Notion API endpoint and headers
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_API_KEY = "secret_PmaWMk9oENUXiLzyyPZoOrH4g4HritdJTETkCdEfqDv"
DATABASE_ID = "24144319c6ba4ee888838d571d96f9e8"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def add_entry_to_notion(feedback, contact, rating):
    # Define the payload with the required fields
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Id": {
                "title": [
                    {
                        "text": {
                            "content": str(uuid.uuid4())
                        }
                    }
                ]
            },
            "Feedback": {
                "rich_text": [
                    {
                        "text": {
                            "content": feedback
                        }
                    }
                ]
            },
            "Contact": {
                "rich_text": [
                    {
                        "text": {
                            "content": contact
                        }
                    }
                ]
            },
            "Rating": {
                "number": rating
            },
            "Date": {
                "date": {
                    "start": datetime.now().isoformat()
                }
            }
        }
    }

    # Make a POST request to the Notion API with the payload
    response = requests.post(NOTION_API_URL, headers=headers, data=json.dumps(payload))

    # Handle the response
    if response.status_code == 200:
        print("Entry added successfully!")
    else:
        print(f"Failed to add entry: {response.status_code}, {response.text}")
