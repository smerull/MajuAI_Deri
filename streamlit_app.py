import os
import streamlit as st
import requests
import base64
from typing import List, Dict, Union

# Mengambil kunci API dari environment variable (opsional)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# URL Endpoint Google Gemini API
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# --- Configuration & Setup ---
st.set_page_config(
    page_title='🌈 Teman Belajar AI',
    layout='centered',
    initial_sidebar_state='expanded'
)

# Sembunyikan header Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    button[kind="header"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Custom CSS untuk tampilan anak-anak yang simple
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
        border-radius: 30px !important;
        padding: 2rem !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12) !important;
        max-width: 900px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffe4e1 0%, #ffd1dc 100%) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #ffe4e1 0%, #ffd1dc 100%) !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #c0392b !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }
    
    section[data-testid="stSidebar"] label {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(90deg, #ff6b6b, #feca57) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 1rem 2rem !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5) !important;
    }
    
    /* Input */
    .stTextInput input {
        border-radius: 20px !important;
        border: 3px solid #ff6b6b !important;
        font-size: 1.2rem !important;
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        padding: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stTextInput input::placeholder {
        color: #666666 !important;
        font-weight: 500 !important;
    }
    
    .stTextInput label {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* Chat */
    .stChatMessage {
        border-radius: 25px !important;
        padding: 1.2rem !important;
        margin: 0.8rem 0 !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
    }
    
    .stChatMessage p {
        color: #1a1a1a !important;
        font-size: 1.15rem !important;
        line-height: 1.6 !important;
        font-weight: 600 !important;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background-color: #e3f2fd !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #fff3e0 !important;
    }
    
    /* File uploader */
    section[data-testid="stFileUploadDropzone"] {
        background: linear-gradient(135deg, #fff9e6 0%, #ffe4e1 100%) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        border: 3px dashed #feca57 !important;
    }
    
    .uploadedFileName {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }
    
    .stFileUploader label {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    .stFileUploader > label > div:first-child {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stFileUploader"] label {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stFileUploader"] > label {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    div[data-testid="stFileUploader"] p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Alerts */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 15px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }
    
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 2px solid #28a745 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border: 2px solid #ffc107 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 2px solid #dc3545 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border: 2px solid #17a2b8 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb);
        margin: 1.5rem 0;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title sederhana
st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(90deg, #ff6b6b, #feca57); border-radius: 25px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🤖 Teman Belajar AI</h1>
        <p style='color: white; font-size: 1.2rem; margin: 0.5rem 0 0 0;'>Ayo Bertanya Apa Saja! 🌟</p>
    </div>
""", unsafe_allow_html=True)

# --- Helper Functions ---

def get_base64_image(image_file) -> str:
    try:
        bytes_data = image_file.getvalue()
        return base64.b64encode(bytes_data).decode('utf-8')
    except Exception as e:
        st.error(f"❌ Ada masalah dengan gambar: {e}")
        return ""

def process_uploaded_files(uploaded_file):
    if uploaded_file is None:
        return None, None

    file_type = uploaded_file.type
    file_name = uploaded_file.name

    if 'image' in file_type:
        st.success(f"✅ Gambar berhasil diupload: {file_name}")
        base64_img = get_base64_image(uploaded_file)
        
        image_content = {
            "inlineData": {
                "data": base64_img,
                "mimeType": file_type
            }
        }
        return image_content, file_name

    elif 'pdf' in file_type:
        st.warning(f"📄 PDF: {file_name}. Fitur sedang dikembangkan! 🛠️")
        return None, file_name 
        
    return None, file_name 

def format_messages_for_gemini(messages: List[Dict]) -> List[Dict]:
    gemini_contents = []
    
    for msg in messages:
        role = msg.get('role')
        content = msg.get('content')
        
        if role == 'system':
            continue
            
        gemini_role = 'user' if role == 'user' else 'model'
        
        parts = []
        if isinstance(content, list):
            for part in content:
                if part.get('type') == 'text':
                    parts.append({"text": part['text']})
                elif part.get('inlineData'): 
                    parts.append(part)
        elif isinstance(content, str):
            parts.append({"text": content})
        
        if parts:
            gemini_contents.append({"role": gemini_role, "parts": parts})

    return gemini_contents

def chat_request(messages: List[Dict], model: str, temperature: float, max_tokens: int, api_key: str, system_prompt: str):
    url = GEMINI_API_URL.format(model=model)
    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}
    
    gemini_contents = format_messages_for_gemini(messages)
    
    generation_config = {
        'temperature': temperature,
        'maxOutputTokens': max_tokens,
    }

    payload = {
        'contents': gemini_contents,
        'generationConfig': generation_config, 
    }
    
    if system_prompt and system_prompt.strip():
        payload['systemInstruction'] = system_prompt.strip()
    
    r = requests.post(url, json=payload, headers=headers, params=params, timeout=60) 
    r.raise_for_status()
    return r.json()

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    
    key_input = st.text_input('🔑 Kunci API Gemini', type="password", value='' if GEMINI_API_KEY is None else '')
    
    with st.expander("🎨 Pengaturan Lanjutan"):
        model = st.selectbox('Model AI', ['gemini-2.5-flash', 'gemini-2.5-pro'], index=0)
        temperature = st.slider('Kreativitas', 0.0, 1.0, 0.8, 0.1)
        max_tokens = st.number_input('Panjang Jawaban', min_value=100, max_value=2000, value=750)
    
    default_system_prompt = 'Kamu adalah guru yang ramah untuk anak SD. Jawab dengan bahasa sederhana, pakai emoji, dan buat jawaban yang menyenangkan!'
    system_prompt = st.text_area('🎭 Peran AI', value=default_system_prompt, height=120)
    
    st.markdown("---")
    
    if st.button('🔄 Mulai Baru', use_container_width=True):
        st.session_state.messages = [{'role': 'system', 'content': system_prompt}]
        st.rerun()

api_key = key_input.strip() or GEMINI_API_KEY
if not api_key:
    st.sidebar.warning('⚠️ Masukkan Kunci API ya!')

# --- Session State ---
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': system_prompt}]

# --- Chat Display ---
for msg in st.session_state.messages:
    role = msg.get('role')
    content = msg.get('content')
    
    if isinstance(content, list):
        text_content = next((item['text'] for item in content if item.get('type') == 'text'), '')
        image_content = [
            {"image_url": {"url": f"data:{item['inlineData']['mimeType']};base64,{item['inlineData']['data']}"}} 
            for item in content if item.get('inlineData')
        ]
    else:
        text_content = content
        image_content = []

    if role == 'user':
        with st.chat_message("user", avatar="👦"):
            st.markdown(text_content)
            for img in image_content:
                st.image(img['image_url']['url'], width=300)
    elif role == 'assistant':
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(text_content)

st.markdown("---")

# --- Input Area ---
uploaded_file = st.file_uploader(
    "📸 Upload Gambar (Opsional)", 
    type=['png', 'jpg', 'jpeg'], 
    key='file_uploader'
)

user_input = st.text_input(
    'Tulis pertanyaanmu di sini...', 
    key='input_text',
    placeholder="Contoh: Jelaskan cara kerja pelangi 🌈"
)

if st.button('🚀 Kirim!', use_container_width=True):
    if not user_input.strip() and uploaded_file is None:
        st.warning('💭 Tulis pertanyaan atau upload gambar dulu ya!')
    else:
        image_content, file_name = process_uploaded_files(uploaded_file)
        
        new_message_parts = []
        
        if image_content:
            new_message_parts.append(image_content)

        if user_input.strip():
            new_message_parts.append({"text": user_input, "type": "text"}) 
        elif file_name and not image_content:
            new_message_parts.append({"text": f"Lihat file: {file_name}", "type": "text"})
            
        if new_message_parts:
            st.session_state.messages.append({'role': 'user', 'content': new_message_parts})
            
            try:
                if not api_key:
                    st.error('🚨 Kunci API belum ada!')
                else:
                    with st.spinner('🤔 AI sedang berpikir...'):
                        resp = chat_request(
                            st.session_state.messages, 
                            model, 
                            temperature, 
                            max_tokens, 
                            api_key, 
                            system_prompt
                        )
                    
                    try:
                        ai_msg = resp['candidates'][0]['content']['parts'][0]['text']
                        st.balloons()
                    except (IndexError, KeyError, TypeError):
                        safety_reason = resp.get('promptFeedback', {}).get('blockReason', 'Error')
                        st.error(f"❌ AI tidak bisa jawab ({safety_reason}). Coba pertanyaan lain!")
                        ai_msg = "Maaf, coba pertanyaan lain ya! 😊"
                        
                    st.session_state.messages.append({'role': 'assistant', 'content': ai_msg})
                    st.rerun()
                    
            except requests.HTTPError as e:
                st.error(f'❌ Koneksi bermasalah: {e}')
            except Exception as e:
                st.error(f'❌ Error: {e}')

# Footer simple
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1rem; background: #fff9e6; border-radius: 20px;'>
        <p style='color: #e74c3c; font-size: 1.2rem; font-weight: 700; margin: 0;'>
            🌟 Terus belajar! 📚✨
        </p>
    </div>
""", unsafe_allow_html=True)
