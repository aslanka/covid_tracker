import requests

def get_state_data(api_url, target_state):
    # Make an API request to retrieve data about all states
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Find the specific object for the desired state
        specific_state_object = next((state for state in data if state['state'] == target_state), None)

        return specific_state_object
    else:
        print(f"Error: {response.status_code}")
        return None

# Example API endpoint
api_url = "https://api.covidtracking.com/v1/states/current.json"

# Example: Retrieve data for the state of Alaska
target_state = "AK"
result = get_state_data(api_url, target_state)

if result:
    print(result["positiveTestsViral"])
else:
    print(f"No data found for {target_state}")
