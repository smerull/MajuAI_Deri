# AI Chatbot (Express + OpenAI)

Simple chatbot scaffold using Node.js, Express, and OpenAI Chat Completions.

Features:
- Small web UI served from `public/`
- `/api/chat` endpoint that proxies to OpenAI
- Client maintains conversation history and system prompt
- Controls for model, temperature, and max tokens

Setup

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Install dependencies: `npm install`.
3. Start server: `npm start` (or `npm run dev` with nodemon).
4. Open http://localhost:3000 in your browser.

Notes
- This project uses the OpenAI REST API; make sure your key is valid and has access to the selected model.
- The backend proxies requests so your API key stays server-side.

Streamlit alternative UI

This project includes a Streamlit-based UI that you can run instead of the web frontend.

1. Create a Python virtual environment and activate it (example on Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Ensure `OPENAI_API_KEY` is set in environment or paste it into the sidebar field when running the app.

4. Run Streamlit:

```powershell
streamlit run streamlit_app.py
```

The Streamlit UI provides controls for model, temperature, max tokens, and system prompt.

Next steps / improvements
- Add message streaming for real-time tokens
- Add authentication and rate-limits
- Add server-side validation and logging
