import os
from aiogram import Bot, types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from filters.chat_type import ChatTypeFilter
import texts
import recognize
import logging
import db.db as db


router = Router()


@router.message(Command("start"), ChatTypeFilter(chat_type=["private"]))
async def start_handler(msg: Message):
    logging.info(f"Run start handler.")
    db.reg_user(msg.from_user)
    await msg.answer(texts.START)


@router.message(F.voice, ChatTypeFilter(chat_type=["group", "supergroup"]))
async def voice(msg: Message, bot: Bot):
    logging.info(f"Run voice handler.")
    ogg_audio = f"storage/voices/{msg.voice.file_id}.ogg"
    
    try:
        logging.info(f"Ogg voice filename: {ogg_audio}.")
        await bot.download(
            msg.voice,
            destination=ogg_audio
        )
        logging.info(f"Ogg voice download successful.")
    except:
        logging.error("Error downloading voice.", exc_info=True)
        return

    try:
        wav_audio = recognize.convert_ogg_to_wav(ogg_audio)
        logging.info(f"Converting ogg to wav successful (filename: {wav_audio}).")
    except:
        logging.error("Error converting ogg to wav file.", exc_info=True)
        return

    try:
        logging.info(f"Start recognaze.")
        answer = recognize.recognize_audio(wav_audio)
        logging.info(f"Successful recognaze.")
        db.new_speech_group(group=msg.chat, msg_type="voice", duration=msg.voice.duration, words=len(answer.split(" ")))
    except:
        logging.error("Error recognizing speech.", exc_info=True)
        return

    os.remove(ogg_audio)
    os.remove(wav_audio)

    if len(answer) != 0:
        await msg.reply(answer)


    
@router.message(F.video_note, ChatTypeFilter(chat_type=["group", "supergroup"]))
async def video_note(msg: Message, bot: Bot):
    logging.info(f"Run video_note handler.")
    mp4_video = f"storage/videos/{msg.video_note.file_id}.mp4"

    try:
        logging.info(f"Mp4 video filename: {mp4_video}.")
        await bot.download(
            msg.video_note,
            destination=mp4_video
        )
        logging.info(f"Mp4 video download successful.")
    except:
        logging.error("Error downloading video.", exc_info=True)
        return

    try:
        wav_audio = recognize.convert_mp4_to_wav(mp4_video)
        logging.info(f"Converting mp4 to wav successful (filename: {wav_audio}).")
    except:
        logging.error("Error converting mp4 to wav file.", exc_info=True)
        return

    try:
        logging.info(f"Start recognaze.")
        answer = recognize.recognize_audio(wav_audio)
        logging.info(f"Successful recognaze.")
        db.new_speech_group(group=msg.chat, msg_type="video", duration=msg.video_note.duration, words=len(answer.split(" ")))
    except:
        logging.error("Error recognizing speech.", exc_info=True)
        return

    os.remove(mp4_video)
    os.remove(wav_audio)

    if len(answer) != 0:
        await msg.reply(answer)



# for private



@router.message(F.voice, ChatTypeFilter(chat_type=["private"]))
async def voice(msg: Message, bot: Bot):
    logging.info(f"Run voice handler.")
    ogg_audio = f"storage/voices/{msg.voice.file_id}.ogg"
    
    try:
        logging.info(f"Ogg voice filename: {ogg_audio}.")
        await bot.download(
            msg.voice,
            destination=ogg_audio
        )
        logging.info(f"Ogg voice download successful.")
    except:
        await msg.reply("Странно, что-то пошло не так")
        logging.error("Error downloading voice.", exc_info=True)
        return

    try:
        wav_audio = recognize.convert_ogg_to_wav(ogg_audio)
        logging.info(f"Converting ogg to wav successful (filename: {wav_audio}).")
    except:
        await msg.reply("Странно, что-то пошло не так")
        logging.error("Error converting ogg to wav file.", exc_info=True)
        return

    try:
        logging.info(f"Start recognaze.")
        answer = recognize.recognize_audio(wav_audio)
        logging.info(f"Successful recognaze.")
        db.new_speech(user=msg.from_user, msg_type="voice", duration=msg.voice.duration, words=len(answer.split(" ")))
    except:
        await msg.reply("Странно, что-то пошло не так")
        logging.error("Error recognizing speech.", exc_info=True)
        return

    os.remove(ogg_audio)
    os.remove(wav_audio)

    if len(answer) == 0:
        answer = "🤷‍♂️"
    await msg.reply(answer)


    
@router.message(F.video_note, ChatTypeFilter(chat_type=["private"]))
async def video_note(msg: Message, bot: Bot):
    logging.info(f"Run video_note handler.")
    mp4_video = f"storage/videos/{msg.video_note.file_id}.mp4"

    try:
        logging.info(f"Mp4 video filename: {mp4_video}.")
        await bot.download(
            msg.video_note,
            destination=mp4_video
        )
        logging.info(f"Mp4 video download successful.")
    except:
        await msg.reply("Странно, что-то пошло не так")
        logging.error("Error downloading video.", exc_info=True)
        return

    try:
        wav_audio = recognize.convert_mp4_to_wav(mp4_video)
        logging.info(f"Converting mp4 to wav successful (filename: {wav_audio}).")
    except:
        await msg.reply("Странно, что-то пошло не так")
        logging.error("Error converting mp4 to wav file.", exc_info=True)
        return

    try:
        logging.info(f"Start recognaze.")
        answer = recognize.recognize_audio(wav_audio)
        logging.info(f"Successful recognaze.")
        db.new_speech(user=msg.from_user, msg_type="video", duration=msg.video_note.duration, words=len(answer.split(" ")))
    except:
        await msg.reply("Странно, что-то пошло не так")
        logging.error("Error recognizing speech.", exc_info=True)
        return

    os.remove(mp4_video)
    os.remove(wav_audio)

    if len(answer) == 0:
        answer = "🤷‍♂️"
    await msg.reply(answer)




@router.message(Command("info"), ChatTypeFilter(chat_type=["private"]))
async def info(msg: Message):
    logging.info(f"Run info handler.")
    if not db.check_admin(msg.from_user.id):
        return
    try:
        info_message = f"Пользователей бота: {len(db.users.getAll())}" + \
                        f"\nГрупп: {len(db.groups.getAll())}" + \
                        f"\nГолосовых: {len(db.messages.getByQuery({'type': 'voice'}))}" + \
                        f"\nКружочков: {len(db.messages.getByQuery({'type': 'video'}))}" + \
                        f"\nДлина всех гс: {sum([int(dur['duration']) for dur in db.messages.getByQuery({'type': 'voice'})])}" + \
                        f"\nДлина всех кружочков: {sum([int(dur['duration']) for dur in db.messages.getByQuery({'type': 'video'})])}" + \
                        f"\nРасшифровано слов: {sum([dur['words'] for dur in db.messages.getAll()])}" + \
                        f"\nДата последнего аудио: {db.messages.getAll()[-1]['time']}"
    except:
        logging.error("Error generate info msg.", exc_info=True)

    logging.info(f"Send info.")
    await msg.answer(info_message)