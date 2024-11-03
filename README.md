
# Discharge summaries from the Mimic dataset 
![](https://img.shields.io/badge/python-3.13-blue)

This repository creates LLM-generated discharge summaries from electronic health record data from the [MIMIC-IV demo dataset](https://physionet.org/content/mimic-iv-demo/2.2/). The objective of the project was to see how well an LLM could perform at generating discharge summaries from electronic health record data. The input dataset contains lists of patients, admissions, lab results, prescriptions and procedures, but no free text clinical notes. I wanted to see whether an LLM could reconstruct the narrative of an admission using only the key events of the admission. 

## Get the data
The dataset was downloaded from [physionet](https://physionet.org/content/mimic-iv-demo/2.2/) to /data. The data is subdivided into hospital (/hosp) and ICU (/icu) data. For this project, I have used /hosp only.

## Repository contents
- `extract_files.py` - extract the compressed files
- `data_to_database.py` - read files into an SQL database and save
- `find-headings.ipynb` - explore the columns in the database
- `collate_data_over_subjects.py` - create a text file containing all the records for each patient
- `generate-model-inputs.ipynb` - functions to use the above modules
- `pass_to_model.py` and `pass_to_model.ipynb` - send the data to gemini
- `run.py` - iterate over the subject files and send each one to the model 

## Model
Google's Gemini 1.5 pro model was used via Vertex AI. This LLM was selected for [data privacy reasons](https://physionet.org/news/post/gpt-responsible-use); user prompts are not used for model training with Gemini.

## Prompt optimisation
I experimented with the prompt to the LLM to get the best output. I tried techniques included giving the model a template to follow. Here are some example prompts I tried:

```
You are a doctor writing a summary of a patient's admission or admissions. Please use the information given to write a clinical narrative for the patient relating to their hospital admission. If they had more than one hospital admission please deal with these separately. Please give the key diagnosis of the admission and other issues. Give each of these on a new line. Include relevant test findings in a succinct manner e.g. do not include antibiotic sensitivities for a microbiolgy result. Where dates are included, give these in British English format (dd/mm/yyyy). Do not include timestamps. Do not include diagnosis codes. Please start your answer with the patient's gender, age and past medical history.
```

<code>
Please write a discharge summary for this patient based on the data supplied. Write one discharge summary for each admission. 
Give any dates in the UK format (dd/mm/yyyy). Do not comment on how the discharge summary could be improved.
Use the following template:
Discharge Summary
Patient ID:
Admission Date:
Discharge Date:
Diagnosis:
Other issues during admission:
History of presenting complaint:
Hospital course:
Discharge medications:
Discharge plan:
</code>

In the end, I settled on generating output from two prompts, a short one and a long one. This was the short prompt:

```
Please write a discharge summary for this patient based on the data supplied. Write one discharge summary for each admission. Give any dates in UK format (dd/mm/yyyy).
```
And this was the long one:
```
You are a doctor writing a discharge summary of a patient's admission or admissions. Please use the information given to write a clinical narrative for the patient relating to their hospital admission. If they had more than one hospital admission please deal with these separately. Please give the key diagnosis of the admission and other issues. Give each of these on a new line. Include relevant test findings in a succinct manner e.g. do not include antibiotic sensitivities for a microbiolgy result. Where dates are included, give these in British English format (dd/mm/yyyy). Do not include timestamps. Do not include diagnosis codes. Use the following headings and use markdown formatting to make each one bold and start on a new line: Patient ID, Patient Age, Admission Date, Discharge Date, Diagnosis, Other issues during admission, History of presenting complaint, Hospital course, Discharge medications, Discharge plan
```

I also experimented with model temperature (a measure of the model's creativity) and in the end settled on the default value of 1 (scale from 0 to 2.) 

## Input data
Alongisde the prompts above, I passed the model a datafile for each patient. This consisted of all the data in the database pertaining to that patient. I did not supply the model with headings or translate ICD-10 codes. Here is an example of ten lines of input for one patient:

```
(10000032, 22595853, '2180-05-06 22:23:00', '2180-05-07 17:15:00', None, 'URGENT', 'P874LG', 'TRANSFER FROM HOSPITAL', 'HOME', 'Other', 'ENGLISH', 'WIDOWED', 'WHITE', '2180-05-06 19:17:00', '2180-05-06 23:30:00', 0)
(10000032, 22841357, '2180-06-26 18:27:00', '2180-06-27 18:49:00', None, 'EW EMER.', 'P09Q6Y', 'EMERGENCY ROOM', 'HOME', 'Medicaid', 'ENGLISH', 'WIDOWED', 'WHITE', '2180-06-26 15:54:00', '2180-06-26 21:31:00', 0)
(10000032, 25742920, '2180-08-05 23:44:00', '2180-08-07 17:50:00', None, 'EW EMER.', 'P60CC5', 'EMERGENCY ROOM', 'HOSPICE', 'Medicaid', 'ENGLISH', 'WIDOWED', 'WHITE', '2180-08-05 20:58:00', '2180-08-06 01:44:00', 0)
(10000032, 29079034, '2180-07-23 12:35:00', '2180-07-25 17:55:00', None, 'EW EMER.', 'P30KEH', 'EMERGENCY ROOM', 'HOME', 'Medicaid', 'ENGLISH', 'WIDOWED', 'WHITE', '2180-07-23 05:54:00', '2180-07-23 14:00:00', 0)
(10000032, 22841357, 4, '2761', 9)
(10000032, 22841357, 7, 'V08', 9)
(10000032, 22841357, 3, '2875', 9)
(10000032, 22841357, 8, '3051', 9)
(10000032, 22841357, 6, '5715', 9)
(10000032, 22841357, 5, '496', 9)
```

## Example output for 3 patients
Here I display the model outputs for three patients. The input was kept the same but I varied the model instruction, and I show the output achieved with short prompt vs the long prompt (see above). 

A note on dates: for anonymisation purposes, for each patient, the dates in the MIMIC dataset have a random offset added to them, which is why the years look implausible. 

### Patient 10000032 (first admission)
Example discharge summary with short prompt:

> ## Discharge Summary: Admission ID 22595853
> 
> **Patient:** 10000032
> **Admission Date:** 06/05/2180
> **Discharge Date:** 07/05/2180
> **Admitting Diagnosis:** OTHER DISORDERS OF THE LIVER
> **Discharge Diagnosis:** OTHER DISORDERS OF THE LIVER
> **Admitting Service:** Transplant
> 
> **History of Present Illness:** The patient was admitted to the Transplant service from the Emergency Department on 06/05/2180 for management of liver disorder. 
> 
> **Hospital Course:** During her brief stay, the patient received intravenous fluids and medications including Heparin, Ipratropium Bromide Neb, Potassium Chloride, Raltegravir, Emtricitabine-Tenofovir (Truvada), Furosemide, Spironolactone, and Albuterol Inhaler.  She was also prescribed a Nicotine Patch, but it was not applied.  She received an Influenza Vaccine.
> 
> **Laboratory data:** The patient's laboratory data revealed abnormalities in AST, ALT, creatinine, and potassium. Hemoglobin was slightly low. Other labs were within normal limits.
> 
> **Discharge Medications:** 
> * Heparin 5000 units SC TID
> * Ipratropium Bromide Neb 1 neb Q6H
> * Raltegravir 400 mg PO BID
> * Emtricitabine-Tenofovir (Truvada) 1 tab PO daily
> * Furosemide 40 mg PO daily
> * Spironolactone 50 mg PO daily
> * Albuterol Inhaler 2 puffs Q4H PRN
> * Acetaminophen 500 mg PO Q6H PRN
> 
> **Discharge Instructions:** 
> * The patient was discharged home in stable condition. 
> * She was advised to follow up with her primary care physician for continued management of her liver disorder.

Example output with long prompt:
  
> **Patient ID**
> 10000032
> 
> **Patient Age**
> 52
> 
> **Admission Date**
> 06/05/2180
> 
> **Discharge Date**
> 07/05/2180
> 
> **Diagnosis**
> Other disorders of the liver
> 
> **Other issues during admission**
> Hypokalaemia 
> 
> **History of presenting complaint**
> The patient was transferred from another hospital. 
> 
> **Hospital course**
> She was found to be hypokalaemic and received potassium chloride replacement. A urine dipstick was positive for blood but urine culture showed mixed growth consistent with contamination.
> 
> **Discharge medications**
> 1. Emtricitabine-Tenofovir
> 2. Albuterol inhaler
> 3. Raltegravir 
> 4. Heparin 
> 5. Ipratropium bromide nebuliser
> 6. Acetaminophen
> 7. Nicotine patch
> 8. Furosemide
> 9. Spironolactone
> 
> **Discharge plan**
> The patient was discharged home.  

### Patient 10001217 (first admission)
Short prompt:

> ## Discharge Summary - Admission 1 (24597018)
> 
> **Patient:** 10001217
> **Admission Date:** 18/11/2157
> **Discharge Date:** 25/11/2157
> **Admitting Diagnosis:** Craniotomy except for trauma, encephalopathy, unspecified, streptococcus anginosus infection 
> **Discharge Diagnosis:**  Craniotomy except for trauma, encephalopathy, unspecified, resolved streptococcus anginosus infection 
> 
> **History of Present Illness:**
> 
> The patient is a 55 year old female who presented to the Emergency Department via ambulance on 18/11/2157 with altered mental status. Initial workup revealed encephalopathy and a history of recent craniotomy. She was admitted to the Surgical Intensive Care Unit (SICU) for close monitoring and further evaluation. During her SICU stay, she required supplemental oxygen and was started on IV antibiotics for a suspected abscess containing streptococcus anginosus. 
> 
> **Hospital Course:**
> 
> The patient's mental status gradually improved with treatment. She was transitioned from IV antibiotics to oral Metronidazole and Ceftriaxone and was able to tolerate a regular diet.  Physical and occupational therapy were consulted to assist with her functional recovery. 
> 
> **Discharge Medications:** 
> - Levetiracetam 1000mg BID PO
> - Senna 1 tablet BID PO/NG
> - Docusate Sodium 100mg BID PO/NG
> - Metronidazole 500mg TID PO/NG
> - Ceftriaxone 2g Q12H IV
> - Heparin 5000 units TID SC
> 
> **Discharge Instructions:**
> 
> - Follow up with neurology as instructed.
> - Continue with home physical and occupational therapy.
> - Take discharge medications as prescribed.

Long prompt:

> **Patient ID**
> 10001217
> 
> **Patient Age**
> 55
> 
> **Admission Date**
> 18/11/2157
> 
> **Discharge Date**
> 25/11/2157
> 
> **Diagnosis**
> Craniotomy except for trauma
> 
> **Other issues during admission**
> Encephalopathy
> Essential hypertension
> Hyponatraemia
> 
> **History of presenting complaint**
> The patient was admitted to hospital via the Emergency Department on 18/11/2157. She presented with headache.
> 
> **Hospital course**
> The patient was admitted to the Surgical Intensive Care Unit following attendance in the Emergency Department. She underwent a craniotomy. Her sodium level dropped to 123 mmol/L but was corrected. She also had a blood culture which showed no growth. There was growth of Fusobacterium nucleatum in an abscess sample and she completed a course of intravenous vancomycin and ceftriaxone.
> 
> **Discharge medications**
> Levetiracetam 1000mg twice a day
> Senna 2 tablets twice a day
> Docusate Sodium 100mg twice a day
> Heparin 5000 units three times a day
> Metronidazole 500mg three times a day
> Ondansetron 4mg when required every 8 hours
> Acetaminophen 650mg when required every 6 hours
> Oxycodone 5mg when required every 6 hours
> 
> **Discharge plan**
> Home health care.

### Patient 10001725 (first admission)

Short prompt:

> ## Discharge Summary 1 - Admission ID: 25563031
> 
> **Patient:** 10001725
> **Admission Date:** 11/04/2010
> **Discharge Date:** 14/04/2010
> **Admitting Diagnosis:** EW EMER.
> **Discharge Diagnosis:** Other
> 
> **History of Present Illness:** This 46-year-old, married, white female presented to the Emergency Department and was subsequently admitted for [reason for admission not provided].
> 
> **Hospital Course:** The patient was initially admitted to GYN on 11/04/2010 and transferred to the ICU shortly after. On 12/04/2010, she was transferred back to the Med/Surg/GYN unit and remained there until discharge. She received various medications including Cephalexin, Docusate Sodium, Nexium, Propranolol, HydrOXYzine, MethylPREDNISolone, Famotidine, Senna, Metolazone, Spironolactone, Trimethoprim, Polyethylene Glycol, Lorazepam, Ondansetron, Albuterol, Hydrocerin, Simethicone, and Zolpidem Tartrate. Some medications were discontinued due to change orders, expired, or were discontinued upon discharge. She also received an IV fluid of Lactated Ringers and was treated with an indwelling urinary catheter. Several labs were drawn throughout her stay, including a urine culture which showed Citrobacter freundii complex. She was treated with appropriate antibiotics based on the sensitivity report.
> 
> **Discharge Condition:** The patient's condition improved during her hospital stay. She was discharged home in stable condition. 
> 
> **Discharge Instructions:** The patient was advised to follow up with her primary care physician for continued management of her condition.

Long prompt:
> 
> **Patient ID:** 10001725
> **Patient Age:** 46
> **Admission Date:** 11/04/2010
> **Discharge Date:** 14/04/2010
> **Diagnosis:** Sepsis
> **Other issues during admission:** Urinary tract infection
> **History of presenting complaint:** This 46 year old lady presented via the Emergency Department on 11/04/2010 with abdominal pain, fever and dysuria.
> **Hospital course:** On presentation the patient was febrile and tachycardic. She was admitted to the Gynaecology ward under the care of Dr P35SU0. Examination revealed generalised abdominal tenderness. She was treated with intravenous fluids and antibiotics. She was reviewed by the surgical team who felt that her symptoms were gynaecological in nature and did not feel that surgical intervention was necessary. During the admission she was transferred to the Intensive Care Unit due to worsening sepsis. A urine culture grew Citrobacter freundii complex. Blood cultures were negative. A MRSA screen was negative. The patient's sepsis improved with treatment and she was able to be transferred back to the Gynaecology ward and was subsequently discharged.
> **Discharge medications:** 
> - Addenall 15mg three times a day
> - Propranolol LA 80mg once a day
> - Trimethoprim 100mg once a day
> - Sodium Chloride 0.9% Flush three times a day
> - Zolpidem Tartrate 5mg at night
> - Potassium Chloride 40mEq once a day
> - Docusate Sodium 100mg twice a day
> - Hydrocerin four times a day as required
> - Simethicone 40-80mg four times a day as required
> - HydrOXYzine 25mg once a day as required
> - Lorazepam 1mg once a day as required
> - Bisacodyl 10mg once a day as required
> - Albuterol 0.083% Neb Soln eight hourly as required
> **Discharge plan:** The patient was discharged home with a plan to follow up with her general practitioner. 
> 