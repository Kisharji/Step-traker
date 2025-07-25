
from flask import Flask, render_template, request, redirect
import json
import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

# Load or initialize data
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    today = str(datetime.date.today())

    if today not in data:
        data[today] = {'steps': 0}

    if request.method == 'POST':
        height = float(request.form['height'])  # in cm
        new_steps = int(request.form['steps'])

        data[today]['steps'] += new_steps
        save_data(data)

    # Calculations
    steps = data[today]['steps']
    height = float(request.form['height']) if request.method == 'POST' else 170
    stride = 0.415 * height / 100  # in meters
    distance = stride * steps
    calories = 0.04 * steps

    return render_template('index.html', steps=steps, distance=round(distance, 2),
                           calories=round(calories, 2), data=data)

if __name__ == '__main__':
    app.run(debug=True)
