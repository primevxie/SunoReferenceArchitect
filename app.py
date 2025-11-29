import streamlit as st
import google.generativeai as genai
import json
import os
import re

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Suno Prompt Architect", page_icon="🎹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #0E0E0E; color: white; }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea { 
            background-color: #1E1E1E; color: white; border-radius: 8px; border: 1px solid #333; 
        }
        .stButton > button { 
            background-color: #FF0050; color: white; border-radius: 20px; border: none; font-weight: bold; width: 100%; transition: 0.3s;
        }
        .stButton > button:hover { background-color: #E60045; transform: scale(1.02); }
        [data-testid="stSidebar"] { background-color: #121212; border-right: 1px solid #333; }
        h1, h2, h3, h4 { color: #FFFFFF; font-family: 'Inter', sans-serif; }
        
        .metric-box { background: #1A1A1A; padding: 15px; border-radius: 10px; border: 1px solid #333; text-align: center; }
        .metric-val { font-size: 1.5em; font-weight: bold; color: #FF0050; }
        .metric-lbl { font-size: 0.8em; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTION ---
def extract_number(value):
    """Robustly extracts numbers from AI responses like '4/10 (High)' -> 4"""
    if isinstance(value, (int, float)):
        return int(value)
    match = re.search(r'\d+', str(value))
    return int(match.group()) if match else 0

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎹 Architect")
    st.markdown("Generate precise Suno prompts from any audio reference.")
    
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Reference Track", type=["mp3", "wav", "m4a"])
    if uploaded_file:
        st.audio(uploaded_file, format='audio/mp3')

    st.markdown("---")
    st.subheader("Lyric Fit Analysis")
    user_lyrics = st.text_area("Paste Lyrics (Optional)", height=200, placeholder="[Verse 1]\nType your lyrics here to check if they fit the tempo...")

# --- BACKEND LOGIC ---
def analyze_track(file_data):
    if not api_key: return None
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    sys_prompt = """
    You are an expert audio engineer and prompt specialist for generative music AI (Suno/Udio).
    Analyze the uploaded audio to create a perfect recreation prompt.
    
    INSTRUCTIONS:
    1. Analyze the Genre, BPM, and Instruments.
    2. Analyze 'Vocal Articulation': 
       - Rate from 1 (Heavily processed, slur, growl, or atmospheric) to 10 (Crystal clear, operatic, or speech-like).
       - If vocals are indistinct, use tags like "hazy", "ethereal", "distorted", or "slurred".
    
    Output JSON only:
    {
        "genre_specific": "Precise Sub-genre",
        "bpm": "Numeric BPM",
        "articulation_score": "Rating 1-10",
        "instruments": "List of key instruments",
        "suno_tags": "Optimized comma-separated tags",
        "vibe_description": "Short 1-sentence description of the mood"
    }
    """
    
    with open("temp.mp3", "wb") as f:
        f.write(file_data.getbuffer())
    
    myfile = genai.upload_file("temp.mp3")
    result = model.generate_content([sys_prompt, myfile])
    return result.text

# --- UI LOGIC ---
col1, col2 = st.columns([2, 1])

if uploaded_file and st.sidebar.button("Analyze Audio"):
    try:
        with st.spinner("Analyzing audio structure..."):
            raw_text = analyze_track(uploaded_file)
            clean_json = raw_text.replace("```json", "").replace("```", "")
            data = json.loads(clean_json)

            # Robust Number Extraction
            bpm_val = extract_number(data['bpm'])
            art_val = extract_number(data['articulation_score'])

        with col1:
            st.markdown("### 🎛️ Generated Prompt")
            st.code(data['suno_tags'], language="markdown")
            
            # Metrics
            c1, c2, c3 = st.columns(3)
            with c1: 
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{bpm_val}</div><div class='metric-lbl'>BPM</div></div>", unsafe_allow_html=True)
            with c2: 
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{art_val}/10</div><div class='metric-lbl'>Articulation</div></div>", unsafe_allow_html=True)
            with c3: 
                st.markdown(f"<div class='metric-box'><div class='metric-val'>{data['genre_specific']}</div><div class='metric-lbl'>Genre</div></div>", unsafe_allow_html=True)

            st.caption(f"**Vibe:** {data['vibe_description']}")

        with col2:
            st.markdown("### 🔮 Compatibility")
            
            if user_lyrics:
                syllables = sum(1 for char in user_lyrics if char.lower() in 'aeiou')
                safe_bpm = bpm_val if bpm_val > 0 else 120
                density_score = syllables / (safe_bpm * 0.5)
                
                st.markdown(f"**Lyric Density Score:** {round(density_score, 2)}")
                
                # UNIVERSAL LOGIC (Works for Metal, Rap, Pop, etc.)
                if art_val < 4:
                    # Low Articulation (Shoegaze, Mumble Rap, Death Metal)
                    if density_score > 10:
                        st.warning("⚠️ High Risk: Fast lyrics with low-articulation vocals often result in muddy/unintelligible audio.")
                        st.progress(20)
                    else:
                        st.success("✅ Good Fit: The lyrics are spaced well for this atmospheric/stylized vocal style.")
                        st.progress(90)
                
                elif art_val > 7:
                    # High Articulation (Pop, Broadway, Country)
                    if density_score > 12:
                         st.warning("⚠️ Pacing Alert: These lyrics are very dense. Ensure the flow is intended to be fast.")
                         st.progress(50)
                    else:
                        st.success("✅ Clean Match: Vocal clarity is high and lyrics fit the tempo.")
                        st.progress(100)
                else:
                    st.info("ℹ️ Balanced: Standard vocal presence detected.")
                    st.progress(70)
            else:
                st.info("Paste your lyrics in the sidebar to see if they fit this style.")

    except Exception as e:
        st.error(f"Analysis Error: {e}")
        st.caption("Tip: Ensure your API key is correct and the audio file is valid.")

elif not uploaded_file:
    with col1:
        st.info("👋 Welcome. Upload a reference track to generate a style profile.")