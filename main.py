from flask import Flask, render_template, request
from demofunctions.generate import generate_solution

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        title = request.form['title']
        diagnosis = request.form['diagnosis']
        consequences = request.form['consequences']
        solution = request.form['solution']
        vulnerability_location = request.form['vulnerability_location']

        response = generate_solution(title, diagnosis, consequences, solution, vulnerability_location)

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
