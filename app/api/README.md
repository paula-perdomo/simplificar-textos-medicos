# BioMedical Text Simplification API

This API provides a service to generate and evaluate Plain Language Summaries (PLS) from biomedical abstracts. It uses a large language model to simplify complex medical texts and provides readability scores for both the original and the simplified versions.

## Folder Structure

```
c:\\Users\\perdo\\Documents\\GitHub\\simplificar-textos-medicos\\app\\api\\
├───__init__.py
├───.gitignore
├───Dockerfile
├───main.py
├───README.md
├───requirements.txt
├───__pycache__\\
├───.vscode\\
├───core\\
│   ├───__init__.py
│   ├───class_model.py
│   ├───classifier_model.py
│   ├───model_loader.py
│   ├───prompt_template.py
│   ├───scoring.py
│   ├───secret_manager.py
│   ├───text_cleaning.py
│   └───__pycache__\\
├───model\\
│   └───pls_classifier\\...
└───ui\\
    ├───index.html
    ├───pico.jade.min.css
    ├───script.js
    └───style.css
```

## Folder and File Explanations

-   **`main.py`**: The main entry point for the FastAPI application. It defines the API endpoints, handles requests, and integrates the other components.
-   **`Dockerfile`**: Contains the instructions to build a Docker image for the application. It sets up the Python environment, installs dependencies, and configures the container to run the FastAPI server.
-   **`requirements.txt`**: Lists the Python dependencies required for the project.
-   **`core/`**: This directory contains the core logic of the application.
    -   **`class_model.py`**: Defines the Pydantic models for the request and response bodies, ensuring data validation and serialization.
    -   **`classifier_model.py`**: Handles the loading and execution of the text classification model.
    -   **`model_loader.py`**: Handles the loading of the language model and tokenizer.
    -   **`prompt_template.py`**: Contains the prompt template used to instruct the language model on how to generate the PLS.
    -   **`scoring.py`**: Contains the logic for calculating readability scores.
    -   **`secret_manager.py`**: Manages secrets from AWS Secret Manager.
    -   **`text_cleaning.py`**: Provides functions for cleaning text before processing.
-   **`model/`**: This directory is intended to store the language model files.
    -   **`pls_classifier/`**: Contains the text classification model.
-   **`ui/`**: This directory contains the user interface for the application.
    -   **`index.html`**: The main HTML file for the UI.
    -   **`script.js`**: The JavaScript file that handles the interaction with the API.
    -   **`style.css`** and **`pico.jade.min.css`**: The CSS files for styling the UI.

## Environment Variables

The following environment variables are used to configure the application:

-   **`S3_BUCKET_NAME`**: The name of the S3 bucket where the model files are stored. This is required if `MODEL_SOURCE` is `s3`.
-   **`S3_PREFIX`**: The prefix of the S3 bucket where the model files are stored. This is required if `MODEL_SOURCE` is `s3`.
-   **`S3_REGION`**: The region of the S3 bucket. This is required if `MODEL_SOURCE` is `s3`.
-   **`MODEL_PATH`**: The path to the language model. If `MODEL_SOURCE` is `s3`, this can be a local path: `"./model/llm/"`. If `MODEL_SOURCE` is `huggingface`, this can be a model identifier from the Hugging Face Hub: `"meta-llama/Llama-3.2-3B-Instruct"`.
-   **`MODEL_NAME`**: The name of the model being used. This is displayed in the UI.
-   **`MODEL_SOURCE`**: The source of the model. It can be `s3` or `huggingface`.
-   **`HF_TOKEN_SOURCE`**: The source of the Hugging Face authentication token. It can be `local` or `aws`.
-   **`HF_TOKEN`**: If `huggingface` is the `MODEL_SOURCE`, this is the Hugging Face authentication token. This is required to download models from the Hugging Face Hub. If `HF_TOKEN_SOURCE` is `'local'`, you must provide the value of this variable. If `HF_TOKEN_SOURCE` is `'aws'` It will be retrieved from AWS Secret Manager.

## How to Run

### Using Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t biomedical-text-simplification --secret id=hf_token,src=$HOME/.huggingface/token .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 biomedical-text-simplification
    ```

### Running Locally

1.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set the environment variables:**

    ```bash
    export S3_BUCKET_NAME="maia-grupo-9"
    export S3_PREFIX="/models/sft2-merged/"
    export S3_REGION="us-east-2"
    export MODEL_NAME="Llama-3.2-3B-Instruct"
    export MODEL_PATH="./model/llm/"
    export MODEL_SOURCE="s3"
    
    
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --host 127.0.0.1 --port 8000
    ```

The API will be available at `http://127.0.0.1:8000`.
The UI will be available by opening the `ui/index.html` file in your browser.

This README file was generated with help of AI.