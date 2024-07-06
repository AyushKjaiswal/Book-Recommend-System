# Book Recommend System

## Project Description
An application that recommends books and creates summaries of books based on user preferences.

## Dependencies

### 1. Configure Ollama and Llama3
As we are using the Llama 3 8B parameter size model, we will be running that using Ollama. Follow the steps below to install Ollama.

1. Browse to the URL [https://ollama.com/download](https://ollama.com/download) to download the Ollama installer based on your platform.
2. Follow the instructions to install and run Ollama for your OS.
3. Once installed, follow the commands below to download the Llama3 model.
    ```sh
    ollama run llama3
    ```

### 2. Install the libraries using `requirements.txt`
Run the command below to install the necessary libraries:
```sh
pip install -r requirements.txt
```

### 3. Create `.env` file using `.env_example` 
Add your AWS RDS Postgres URI, PORT, and Swagger.yaml file path in the .env file.

## Usage
1. Run the application with the following command:
```sh
python app.py
```
2. Swagger UI BASE URL [http://localhost:5000/apidocs]


## Features
1. Book recommendations based on user preferences.
2. Generation of book summaries.
3. Everything on your local machine, no need to use online/cloud LLM.