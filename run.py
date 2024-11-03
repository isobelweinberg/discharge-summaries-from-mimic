from pass_to_model import generate
import os
import google.api_core.exceptions

input_dir = "data/mimic-iv-clinical-database-demo-2.2/subject-data"
output_dir = "data/mimic-iv-clinical-database-demo-2.2/output-data"
input_files = os.listdir(input_dir)

prompts = {
    "short_prompt": """Please write a discharge summary for this patient based on the data supplied. Write one discharge summary for each admission. Give any dates in UK format (dd/mm/yyyy).""",
    "long_prompt": """You are a doctor writing a discharge summary of a patient's admission or admissions. Please use the information given to write a clinical narrative for the patient relating to their hospital admission. If they had more than one hospital admission please deal with these separately. Please give the key diagnosis of the admission and other issues. Give each of these on a new line. Include relevant test findings in a succinct manner e.g. do not include antibiotic sensitivities for a microbiolgy result. Where dates are included, give these in British English format (dd/mm/yyyy). Do not include timestamps. Do not include diagnosis codes. Use the following headings and use markdown formatting to make each one bold and start on a new line: Patient ID, Patient Age, Admission Date, Discharge Date, Diagnosis, Other issues during admission, History of presenting complaint, Hospital course, Discharge medications, Discharge plan"""
}

for promptkey, prompt in prompts.items():
    print(promptkey)
    for file in input_files:
        
        output_file = file.replace('.txt', '.md')
        output_subdir = output_dir + "/" + promptkey
        
        if not os.path.exists(output_subdir): # create a new subdirectory for each prompt
            os.makedirs(output_subdir)

        if len(os.listdir(output_subdir)) >= 60: # switch prompts after 60 files
            continue
        
        print(file.removesuffix('.txt'))

        if output_file not in os.listdir(output_subdir):
            try:
                response = generate(input_dir + "/" + file, prompt)
                with open(output_subdir + "/" + output_file, "w+") as f:
                    f.write(response)
                print(output_file + " created")
            except google.api_core.exceptions.InvalidArgument:
                print("Error in model. Skipping " + output_file)
        else:
            print(output_file + " already exists")
        