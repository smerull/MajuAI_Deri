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
st.set_page_config(page_title='AI Chatbot (Streamlit Gemini Multimodal)', layout='wide')
st.title('🤖 Teman Belajar AI Cerdas — Untuk Anak SD (Google Gemini)')

# --- Helper Functions ---

def get_base64_image(image_file) -> str:
    """Mengubah file gambar yang diunggah Streamlit menjadi string Base64."""
    try:
        bytes_data = image_file.getvalue()
        return base64.b64encode(bytes_data).decode('utf-8')
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return ""

def process_uploaded_files(uploaded_file):
    """
    Memproses file yang diunggah dan menyiapkan konten dalam format 'part' 
    yang diperlukan oleh Gemini API untuk gambar (inlineData).
    """
    if uploaded_file is None:
        return None, None

    file_type = uploaded_file.type
    file_name = uploaded_file.name

    if 'image' in file_type:
        st.info(f"Gambar diunggah: {file_name}")
        base64_img = get_base64_image(uploaded_file)
        
        # Struktur konten Gemini untuk multimodal
        image_content = {
            "inlineData": {
                "data": base64_img,
                "mimeType": file_type
            }
        }
        return image_content, file_name

    elif 'pdf' in file_type:
        # --- PDF PROCESSING (Placeholder) ---
        st.warning(f"PDF diunggah: {file_name}. Fitur ini belum aktif.")
        return None, file_name 
        
    return None, file_name 

def format_messages_for_gemini(messages: List[Dict]) -> List[Dict]:
    """
    Mengubah format riwayat pesan Streamlit ke format 'contents' Gemini.
    """
    gemini_contents = []
    
    for msg in messages:
        role = msg.get('role')
        content = msg.get('content')
        
        # Lewati system prompt
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
    """Mengirim permintaan ke Gemini API."""
    
    url = GEMINI_API_URL.format(model=model)
    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}
    
    gemini_contents = format_messages_for_gemini(messages)
    
    # Konfigurasi parameter generasi (menggunakan kunci 'generationConfig')
    generation_config = {
        'temperature': temperature,
        'maxOutputTokens': max_tokens,
    }

    # Payload untuk Gemini API. 
    payload = {
        'contents': gemini_contents,
        'generationConfig': generation_config, 
    }
    
    # Tambahkan 'systemInstruction' hanya jika nilainya tidak kosong. (FIXED)
    if system_prompt and system_prompt.strip():
        payload['systemInstruction'] = system_prompt.strip()
    
    r = requests.post(url, json=payload, headers=headers, params=params, timeout=60) 
    r.raise_for_status()
    return r.json()

# --- Streamlit UI: Sidebar Settings ---

with st.sidebar:
    st.header('Pengaturan Rahasia ⚙️')
    st.markdown("Ini adalah tempat untuk mengatur AI-nya!")
    
    # Input kunci API Gemini
    key_input = st.text_input('Kunci API Gemini (AIzaSy...)', type="password", value='' if GEMINI_API_KEY is None else '')
    
    # Seleksi Model Gemini. FLASH adalah yang Gratis dan Cepat.
    model = st.selectbox('Model AI', ['gemini-2.5-flash', 'gemini-2.5-pro'], index=0)
    
    # Pengaturan untuk tingkat kreativitas dan panjang jawaban
    temperature = st.slider('Tingkat Kreativitas (Suhu)', 0.0, 1.0, 0.8, 0.05)
    max_tokens = st.number_input('Panjang Jawaban Maksimal', min_value=50, max_value=4000, value=750)
    
    # System prompt baru yang berfokus untuk Anak SD
    default_system_prompt = 'Kamu adalah guru atau teman virtual yang sangat ramah dan ceria. Jawablah semua pertanyaan dengan bahasa yang sederhana, mudah dipahami, gunakan analogi yang menyenangkan, dan sertakan emoji yang sesuai. Berikan jawaban yang mendidik, singkat, dan menghibur, seolah-olah kamu sedang berbicara dengan anak sekolah dasar.'
    system_prompt = st.text_area('Peran AI (System prompt)', value=default_system_prompt, height=150)
    
    st.markdown("---")
    clear_history = st.button('Bersihkan Obrolan 🗑️')

api_key = key_input.strip() or GEMINI_API_KEY
if not api_key:
    st.sidebar.warning('🚨 Kunci API Gemini belum dimasukkan. Masukkan kunci Anda dari Google AI Studio.')

# --- Session State Initialization ---

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': system_prompt}]

# Handle History Clearing
if clear_history:
    st.session_state.messages = [{'role': 'system', 'content': system_prompt}]
    st.experimental_rerun()

# --- Conversation Display ---
st.subheader('Ayo Bertanya dan Belajar! 🚀')

# Menampilkan pesan
for msg in st.session_state.messages:
    role = msg.get('role')
    content = msg.get('content')
    
    if isinstance(content, list):
        text_content = next((item['text'] for item in content if item.get('type') == 'text'), '[Pesan Tanpa Teks]')
        image_content = [
            {"image_url": {"url": f"data:{item['inlineData']['mimeType']};base64,{item['inlineData']['data']}"}} 
            for item in content if item.get('inlineData')
        ]
    else:
        text_content = content
        image_content = []

    if role == 'user':
        st.chat_message("user").markdown(f"**Saya:** {text_content}")
        for img in image_content:
            st.chat_message("user").image(img['image_url']['url'], caption='Gambar yang kamu tunjukkan', width=200)
    elif role == 'assistant':
        st.chat_message("assistant").markdown(f"**Teman AI:** {text_content}")
    elif role == 'system':
        # System prompt tidak perlu ditampilkan di chat utama
        pass 

st.divider()

# --- Input and File Upload ---

uploaded_file = st.file_uploader(
    "Tunjukkan Gambar (misalnya PR, gambar hewan, dll.) 🖼️", 
    type=['png', 'jpg', 'jpeg'], 
    key='file_uploader'
)

user_input = st.text_area('Tuliskan pertanyaanmu di sini...', key='input_text')

if st.button('Kirim Pertanyaan! 🌟'):
    if not user_input.strip() and uploaded_file is None:
        st.warning('Ayo, tuliskan sesuatu atau tunjukkan gambarmu!')
    else:
        # 1. Proses Unggahan File 
        image_content, file_name = process_uploaded_files(uploaded_file)
        
        # 2. Bangun Konten Pesan 
        new_message_parts = []
        
        if image_content:
            new_message_parts.append(image_content)

        if user_input.strip():
            new_message_parts.append({"text": user_input, "type": "text"}) 
        elif file_name and not image_content:
            new_message_parts.append({"text": f"Tolong lihat file ini: {file_name}. Jawab pertanyaan di dalamnya ya.", "type": "text"})
            
        # 3. Tambahkan Pesan Pengguna ke Riwayat
        if new_message_parts:
            st.session_state.messages.append({'role': 'user', 'content': new_message_parts})
            
            # 4. Panggil API
            try:
                if not api_key:
                    st.error('🚨 Kunci API belum dimasukkan!')
                else:
                    with st.spinner('Teman AI sedang berpikir... 🤔'):
                        
                        resp = chat_request(
                            st.session_state.messages, 
                            model, 
                            temperature, 
                            max_tokens, 
                            api_key, 
                            system_prompt
                        )
                    
                    # Ekstrak jawaban dari format respons Gemini
                    try:
                        ai_msg = resp['candidates'][0]['content']['parts'][0]['text']
                    except (IndexError, KeyError, TypeError):
                        # Handling Safety Filter atau Response Error
                        safety_reason = resp.get('promptFeedback', {}).get('blockReason', 'Unknown Error')
                        st.error(f"❌ Ups! Teman AI tidak bisa menjawab itu ({safety_reason}). Coba pertanyaan yang lain, ya!")
                        ai_msg = str(resp) 
                        
                    st.session_state.messages.append({'role': 'assistant', 'content': ai_msg})
                    
                    # Reset input dan reran
                    st.session_state.file_uploader = None
                    st.session_state.input_text = ""
                    st.experimental_rerun()
                    
            except requests.HTTPError as e:
                st.error(f'❌ Terjadi masalah dengan koneksi AI: {e} - Pastikan Kunci API Anda benar dan aktif.')
            except Exception as e:
                st.error(f'❌ Terjadi kesalahan: {e}')