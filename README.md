# Importer-Microservice
The Importer microservice takes raw input and returns it as structured JSON that another program can use. It has two endpoints: /define looks up definitions for a list of words, and /parse-csv converts an uploaded CSV file into one record per row. Words that can’t be found and files that can’t be parsed are reported in an errors list, so the calling program can handle them without the service crashing.

**Communication Pipe**

REST API (HTTP requests with JSON responses)


**Request Data**

The microservice runs on its own and listens on a port (for example, http://localhost:5001). To get definitions, the main program sends a POST request to /define with a JSON body containing the word list. To parse a CSV, it sends a POST request to /parse-csv with the file attached.


**Request example**
```
import requests

url = "http://localhost:5001/define"
request_body = {
    "words": ["apple", "river"]
}

response = requests.post(url, json=request_body)
```

**Receive Data**

The microservice sends back an HTTP response with a JSON body. The body contains a status, a data list with successfully processed results, and an errors list for any items that could not be processed. If a request is valid but some words cannot be found, the microservice will still return a 200 OK response. Successfully processed words will appear in data, while any words that could not be found will appear in errors. If the entire request cannot be processed, such as when an invalid or improperly formatted CSV file is uploaded, the microservice will return a 400 Bad Request response with an error message.


**Recieve Example**
```
response_data = response.json()

if response.status_code == 200:
    for item in response_data["data"]:
        print(item["word"])
        print(item["definition"])

    if response_data["errors"]:
        print("Errors:", response_data["errors"])

else:
  print("Request failed:", response_data["errors"])
```
