# Simplificación de Textos Médicos

Este es el proyecto final de grado de la maestría en inteligencia artificial (MaIA) de la Universidad de los Andes.

## Resumen

Se entrenó un modelo Llama fine-tuned con técnica LoRA para la tarea de generación de resumenes simplificados de texto médico. Además, se entrenó un clasificador binario para clasificar si un texto es técnico o si ya ha sido simplificado. Finalmente, se buscó desarrollar un sistema robusto para evaluar dichos modelos, por lo que se compararon diferentes medidas de legibilidad como SMOG, FKG y FRE; también se midió la relevancia y factualidad con BERTScore y AlignScore, respectivamente.

Con estos modelos, se creó una API donde en un primer paso se utiliza el clasificador que define si el texto de entrada es simplificado o técnico, and si es este último, retorna el texto simplificado (utilizando el modelo fine-tuned). Junto con el texto simplificado generado se emiten las medidas de legibilidad del texto. Esta herramienta fue creada teniendo en mente al personal médico como usuario final.

### Enlaces relevantes

- Pagina web: [PLS Generator](http://maia-grupo-9.s3-website.us-east-2.amazonaws.com/)

## Uso

El flujo de interacción de la herramienta se inicia mediante un campo de entrada destinado al ingreso de texto médico. Al ejecutar la acción de generación, el sistema realiza una verificación preliminar del contenido para clasificar su naturaleza; si se determina que el texto ya corresponde a un Resumen en Lenguaje Sencillo (PLS), se notifica al usuario mediante un mensaje de error. En caso contrario, se procede con la inferencia utilizando el modelo Llama-3.2-3B-Instruct para la generación del resumen. Finalmente, la interfaz despliega el PLS resultante junto con una tabla comparativa de métricas de legibilidad, permitiendo al profesional validar objetivamente el grado de comprensibilidad alcanzado respecto al texto original.

## Dependencias

Se encuentran en el archivo [requirements.txt](https://github.com/paula-perdomo/simplificar-textos-medicos/blob/main/app/requirements.txt)

## Despliegue

### Entorno de ejecución

- **Backend**: Una api desarrollada en python con fastapi. La api esta hosteada en AWS EC2.
- **Modelo AI**:La api usa un modelo Llama-3.2-3B-Instruct entrenado. El modelo AI esta hosteado en AWS S3.
- **Frontend**: Una pagina web estatica desarrollada con html, javascript, css. Esta hosteada en AWS S3.

### Pasos de despliegue

Se implemento unos pipelines de despliegue continuo para la API y la interfaz usando Github Actions y AWS CodeDeploy. Estos se encargan de actualizar la version de la aplicacion en EC2 para la api y en S3 para la interfaz.

Adicionalmente puede seguir estos pasos para el despliegue.

#### Para instalación local de la API:
1. Instalar Docker Desktop
2. Clonar el repositorio
3. Abrir un command prompt en la carpeta donde se instaló el repositorio
4. Utilizar el comando  `docker build -t biomedical-text-simplification:latest .`
5. Utilizar el comando `docker run -p 8000:8000 biomedical-text-simplification`
6. La imagen docker va a quedar corriendo en tu máquina en `http://127.0.0.1:8000/docs`

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


## Credenciales

Credenciales para AWS:
```
aws_access_key_id="CREDENCIALES"
aws_secret_access_key="CREDENCIALES"
aws_session_token="CREDENCIALES"
```

Credenciales para HuggingFace:
```
HF_TOKEN="TOKEN"
```

## Ejemplos de uso.

<details>
<summary>Prueba 1. Texto medico 10.1002-14651858.CD014257.pub2-abstract.txt. Se pega en el campo de texto "Input" y se utiliza el boton generar. La aplicacion debe generar un PLS y popular la tabla comparativa.</summary>

Texto extraido de [bridging-the-gap-in-health-literacy:](https://github.com/feliperussi/bridging-the-gap-in-health-literacy/blob/main/data_collection_and_processing/Data%20Sources/Cochrane/train/non_pls/10.1002-14651858.CD014257.pub2-abstract.txt):

Background
Functional constipation is defined as chronic constipation with no identifiable underlying cause. It is a significant cause of morbidity in children, accounting for up to 25% of visits to paediatric gastroenterologists. Probiotic preparations may sufficiently alter the gut microbiome and promote normal gut physiology in a way that helps relieve functional constipation. Several studies have sought to address this hypothesis, as well as the role of probiotics in other functional gut disorders. Therefore, it is important to have a focused review to assess the evidence to date.
Objectives
To evaluate the efficacy and safety of probiotics for the management of chronic constipation without a physical explanation in children.
Search methods
On 28 June 2021, we searched CENTRAL, MEDLINE, Embase, CINAHL, AMED, WHO ICTR, and ClinicalTrials.gov, with no language, date, publication status, or document type limitations.
Selection criteria
We included randomised controlled trials (RCTs) that assessed probiotic preparations (including synbiotics) compared to placebo, no treatment or any other interventional preparation in people aged between 0 and 18 years old with a diagnosis of functional constipation according to consensus criteria (such as Rome IV).
Data collection and analysis
We used standard methodological procedures expected by Cochrane.
Main results
We included 14 studies (1127 randomised participants): 12 studies assessed probiotics in the treatment of functional constipation, whilst two studies investigated synbiotic preparations.
Three studies compared probiotics to placebo in relation to the frequency of defecation at study end, but we did not pool them as there was very significant unexplained heterogeneity. Four studies compared probiotics to placebo in relation to treatment success. There may be no difference in global improvement/treatment success (RR 1.29, 95% CI 0.73 to 2.26; 313 participants; low‐certainty evidence). Five studies compared probiotics to placebo in relation to withdrawals due to adverse events, with the pooled effect suggesting there may be no difference (RR 0.64, 95% CI 0.21 to 1.95; 357 participants; low‐certainty evidence).
The pooled estimate from three studies that compared probiotics plus an osmotic laxative to osmotic laxative alone found there may be no difference in frequency of defecation (MD ‐0.01, 95% CI ‐0.57 to 0.56; 268 participants; low‐certainty evidence). Two studies compared probiotics plus an osmotic laxative to osmotic laxative alone in relation to global improvement/treatment success, and found there may be no difference between the treatments (RR 0.95, 95% CI 0.79 to 1.15; 139 participants; low‐certainty evidence). Three studies compared probiotics plus osmotic laxative to osmotic laxative alone in relation to withdrawals due to adverse events, but it is unclear if there is a difference between them (RR 2.86, 95% CI 0.12 to 68.35; 268 participants; very low‐certainty evidence).
Two studies compared probiotics versus magnesium oxide. It is unclear if there is a difference in frequency of defecation (MD 0.28, 95% CI ‐0.58 to 1.14; 36 participants), treatment success (RR 1.08, 95% CI 0.74 to 1.57; 36 participants) or withdrawals due to adverse events (RR 0.50, 95% CI 0.05 to 5.04; 77 participants). The certainty of the evidence is very low for these outcomes.
One study assessed the role of a synbiotic preparation in comparison to placebo. There may be higher treatment success in favour of synbiotics compared to placebo (RR 2.32, 95% CI 1.54 to 3.47; 155 participants; low‐certainty evidence). The study reported that there were no withdrawals due to adverse effects in either group.
One study assessed a synbiotic plus paraffin compared to paraffin alone. It is uncertain if there is a difference in frequency of defecation (MD 0.74, 95% CI ‐0.96, 2.44; 66 participants; very low‐certainty evidence), or treatment success (RR 0.91, 95% CI 0.71 to 1.17; 66 participants; very low‐certainty evidence). The study reported that there were no withdrawals due to adverse effects in either group.
One study compared a synbiotic preparation to paraffin. It is uncertain if there is a difference in frequency of defecation (MD ‐1.53, 95% CI ‐3.00, ‐0.06; 60 participants; very low‐certainty evidence) or in treatment success (RR 0.86, 95% CI 0.65, 1.13; 60 participants; very low‐certainty evidence). The study reported that there were no withdrawals due to adverse effects in either group.
All secondary outcomes were either not reported or reported in a way that did not allow for analysis.
Authors' conclusions
There is insufficient evidence to conclude whether probiotics are efficacious in successfully treating chronic constipation without a physical explanation in children or changing the frequency of defecation, or whether there is a difference in withdrawals due to adverse events when compared with placebo. There is limited evidence from one study to suggest a synbiotic preparation may be more likely than placebo to lead to treatment success, with no difference in withdrawals due to adverse events.
There is insufficient evidence to draw efficacy or safety conclusions about the use of probiotics in combination with or in comparison to any of the other interventions reported. The majority of the studies that presented data on serious adverse events reported that no events occurred. Two studies did not report this outcome.
Future studies are needed to confirm efficacy, but the research community requires guidance on the best context for probiotics in such studies, considering where they should be best considered in a potential treatment hierarchy and should align with core outcome sets to support future interpretation of findings.

</details>

<details>
<summary>Prueba 2. Texto PLS generado por Gemini 2.5 flash. Se pega en el campo de texto "Input" y se utiliza el boton generar. La aplicacion debe generar un mensaje de error</summary>

Plain Language Summary: Do Probiotics Help Kids with Constipation?

Rationale

Many children have long-term constipation. This means they have trouble going to the bathroom often. Doctors call this ""functional constipation."" It means there is no clear reason for it. This problem can make kids feel bad. It can also cause many visits to children's stomach doctors.

Some people think special good germs, called probiotics, might help. These germs live in our gut. They may help the gut work better. This could help kids with constipation. We wanted to look at all the studies about probiotics for kids with this problem. We wanted to see if they really help.

Trial Design

We looked at many research studies. These studies were called ""randomized controlled trials."" This is a good way to test if a treatment works. We looked for studies that tested probiotics. We also looked for studies that tested ""synbiotics."" Synbiotics are probiotics with added food for the good germs.

These studies looked at children from birth up to 18 years old. All these kids had functional constipation. The studies compared probiotics or synbiotics to other things. These included a sugar pill (placebo), no treatment, or other medicines. We looked for studies that measured how often kids went to the bathroom. We also looked at how well the treatment worked overall. We also checked for any bad effects. We searched many databases for these studies up to June 2021.

Results

We found 14 studies to include. These studies had a total of 1127 children. Most studies looked at probiotics. Two studies looked at synbiotics.

Some studies compared probiotics to a sugar pill. We found it was not clear if probiotics helped kids go to the bathroom more often. It was also not clear if probiotics made kids feel better overall. The studies also showed that probiotics likely did not cause more bad effects than a sugar pill.

Other studies looked at probiotics plus a common laxative. A laxative is a medicine that helps you go to the bathroom. These studies compared that to just the laxative alone. Again, it was not clear if adding probiotics helped kids go to the bathroom more. It was also not clear if it helped them feel better. We are also unsure if there were more bad effects with probiotics.

Two studies compared probiotics to another medicine called magnesium oxide. It was not clear if probiotics were better for going to the a bathroom. It was also not clear if they made kids feel better or caused fewer bad effects.

One study looked at a synbiotic. This study found that the synbiotic might help kids feel better more often than a sugar pill. This study also said there were no bad effects. Other studies looked at synbiotics with other medicines. It was not clear if synbiotics made a difference in how often kids went to the bathroom. It was also not clear if they made kids feel better.

Overall, it's hard to say if probiotics work for kids with constipation. We need more studies to be sure. There is a small hint that synbiotics might help some kids. Most studies said there were no serious bad effects. More research is needed to find the best way to use probiotics for children's constipation.

</details>