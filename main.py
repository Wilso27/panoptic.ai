from flask import Flask, render_template, request, jsonify
import pandas as pd
from demofunctions.generate import generate_solution, generate_chat_response
import markdown2
import re

app = Flask(__name__)

# Initialize chat history
chat_history = {}

# Load the CSV data
df = pd.read_csv('demodata/vuln_list.csv')

@app.route('/')
def index():
    titles = df['Title'].tolist()
    return render_template('index.html', titles=titles)

@app.route('/generate_solution', methods=['POST'])
def generate_solution_route():
    # NOTE: Initialize new chat history every time a new solution is generated
    
    selected_title = request.form['title']
    chat_history['selected_title'] = selected_title
    
    # Retrieve the corresponding row from the dataframe
    vulnerability = df[df['Title'] == selected_title].iloc[0]
    
    # Extract the necessary details
    title = vulnerability['Title']
    diagnosis = vulnerability['Diagnosis']
    consequences = vulnerability['Consequence']
    solution = vulnerability['Solution']
    vulnerability_location = vulnerability['Detection Location(s)']
    
    # Try generating the solution
    for _ in range(3):
        try:
            result = generate_solution(title, diagnosis, consequences, solution, vulnerability_location)
            break
        except:
            if _ == 2:
                result = "An error occurred while generating the solution. Please try again."
            continue
        
    # result = generate_solution(title, diagnosis, consequences, solution, vulnerability_location)
    chat_history["generated_solution"] = result
    
    # Convert the result from Markdown to HTML
    result_html = markdown2.markdown(result)
    
    # Add target="_blank" to all links and wrap them in brackets
    result_html = re.sub(r'<a href="(https?://[^\s]+)">see link</a>', r'<a href="\1" target="_blank">[see link]</a>', result_html)
    
    # Render the response with the selected title still in place
    return render_template('index.html', titles=df['Title'].tolist(), generated_response=result_html, selected_title=selected_title)

@app.route('/process_input', methods=['POST'])
def process_input():
    
    selected_title = chat_history['selected_title']
    
    # Retrieve the corresponding row from the dataframe
    vulnerability = df[df['Title'] == selected_title].iloc[0]
    
    # Extract the necessary details
    title = vulnerability['Title']
    diagnosis = vulnerability['Diagnosis']
    consequences = vulnerability['Consequence']
    solution = vulnerability['Solution']
    vulnerability_location = vulnerability['Detection Location(s)']
    vulnerability_info = {"title": title, "diagnosis": diagnosis, "consequences": consequences, "solution": solution, "vulnerability_location": vulnerability_location}
    
    data = request.json
    user_input = data.get('user_input')

    if 'history' not in chat_history:
        chat_history['history'] = {}
    if 'generated_solution' not in chat_history:
        chat_history['generated_solution'] = ""
    
    constructed_chat_history = ""
    for interaction in chat_history['history']:
        constructed_chat_history += "User: " + chat_history['history'][interaction]['user_input'] + "\n"
        constructed_chat_history += "AI: " + chat_history['history'][interaction]['ai_response'] + "\n"
    
    # Try generating the AI response
    for _ in range(3):
        try:
            ai_response = generate_chat_response(user_input, constructed_chat_history, chat_history['generated_solution'], vulnerability_info)
            break
        except:
            if _ == 2:
                ai_response = "An error occurred while answering your questions. Please try again."
            continue
    
    # Convert the AI response from Markdown to HTML
    #ai_response = generate_chat_response(user_input, constructed_chat_history, chat_history['generated_solution'], vulnerability_info)
    ai_response = markdown2.markdown(ai_response)
    ai_response = re.sub(r'<a href="(https?://[^\s]+)">see link</a>', r'<a href="\1" target="_blank">[see link]</a>', ai_response)
    ai_response = re.sub(r'<p>', r'<p class="no-margin">', ai_response)

    # Update the chat history
    interaction_number = len(chat_history['history'])
    chat_history['history'][f'interaction_{interaction_number}'] = {'user_input': user_input, 'ai_response': ai_response}

    # Return the response as JSON
    return jsonify(response=ai_response)


if __name__ == '__main__':
    app.run(debug=True)
