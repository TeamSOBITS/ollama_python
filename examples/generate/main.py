from ollama import generate


response = generate('llama3', 'Why is the sky blue?')
print(response['response'])
