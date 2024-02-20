from flask import Flask, render_template, request
import requests


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dash.html',  specific_state_object=None)

@app.route('/getdata', methods=['GET'])
def getdata():

    target_state = request.args.get('target_state')
    

    response = requests.get("https://api.covidtracking.com/v1/states/current.json")

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Find the specific object for the desired state
        specific_state_object = next((state for state in data if state['state'] == target_state), None)
        return render_template('dash.html', specific_state_object=specific_state_object)
    else:
        print(f"Error: {response.status_code}")
        return 0
       
    

if __name__ == '__main__':
    app.run(debug=True)
