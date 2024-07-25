import openai
import os


from openai import OpenAI



# Read OpenAI API key from file
def read_api_key():
    """
    Reads the OpenAI API key from a file.

    This function opens a file located at ".keys/open-api-key.txt" and reads the API key from it.

    Returns:
    str: The API key as a string.
    """
    with open(".keys/openai-api-key.txt", 'r') as file:
        return file.read().strip()


def verify_prediction_with_chatgpt(prediction):
    """
    Verifies a prediction using ChatGPT.

    This function sends a prompt to ChatGPT asking if a given prediction has come true.
    It then processes the response to determine if the prediction is true or false.

    Parameters:
    prediction (str): The prediction to be verified.

    Returns:
    str: "true" if the prediction is verified as true, "false" otherwise.
    """

    try:
        print(1)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that helps verify predictions."},
                {"role": "user", "content": f"Has the following prediction come true? {prediction}"}
            ]
        )
        print(response)
        print(2)
        answer = response['choices'][0]['message']['content'].strip()
        print(answer)
        return "true" if "yes" in answer.lower() else "false"
    except openai.RateLimitError:
        return "error: rate limit exceeded"
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "error"



        


client = OpenAI(
    api_key = read_api_key()
)


chatgpt_available = True
if not verify_prediction_with_chatgpt("Does the earth revolve around the moon?"):
    print("Error: Failed to verify prediction with ChatGPT")
    chatgpt_available = False
else:
    print("ChatGPT is available")


