from flask import Flask, render_template, request, jsonify
import pandas as pd
from demofunctions.generate import generate_solution, give_dummy_answer
import markdown2
import re

app = Flask(__name__)

# Load the CSV data
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
    
    # Convert the result from Markdown to HTML
    result_html = markdown2.markdown(result)
    
    # Add target="_blank" to all links and wrap them in brackets
    result_html = re.sub(r'<a href="(https?://[^\s]+)">see link</a>', r'<a href="\1" target="_blank">[see link]</a>', result_html)
    
    # Render the response with the selected title still in place
    return render_template('index.html', titles=df['Title'].tolist(), generated_response=result_html, selected_title=selected_title)

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json
    user_input = data.get('user_input')

    # Call the dummy function and get the response
    dummy_response = give_dummy_answer(user_input)

    # Return the response as JSON
    return jsonify(response=dummy_response)


if __name__ == '__main__':
    app.run(debug=True)
