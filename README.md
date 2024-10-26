
# Discharge summaries from the Mimic dataset 

This repository creates LLM-generated discharge summaries from electronic health record data from the [MIMIC-IV demo dataset](https://physionet.org/content/mimic-iv-demo/2.2/). The objective of the project was to see how well an LLM could perform at generating discharge summaries from electronic health record data. The input dataset contains lists of patients, admissions, lab results, prescriptions and procedures, but no free text clinical notes. I wanted to see whether an LLM could reconstruct the narrative of an admission using only the key events of the admission. 

## Get the data
The dataset was downloaded [from physionet](https://physionet.org/content/mimic-iv-demo/2.2/) to /data. The data is subdivided into hospital (/hosp) and ICU (/icu) data. For this project, I have used /hosp only.

## Repository contents
- extract_files.py - extract the compressed files
- data_to_database.py - read files into an SQL database and save
- find-headings.ipynb - explore the columns in the database
- collate_data_over_subjects.py - create a text file containing all the records for each patient
- generate-model-inputs.ipynb - use the above modules
- pass_to_model.py and pass_to_model.ipynb - send the data to gemini 

## Model
Google's Gemini 1.5 pro model was used via Vertex AI. This LLM was selected for [data privacy reasons](https://physionet.org/news/post/gpt-responsible-use); user prompts are not used for model training with Gemini.

## Example output
- manual experimentation to get best outputs
- found that best output was 
- experimented with prompt and temperature
