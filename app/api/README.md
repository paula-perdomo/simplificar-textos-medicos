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
│   ├───model_loader.py
│   ├───prompt_template.py
│   ├───scoring.py
│   └───__pycache__\\
├───model\\
│   └───llama_3_2_3b\\...
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
    -   **`model_loader.py`**: Handles the loading of the language model and tokenizer.
    -   **`prompt_template.py`**: Contains the prompt template used to instruct the language model on how to generate the PLS.
    -   **`scoring.py`**: Contains the logic for calculating readability scores.
-   **`model/`**: This directory is intended to store the language model files.
-   **`ui/`**: This directory contains the user interface for the application.
    -   **`index.html`**: The main HTML file for the UI.
    -   **`script.js`**: The JavaScript file that handles the interaction with the API.
    -   **`style.css`** and **`pico.jade.min.css`**: The CSS files for styling the UI.

## Environment Variables

The following environment variables are used to configure the application:

-   **`MODEL_PATH`**: The path to the language model. This can be a local path or a model identifier from the Hugging Face Hub.
-   **`MODEL_NAME`**: The name of the model being used. This is displayed in the UI.
-   **`HF_TOKEN`**: Your Hugging Face authentication token. This is required to download models from the Hugging Face Hub.

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
    export MODEL_PATH="meta-llama/Llama-3.2-3B-Instruct"
    export MODEL_NAME="Llama 3.2 3B Instruct"
    export HF_TOKEN="your_hugging_face_token"
    ```

3.  **Run the application:**
    ```bash
    uvicorn main:app --host 127.0.0.1 --port 8000
    ```

The API will be available at `http://127.0.0.1:8000`.
The UI will be available by opening the `ui/index.html` file in your browser.

This README file was generated using AI.