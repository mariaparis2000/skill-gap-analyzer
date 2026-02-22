import google.generativeai as genai

genai.configure(api_key="AIzaSyB7naAM-RU-tqUJ31jYAIm7t27VsSD-Bvo")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)