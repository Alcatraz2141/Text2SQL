# Text2SQL
Fetch data from SQL Database using Natural language
![image](https://github.com/Alcatraz2141/Text2SQL/assets/83905457/9f5205e3-c9be-49b3-858a-d6bccd322476)


## Overview
Text2SQL project is aimed at developing a system that can interpret natural language queries and convert them into equivalent SQL queries and execute them using LLMs. Leveraging natural language processing (NLP) and semantic parsing techniques, Text2SQL bridges the gap between human language and structured query languages. This approach enables users to interact with databases more intuitively.


## Getting Started
To run the  ChatBot project locally, follow these steps:

1. **Clone the Repository**: git clone {repo url}

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies: pip install -r requirements.txt

3. **Add Google API Key**: Obtain OPENAI API key and add it to the .env file in the project directory: OPENAI_API_KEY=your_openai_api_key

4. **Add DATABASE Details**: Obtain Database details like Hostname, Username, password, Database name and add it to the .env file in the project directory.

5. **Run the Project**: Launch the chatbot application using Streamlit: streamlit run NL2SQL.py

5. **Interact with the ChatBot**: Open your web browser and navigate to the provided URL to interact with  ChatBot.

## Project Structure
The project structure is organized as follows:

- NL2SQL.py: Main application file containing the Streamlit user interface and chatbot functionality.

- requirements.txt: List of Python dependencies required to run the project.

- .env: Environment configuration file for storing sensitive information (e.g., API keys).

- README.md: Project documentation file.


