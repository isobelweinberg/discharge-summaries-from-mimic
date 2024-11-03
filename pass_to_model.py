import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

def generate(filepath: str) -> str:
    project_name = "optimum-phalanx-439708-n4"
    vertexai.init(project=project_name, location="europe-west2")
    model = GenerativeModel(
        "gemini-1.5-pro-001",
    )
    
    with open(filepath, "rb") as fid:
        input = fid.read()

    document1 = Part.from_data(
        mime_type="text/plain",
        data=input,
    )
    text1 = """Please write a discharge summary for this patient based on the data supplied. Write one discharge summary for each admission. Give any dates in UK format (dd/mm/yyyy)."""

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        ]
    
    checktokens = model.count_tokens([document1, text1])

    if checktokens.total_tokens > 2000000:
        return "The input is too long. Please try again with a shorter input:" + filepath
    else:
        responses = model.generate_content(
        [document1, text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
        )

        text_responses = [response.text for response in responses]
        output = "".join(text_responses)
    return output
    
    # for response in responses:
    #     print(response.text, end="")


    