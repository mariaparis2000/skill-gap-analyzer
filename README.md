# Skill-Gap AI Analyzer

Bridging the gap between your current profile and your target job requirements.

## 🚀 Features

- **Input system:** Upload your CV in PDF format or paste your professional summary directly.
- **AI-powered analysis:** Semantic skill matching using Google Gemini — understands context, not just keywords.
- **Interactive dashboard:**
  - **Compatibility metrics:** Overall match percentage with donut charts per category.
  - **Skill gap visualization:** Hard Skills, Soft Skills and Languages breakdown.
  - **Detailed checklist:** Visual confirmation of skills detected and skills missing.
- **AI Career Coach:** Personalized Gemini-generated advice to bridge your specific skill gaps, with three depth levels (Fast / Standard / Detailed).

## 🛠️ Technology Stack

- **Frontend/App Framework:** [Streamlit](https://streamlit.io/)
- **Language:** Python 3.x
- **AI Integration:** [Google Gemini API](https://aistudio.google.com/) via [`google-genai`](https://pypi.org/project/google-genai/) SDK — model `gemini-2.0-flash-lite`

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tu-usuario/skill-gap-analyzer.git
   cd skill-gap-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key:**

   - Get a free API key at [aistudio.google.com](https://aistudio.google.com/)
   - Create a `.streamlit/secrets.toml` file in the project root:
     ```toml
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - ⚠️ Never commit this file to GitHub — it's already in `.gitignore`

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## ☁️ Deploying to Streamlit Cloud

1. Push your code to GitHub (the `secrets.toml` will be ignored automatically)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. In **Settings → Secrets**, paste your key:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

## 🔒 Security

This project uses Streamlit's secrets management to keep API keys safe.
Never hardcode your API key directly in the code.