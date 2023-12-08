import os
from aiogram import Bot, types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
import texts
import recognize


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(texts.START)


@router.message(F.voice)
async def message_handler(msg: Message, bot: Bot):
    ogg_audio = f"data/voices/{msg.voice.file_id}.ogg"
    
    await bot.download(
        msg.voice,
        destination=ogg_audio
    )
    wav_audio = recognize.convert_ogg_to_wav(ogg_audio)

    answer = recognize.recognize_audio(wav_audio)
    os.remove(ogg_audio)
    os.remove(wav_audio)

    await msg.reply(answer)


    
@router.message(F.video_note)
async def message_handler(msg: Message, bot: Bot):
    mp4_video = f"data/videos/{msg.video_note.file_id}.mp4"

    await bot.download(
        msg.video_note,
        destination=mp4_video
    )
    wav_audio = recognize.convert_mp4_to_wav(mp4_video)

    answer = recognize.recognize_audio(wav_audio)
    os.remove(mp4_video)
    os.remove(wav_audio)

    await msg.reply(answer)