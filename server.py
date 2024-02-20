from flask import Flask, render_template, request
import requests
import matplotlib
matplotlib.use('Agg')  # Use Agg backend (non-GUI)
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dash.html', specific_state_object=None)

@app.route('/getdata', methods=['GET'])
def getdata():
    target_state = request.args.get('target_state')

    response = requests.get("https://api.covidtracking.com/v1/states/current.json")

    if response.status_code == 200:
        data = response.json()
        specific_state_object = next((state for state in data if state['state'] == target_state), None)

        # Generate the plot
        dates = [entry["date"] for entry in data]
        positive_cases = [entry["positive"] for entry in data]
        dates = [datetime.strptime(str(date), "%Y%m%d") for date in dates]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, positive_cases, marker='o', linestyle='-', color='b')
        plt.title('Positive Cases Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Positive Cases')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)

        # Convert the image to a base64 string
        img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

        plt.close()  # Close the plot to free up resources

        return render_template('dash.html', specific_state_object=specific_state_object, plot=img_base64)
    else:
        print(f"Error: {response.status_code}")
        return 0

if __name__ == '__main__':
    app.run(debug=True)
