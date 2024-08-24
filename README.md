# AI Vulnerability Remediation Demo

## Overview

This project is an AI-powered web application that generates detailed, instruction-style solutions for cybersecurity vulnerabilities. The application allows users to select a vulnerability from a dropdown list, and the system generates a solution based on predefined data. The generated solution is displayed in a user-friendly format, including clickable links that open in a new tab.

## Project Structure

The project is organized as follows:

```
panoptic.ai/
├── config/
│   └── .env
├── demodata/
│   ├── prompt_template.txt
│   └── vuln_list.csv
├── demofunctions/
│   └── generate.py
├── envdemo/               # Virtual environment
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   └── secuvantlogo.png
│   └── js/
├── templates/
│   └── index.html
├── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Folder Descriptions

- **`config/`**: Contains the `.env` file, which stores environment variables, such as API keys, securely.
  
- **`demodata/`**: Includes the `prompt_template.txt`, which contains the template for generating solutions, and `vuln_list.csv`, which stores the data for vulnerabilities used in the dropdown.

- **`demofunctions/`**: Contains `generate.py`, which defines the `generate_solution` function. This function interfaces with the AI model to produce the remediation solutions.

- **`envdemo/`**: The virtual environment directory where all the project's Python dependencies are installed.

- **`static/`**: Contains static assets like CSS stylesheets, images, and JavaScript files.

- **`templates/`**: Contains the `index.html` file, which is the main template for the web application's front-end.

- **`main.py`**: The entry point of the Flask application. It handles routing, data processing, and rendering the HTML templates.

- **`.gitignore`**: Specifies files and directories that should be ignored by Git, such as the virtual environment and any sensitive files.

- **`README.md`**: The file you're reading now, providing an overview of the project.

- **`requirements.txt`**: Lists all the Python dependencies required to run the project.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wilso27/panoptic.ai.git
   cd panoptic.ai
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv envdemo
   source envdemo/bin/activate  # On Windows use `envdemo\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the `.env` file**:
   - Create a `.env` file in the `config/` directory with your environment variables, such as your API keys.

5. **Run the application**:
   ```bash
   python main.py
   ```
   - The application will run locally on `http://127.0.0.1:5000/`.

## Code Explanation

### `main.py`

This is the main entry point of the application, which sets up the Flask web server. The key functions are:

- **`index()`**: Renders the homepage with the dropdown list of vulnerabilities.
- **`generate_solution_route()`**: Handles form submissions, retrieves data from the CSV, passes it to the `generate_solution` function, and renders the generated response.

### `generate.py`

This module defines the `generate_solution` function, which interacts with the AI model to generate the remediation solution based on the provided inputs.

- **`generate_solution()`**: 
  - Loads the AI model and template. (llama 3.1 70b)
  - Substitutes the provided vulnerability details into the template.
  - Processes the output to format it correctly, including converting URLs to markdown links.

### `styles.css`

The CSS file contains styles for the HTML elements to ensure the application has a modern and responsive design. Key styles include layout adjustments, button designs, and loading animations.

## Deployment

This project can be deployed on any platform that supports Python and Flask. Here are the basic steps to deploy on [Vercel](https://vercel.com/) (assuming you've set up the project and tested it locally):

1. **Initialize Vercel in the project directory**:
   ```bash
   vercel init
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

For more details on deployment, consult the Vercel documentation.