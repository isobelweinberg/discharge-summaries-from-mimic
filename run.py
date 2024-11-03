from pass_to_model import generate
import os
import google.api_core.exceptions

input_dir = "data/mimic-iv-clinical-database-demo-2.2/subject-data"
output_dir = "data/mimic-iv-clinical-database-demo-2.2/output-data"
input_files = os.listdir(input_dir)

for file in input_files:
    print(file.removesuffix('.txt'))
    output_file = file.replace('.txt', '.md')
    if output_file not in os.listdir(output_dir):
        try:
            response = generate(input_dir + "/" + file)
            with open(output_dir + "/" + output_file, "w+") as f:
                f.write(response)
            print(output_file + " created")
        except google.api_core.exceptions.InvalidArgument:
            print("Error in model. Skipping " + output_file)
    else:
        print(output_file + " already exists")