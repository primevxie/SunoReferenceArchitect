# 🎵 Suno Architect

**Reverse-engineer the "DNA" of any song and generate perfect Suno AI prompts.**

Suno Architect is a specialized tool that uses **Google Gemini 2.5 Flash** (Multimodal AI) to "listen" to your reference tracks. It extracts the genre, BPM, instruments, and vocal style, then converts that data into optimized tags for Suno v3.5/v4.

It also includes a **Lyric Density Calculator** to predict if your lyrics will fit the generated beat or if they will result in hallucinations/rushing.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red)
![Gemini](https://img.shields.io/badge/Powered%20By-Gemini%202.5-orange)

## ✨ Features

* **🎧 Audio Reverse Engineering:** Upload any MP3/WAV. The AI listens to the mix, vocal chain, and instrumentation.
* **🎛️ Instant Prompt Generation:** Get a copy-paste ready string of tags (e.g., `[Dark Synthwave, Ethereal Vocals, 140 BPM]`).
* **📊 Articulation Score:** The AI rates vocal clarity from 1 (Atmospheric/Slurred) to 10 (Crystal Clear).
* **📝 Lyric Flow Check:** Paste your lyrics to calculate "Syllable Density." The app warns you if your lyrics are too fast for the beat or too sparse for the genre.
* **🌍 Universal Support:** Works for **all genres** (Pop, Trap, Metal, Orchestral, Country, etc.).

## 🚀 Quick Start (Run Locally)

Prerequisites: Python installed and a [Google Gemini API Key](https://aistudio.google.com/app/apikey) (Free).

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/suno-architect.git](https://github.com/yourusername/suno-architect.git)
    cd suno-architect
    ```

2.  **Install requirements**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app**
    ```bash
    streamlit run app.py
    ```

4.  **Use the tool**
    * Enter your Gemini API Key in the sidebar.
    * Upload a reference track.
    * Copy the generated tags into Suno!

## 🧠 How It Works

1.  **Ingestion:** The app takes the raw audio bytes from your upload.
2.  **Multimodal Analysis:** It sends the audio directly to **Gemini 2.5 Flash**, a model capable of native audio understanding (not just text descriptions).
3.  **Extraction:** The system prompt instructs the AI to identify:
    * **BPM & Key**
    * **Vocal Texture** (Articulation rating)
    * **Instrumentation**
4.  **Math:** The app calculates the **Lyric Density** (Syllables / Seconds) and compares it against the **Articulation Score** to predict if Suno will generate a "clean" or "muddy" result.

## 📦 File Structure

* `app.py` - The complete application logic (Frontend + Backend).
* `requirements.txt` - Dependencies (`streamlit`, `google-generativeai`).
* `README.md` - Documentation.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
