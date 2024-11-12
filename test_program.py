import requests

# URL for microservice
url = "http://127.0.0.1:5000/api/plates"

# Example data to be sent to microservice
example_data = {
    "totalWeight": 185,
    "barWeight": 45,
    "plateOptions":[45, 35, 25, 10, 5, 2.5]
}

# HTTP Post request
response = requests.post(url, json=example_data)

results = response.json()

# Print results to confirm they match what was promised
# Also demonstrates how to access the results
print(results['lbs'])
print(results['kgs'])
print(results['funUnits'])
print(results['funUnits']['corgis'])
