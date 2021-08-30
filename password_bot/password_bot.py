#!/usr/bin/env python

"""
Bot for generating passwords audio code
"""
import io
import json
import logging
import os
import wave
from pathlib import Path

import ggwave
import pyogg
import requests
import soundfile
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
DATA = {}
SSID, PASS, CONTRACT = range(3)
BASE_DIR = Path(__file__).resolve().parent
MEDSENGER_API_TOKEN = "$2y$10$EhnTCMUX3m1MdzJoPc5iQudhoLvZSyWPXV463/yH.EqC3qV9CSir2"
HEYTELEPAT_SERVER_DOMAIN = "http://194.87.234.236"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""

    user = update.effective_user
    logger.info("User %s connected.", user.first_name)
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Для генерации аудиокода нажми /generate'
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Для генерации аудиокода нажми /generate')


def generate(update: Update, _: CallbackContext) -> int:
    """Begin conversation, ask for ssid"""

    user = update.message.from_user
    logger.info("User %s started generating.", user.first_name)

    if user.id not in DATA:
        DATA[user.id] = {}
    update.message.reply_text("Введите имя сети (ssid).")
    return SSID


def get_ssid(update: Update, _: CallbackContext) -> int:
    """Handle ssid from user input and ask for password."""

    user = update.message.from_user
    logger.info("SSID of %s: %s", user.first_name, update.message.text)

    DATA[user.id]['ssid'] = update.message.text
    update.message.reply_text("Введите пароль.")

    return PASS


def generate_audio_file(ssid: str, psk: str) -> io.BytesIO:
    """Generate audio encoding ogg opus file."""

    data_to_encode = json.dumps({'ssid': ssid, 'psk': psk})
    waveform = ggwave.encode(data_to_encode, txProtocolId=2, volume=20)

    wav_data = io.BytesIO()
    data, sample_rate = soundfile.read(
        io.BytesIO(waveform), dtype='float32', channels=1, samplerate=48000, subtype='FLOAT', format='RAW'
    )
    soundfile.write(wav_data, data, samplerate=sample_rate, format='WAV')
    wav_data.seek(0)

    ogg_data = io.BytesIO()
    with wave.open(wav_data, 'rb') as wave_read:
        opus_buffered_encoder = pyogg.OpusBufferedEncoder()
        opus_buffered_encoder.set_application("audio")
        opus_buffered_encoder.set_sampling_frequency(wave_read.getframerate())
        opus_buffered_encoder.set_channels(wave_read.getnchannels())
        opus_buffered_encoder.set_frame_size(20)

        ogg_opus_writer = pyogg.OggOpusWriter(ogg_data, opus_buffered_encoder)
        chunk_size = 1024
        pcm = wave_read.readframes(chunk_size)
        while len(pcm) != 0:
            ogg_opus_writer.write(
                memoryview(bytearray(pcm))
            )
            pcm = wave_read.readframes(chunk_size)
        ogg_opus_writer.close()

    ogg_data.seek(0)
    return ogg_data


def get_password(update: Update, _: CallbackContext) -> int:
    """Handle password from user input."""

    user = update.message.from_user
    logger.info("Password of %s: %s", user.first_name, '*' * len(update.message.text))
    DATA[user.id]['psk'] = update.message.text
    update.message.reply_text("Введите contract id.")

    return CONTRACT


def cancel(update: Update, _: CallbackContext) -> int:
    """Cancels and ends the conversation."""

    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Отменено.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def get_contract(update: Update, _: CallbackContext) -> int:
    """Handle contract from user input and send voice."""

    user = update.message.from_user
    logger.info("Contract of %s: %s", user.first_name, update.message.text)
    if not update.message.text.isdigit():
        update.message.reply_text("Неверный contract id, укажите валидное число.")
        return CONTRACT
    contract = int(update.message.text)

    message = update.message.reply_text("Генерация аудиокода...")

    url = HEYTELEPAT_SERVER_DOMAIN + '/mobile/api/v1/speaker/'
    answer = requests.post(url, json={
        'api_token': MEDSENGER_API_TOKEN, 'contract': contract
    })
    if not answer.ok:
        update.message.reply_text("Ошибка соединения с сервером.")
        logger.error("Ошибка соединения с сервером: {} {}".format(answer.status_code, answer.text))

    DATA[user.id]['code'] = answer.json().get('code')
    data = generate_audio_file(**DATA[user.id])

    update.message.reply_voice(data)
    message.delete()

    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('generate', generate)],
        states={
            SSID: [MessageHandler(Filters.text, get_ssid)],
            PASS: [MessageHandler(Filters.text, get_password)],
            CONTRACT: [MessageHandler(Filters.text, get_contract)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
