# API de Simplificación de Textos Biomédicos

Esta API proporciona un servicio para generar y evaluar Resúmenes en Lenguaje Sencillo (PLS, por sus siglas in inglés) a partir de resúmenes biomédicos. Utiliza un modelo de lenguaje grande para simplificar textos médicos complejos y proporciona puntuaciones de legibilidad tanto para la versión original como para la simplificada.

## Estructura de Carpetas

```
c:\Users\perdo\Documents\GitHub\simplificar-textos-medicos\app\ 
├───__init__.py
├───.gitignore
├───Dockerfile
├───main.py
├───README.md
├───requirements.txt
├───__pycache__\
├───.vscode\
├───core\
│   ├───__init__.py
│   ├───class_model.py
│   ├───classifier_model.py
│   ├───model_loader.py
│   ├───prompt_template.py
│   ├───scoring.py
│   ├───secret_manager.py
│   ├───text_cleaning.py
│   └───__pycache__\
├───model\
│   └───pls_classifier\...
└───ui\
    ├───index.html
    ├───pico.jade.min.css
    ├───script.js
    └───style.css
```

## Explicación de Carpetas y Archivos

-   **`main.py`**: El punto de entrada principal para la aplicación FastAPI. Define los puntos de conexión de la API, maneja las solicitudes e integra los demás componentes.
-   **`Dockerfile`**: Contiene las instrucciones para construir una imagen de Docker para la aplicación. Configura el entorno de Python, instala las dependencias y configura el contenedor para que ejecute el servidor FastAPI.
-   **`requirements.txt`**: Enumera las dependencias de Python necesarias para el proyecto.
-   **`core/`**: Este directorio contiene la lógica principal de la aplicación.
    -   **`class_model.py`**: Define los modelos Pydantic para los cuerpos de las solicitudes y respuestas, asegurando la validación y serialización de los datos.
    -   **`classifier_model.py`**: Maneja la carga y ejecución del modelo de clasificación de texto.
    -   **`model_loader.py`**: Maneja la carga del modelo de lenguaje y el tokenizador.
    -   **`prompt_template.py`**: Contiene la plantilla de aviso utilizada para instruir al modelo de lenguaje sobre cómo generar el PLS.
    -   **`scoring.py`**: Contiene la lógica para calcular las puntuaciones de legibilidad.
    -   **`secret_manager.py`**: Gestiona los secretos de AWS Secret Manager.
    -   **`text_cleaning.py`**: Proporciona funciones para limpiar el texto antes de procesarlo.
-   **`model/`**: Este directorio está destinado a almacenar los archivos del modelo de lenguaje.
    -   **`pls_classifier/`**: Contiene el modelo de clasificación de texto.
-   **`ui/`**: Este directorio contiene la interfaz de usuario para la aplicación.
    -   **`index.html`**: El archivo HTML principal para la interfaz de usuario.
    -   **`script.js`**: El archivo JavaScript que maneja la interacción con la API.
    -   **`style.css`** y **`pico.jade.min.css`**: Los archivos CSS para estilizar la interfaz de usuario.

## Variables de Entorno

Las siguientes variables de entorno se utilizan para configurar la aplicación:

-   **`S3_BUCKET_NAME`**: El nombre del bucket S3 donde se almacenan los archivos del modelo. Esto es necesario si `MODEL_SOURCE` es `s3`.
-   **`S3_PREFIX`**: El prefijo del bucket S3 donde se almacenan los archivos del modelo. Esto es necesario si `MODEL_SOURCE` es `s3`.
-   **`S3_REGION`**: La región del bucket S3. Esto es necesario si `MODEL_SOURCE` es `s3`.
-   **`MODEL_PATH`**: La ruta al modelo de lenguaje. Si `MODEL_SOURCE` es `s3`, puede ser una ruta local: "./model/llm/". Si `MODEL_SOURCE` es `huggingface`, puede ser un identificador de modelo del Hugging Face Hub: "meta-llama/Llama-3.2-3B-Instruct".
-   **`MODEL_NAME`**: El nombre del modelo que se está utilizando. Esto se muestra en la interfaz de usuario.
-   **`MODEL_SOURCE`**: El origen del modelo. Puede ser `s3` o `huggingface`.
-   **`HF_TOKEN_SOURCE`**: El origen del token de autenticación de Hugging Face. Puede ser `local` o `aws`.
-   **`HF_TOKEN`**: Si `huggingface` es el `MODEL_SOURCE`, este es el token de autenticación de Hugging Face. Esto es necesario para descargar modelos del Hugging Face Hub. Si `HF_TOKEN_SOURCE` es 'local', debe proporcionar el valor de esta variable. Si `HF_TOKEN_SOURCE` es 'aws', se recuperará de AWS Secret Manager.

## Cómo desplegar la aplicación

### Usando AWS

#### Para instalación en EC2 de la API:
1. Crear un EC2 con imagen Ubuntu 20.04 x64, 70 GB de disco y tier g4dn.xlarge
2. Conectarse por medio de ssh a la instancia
3. Seguir los siguientes comandos:
  ```bash
  sudo apt-get remove docker docker-engine docker.io containerd runc
  sudo apt-get update
  sudo apt-get install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
  echo \
      "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
       \"$(. /etc/os-release && echo \"$VERSION_CODENAME\")\" stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  git clone https://github.com/paula-perdomo/simplificar-textos-medicos.git
  sudo apt install git-lfs
  cd biomedical-text-simplification/app/
  git lfs pull
  sudo docker build -t biomedical-text-simplification:latest .
  sudo docker run -p 8000:8000 biomedical-text-simplification
  ```
4. Exponer el puerto 8000 a todo ipv4

#### Para instalación de pagina web en S3:

1. Crear S3 bucket. 
1. Actualizar el valor de la variable `apiUrl` en el archivo `script.js` con la direccion url donde se encuentra alojada la api.
2. Copiar los archivos de la carpeta [ui](https://github.com/paula-perdomo/simplificar-textos-medicos/tree/main/app/ui) en la raiz del bucket.
3. Configurarlo como pagina estatica.

### Usando Docker

1.  **Construir la imagen de Docker:**

    ```bash
    docker build -t biomedical-text-simplification:latest --secret id=hf_token,src=$HOME/.huggingface/token . 
    ```

2.  **Ejecutar el contenedor de Docker:**

    ```bash
    docker run -p 8000:8000 biomedical-text-simplification
    ```

### Ejecutando Localmente

1.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Establecer las variables de entorno:**

    ```bash
    export S3_BUCKET_NAME="maia-grupo-9"
    export S3_PREFIX="/models/sft2-merged/"
    export S3_REGION="us-east-2"
    export MODEL_NAME="Llama-3.2-3B-Instruct"
    export MODEL_PATH="./model/llm/"
    export MODEL_SOURCE="s3"
    export HF_TOKEN_SOURCE="local"
    export HF_TOKEN="YOUR_TOKEN"
    ```

3.  **Ejecutar la aplicación:
    ```bash
    uvicorn main:app --host 127.0.0.1 --port 8000
    ```

La API estará disponible en `http://127.0.0.1:8000`.
La interfaz de usuario estará disponible abriendo el archivo `ui/index.html` en su navegador.

Este archivo README fue generado con la ayuda de IA.
