import requests
from urls import urls
from dotenv import load_dotenv
from os import environ

load_dotenv("../.env")

# API endpoint URL
base = "http://127.0.0.1:5000/"
data = {
    "host": environ.get("USER"),
    "api_key": environ.get("USER_API_KEY")
}

call = "<action:str>"

# Send POST request with data
response = requests.post(base+call, json={**data, **urls[call]})

# Check the status code of the response
if response.status_code == 200:
    # Request successful
    print("Request successful")
elif response.status_code == 201:
    # Resource created
    print("Resource created")
    print("New resource location:", response.headers.get('Location'))
elif response.status_code == 204:
    # No content
    print("Request successful, but no content returned")
elif response.status_code == 400:
    # Bad request
    print("Bad request. Check your syntax or parameters.")
elif response.status_code == 401:
    # Unauthorized
    print("Unauthorized. Authentication required.")
elif response.status_code == 403:
    # Forbidden
    print("Forbidden. You do not have sufficient permissions.")
elif response.status_code == 404:
    # Not found
    print("Resource not found. Verify the URL or parameters.")
elif response.status_code == 500:
    # Internal server error
    print("Internal server error. Please try again later.")
else:
    # Other status codes
    print("Request failed with status code:", response.status_code)
print("Response content:", response.json())
