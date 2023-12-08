import logging
from pysondb import getDb
import utils
from datetime import datetime

users = getDb("db/users.json")
groups = getDb("db/groups.json")
messages = getDb("db/messages.json")
admins = getDb("db/admins.json")
statistics = getDb("db/statistics.json")

def check_db():
    if len(users.getAll()) == 0:
        users.add({"tg_id": "", "tg_username": "", "messages": []})
    if len(groups.getAll()) == 0:
        groups.add({"chat_id": "", "messages": []})
    if len(messages.getAll()) == 0:
        messages.add({"time": "", "type": "", "duration": "", "words": 0})
    if len(admins.getAll()) == 0:
        admins.add({"tg_id": "1454029826", "tg_username": "ivan_noskovvv"})
    if len(statistics.getAll()) == 0:
        statistics.add({"requests_number": 0})

def delete_all():
    users.deleteAll()
    groups.deleteAll()
    messages.deleteAll()
    admins.deleteAll()
    statistics.deleteAll()

def start(new_user):
    if len(users.getByQuery({"tg_id": new_user.id})) == 0:
        users.add({"tg_id": str(new_user.id), "tg_username": str(new_user.username), "messages": []})
        logging.info(f"Add new user (всего: {len(users.getAll())})")
    else:
        logging.info(f"There is already such a user")

def new_voice(user, msg_type, duration, words):
    bd_users = users.getByQuery({"tg_id": str(user.id)})
    if len(bd_users) == 0:
        start(user)
    bd_user = users.getByQuery({"tg_id": str(user.id)})[0]
    message_id = messages.add({"time": datetime.now().strftime(utils.date_format), "type": msg_type, "duration": duration, "words": words})
    users.updateById(bd_user["id"], {"messages": bd_user["messages"] + [message_id]})