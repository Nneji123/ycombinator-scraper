import requests

def generate_cold_email(name, job_description, co_founder_first_name, api_key):
    # Splitting the job description into chunks to fit within OpenAI's token limit
    job_chunks = [job_description[i:i+500] for i in range(0, len(job_description), 500)]
    
    # Constructing the prompt with each chunk
    prompt = f"Generate a cold email for the {name} applying for the {co_founder_first_name}-led company. {co_founder_first_name} is known for their innovative work. Here is the job description:\n\n"

    for chunk in job_chunks:
        prompt += f"{chunk}\n\n"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    data = {
        'model': 'text-davinci-002',
        'prompt': prompt,
        'max_tokens': 400,
        'temperature': 0.6,
    }

    response = requests.post('https://api.openai.com/v1/engines/text-davinci-002/completions', headers=headers, json=data)
    response_data = response.json()

    cold_email = response_data['choices'][0]['text']
    return cold_email


def generate_message():
  pass
