const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const PORT = process.env.PORT || 3000;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (!OPENAI_API_KEY) {
  console.warn('Warning: OPENAI_API_KEY is not set. Chat endpoint will fail without it.');
}

app.post('/api/chat', async (req, res) => {
  const { messages, temperature = 0.7, max_tokens = 500, model = 'gpt-4o-mini' } = req.body;

  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json({ error: 'messages (array) is required in the request body' });
  }

  try {
    const resp = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model,
        messages,
        temperature,
        max_tokens
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return res.json(resp.data);
  } catch (err) {
    console.error('OpenAI request failed:', err.response ? err.response.data : err.message);
    const status = err.response ? err.response.status : 500;
    const data = err.response ? err.response.data : { error: err.message };
    return res.status(status).json(data);
  }
});

app.listen(PORT, () => {
  console.log(`AI Chatbot server listening on http://localhost:${PORT}`);
});
