import json
import time
import requests
import config
from TG_bot import bot, moderator
from database import dbase
from logger_config import logger
import threading
import flask
from flask import redirect, request
app = flask.Flask(__name__, static_url_path='/static')
app.config['JSON_AS_ASCII'] = False


def check_with_timestamp(id_record, time_sleeping=config.time_sleeping):
    time.sleep(time_sleeping)
    record = dbase.get_record(id_record=id_record)
    if record:
        link = record.get('link')
        id_record = record.get('id_record')
        try:
            is_join = moderator.check_link(link)
        except:
            is_join = False
        record_time = dbase.set_new_join(is_join=is_join, id_record=id_record)
        params = record.get('params')
        params = json.loads(params)
        params['time'] = record_time
        logger.info(f"Записав дані, is_join = {is_join}")
        requests.get(f"{config.webhook_ip}", params=params)



@app.route('/', methods=['GET', 'POST'])
def base():
    params = dict(request.args)
    new_params = {
    }
    for param in config.params:
        new_params[param] = params.get(param)
    new_params = json.dumps(new_params)
    invite_link = moderator.create_invite_link()
    record = dbase.save_record(invite_link=invite_link, params=new_params, chat_id=moderator.chat_id)
    id_record = record.get('id_record')
    threading.Thread(target=check_with_timestamp, args=[id_record,]).start()
    return redirect(invite_link)


def run_bot():
    while True:
        try:
            logger.info(f"Starting bot {bot.get_my_name().name}")
            try:
                bot.delete_webhook()
            except:
                pass
            bot.polling(True)
        except Exception as e:
            logger.error(f"!!! Error bot: {e}")


if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    logger.info(f"Starting web admin")
    app.run(debug=False,
            host='0.0.0.0',
            port=5000)
