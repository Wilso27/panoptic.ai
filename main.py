from flask import Flask, render_template, request
import pandas as pd
from demofunctions.generate import generate_solution  # Import the function
import os

app = Flask(__name__)

# Load CSV data
df = pd.read_csv('demodata/vuln_list.csv')

@app.route('/')
def index():
    titles = df['Title'].tolist()
    return render_template('index.html', titles=titles)

@app.route('/generate_solution', methods=['POST'])
def generate_solution_route():
    selected_title = request.form['title']
    
    # Retrieve the corresponding row from the dataframe
    vulnerability = df[df['Title'] == selected_title].iloc[0]
    
    # Extract the necessary details
    title = vulnerability['Title']
    diagnosis = vulnerability['Diagnosis']
    consequences = vulnerability['Consequence']
    solution = vulnerability['Solution']
    vulnerability_location = vulnerability['Detection Location(s)']
    
    # Pass these to the generate_solution function
    result = generate_solution(title, diagnosis, consequences, solution, vulnerability_location)
    
    # Render the response or return it to the client
    return render_template('index.html', titles=df['Title'].tolist(), generated_response=result)

if __name__ == '__main__':
    app.run(debug=True)
