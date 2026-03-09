import os, openai, io
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT_API_KEY', '')
OPENAI_API = os.getenv('OPENAI_API', '')


bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)
openai.api_key = OPENAI_API

user_state = {}

def carregar_prompt(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()


def openai_agent(mensagem):
    system_prompt = carregar_prompt('prompts/commitai.md')

    resposta = openai.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[
            {'role': 'system',
            'content': system_prompt},
            {'role': 'user', 'content': mensagem}
        ]
    )
    return resposta.choices[0].message.content


@bot.message_handler(content_types=['voice', 'audio'])
def receber_audio(msg):
    # só aceita áudio quando o usuário está aguardando descrição
    if user_state.get(msg.from_user.id) != 'aguardando_descricao':
        bot.send_message(msg.chat.id, '⚠️ Clique no botão *Gerar commit* antes de enviar o áudio com as informações.', parse_mode='Markdown')
        responder(msg)
        return

    # pega o file_id correto
    if msg.voice:
        file_id = msg.voice.file_id
        nome_arquivo = 'audio.ogg'
    else:
        file_id = msg.audio.file_id
        nome_arquivo = msg.audio.file_name or 'audio.mp3'

    # baixa o arquivo do Telegram
    file_info = bot.get_file(file_id)
    audio_bytes = bot.download_file(file_info.file_path)

    # cria arquivo em memória
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = nome_arquivo  # necessário para a API reconhecer o tipo

    # transcreve com a OpenAI
    transcricao = openai.audio.transcriptions.create(
        model='gpt-4o-mini-transcribe',
        file=audio_file,
    )

    texto_usuario = transcricao.text  # texto transcrito

    # segue o fluxo normal
    texto_commit = openai_agent(texto_usuario)
    bot.send_message(msg.chat.id, texto_commit, parse_mode='Markdown')
    user_state.pop(msg.from_user.id, None)
    responder(msg)


@bot.callback_query_handler(func=lambda c: c.data == 'commit')
def cb_commit(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, '💬 Envie um *texto* ou *áudio* descrevendo as alterações realizadas no projeto.', parse_mode='Markdown')
    user_state[call.from_user.id] = 'aguardando_descricao'


@bot.message_handler(func=lambda m: user_state.get(m.from_user.id) == 'aguardando_descricao')
def receber_descricao(msg):
    texto_commit = openai_agent(msg.text)
    bot.send_message(msg.chat.id, texto_commit, parse_mode='Markdown')
    user_state.pop(msg.from_user.id, None)
    responder(msg)


@bot.callback_query_handler(func=lambda c: c.data == 'sobre')
def sobre(call):
    bot.answer_callback_query(call.id)
    texto_sobre = '''
*Sobre o Desenvolvedor:*
- *Nome:* David Alves
- *Website:* https://davidalves.dev/
- *LinkedIn:* https://www.linkedin.com/in/davidalves-dev/
'''
    bot.send_message(call.message.chat.id, texto_sobre, parse_mode='Markdown')


def verificar(msg):
    return True


@bot.message_handler(func=verificar)
def responder(msg):
    msg_inicial = '''
Escolha uma **opção** abaixo para continuar:
'''
    teclado = types.InlineKeyboardMarkup()
    teclado.add(
        types.InlineKeyboardButton('⚡ Gerar commit', callback_data='commit'),
        types.InlineKeyboardButton('🧑🏻‍💻 Sobre', callback_data='sobre'),
    )
    bot.send_message(msg.chat.id, msg_inicial, reply_markup=teclado, parse_mode='Markdown')


bot.infinity_polling()