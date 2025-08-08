// agno.js
const { OpenAI } = require('openai');
const { getCredential } = require('./credentials.js');

const openai = new OpenAI({
  apiKey: getCredential('openai', 'apiKey')
});

async function gerarRespostaAgno(mensagem) {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'Você é um assistente útil.' },
        { role: 'user', content: mensagem }
      ],
    });
    return response.choices[0].message.content;
  } catch (error) {
    console.error('Erro ao gerar resposta no Agno:', error);
    return 'Erro ao processar a resposta.';
  }
}

module.exports = { gerarRespostaAgno };
