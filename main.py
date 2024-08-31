from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.types import KeyboardButtonCallback
from telethon.tl.types import Message
from datetime import datetime, time as dt_time, timedelta
import random
import asyncio
import time
import json


with open('phone.json') as f:
    phone = json.load(f)[str(random.randint(1, 25))]

api_id = input('api_id: ')
api_hash = input('api_hash: ')
mining = bool(int(input('Do you have mining (0 – no, 1 – yes): ')))
auto_withdrawal = bool(int(input('Auto-withdrawal (0 – no, 1 – yes): ')))

client = TelegramClient(session='session1', api_id=int(api_id), api_hash=api_hash, system_version="4.16.30-vxCUSTOM",
                        device_model=phone, app_version='Telegram Android 10.14.5',
                        system_lang_code='en', lang_code='en')

# Delays for random selection
click_delay = [i / 1000000 for i in range(650000, 1000000)] + [i / 1000000 for i in range(1950000, 2130000)]
check_balance = [i / 1000000 for i in range(1110000, 1500000)]

# ID bot
id_bot_touch = '@gramTouchBot'

# Global variables for process control
new_day = True
login_to_the_game = 0  # number of inputs
now_time = 0  # first click time
max_click = 0  # max number of clicks, depends on the limit and the number of inputs
quantity_click = 0  # number of clicks that were made
max_hours_wait = 16_200  # max waiting time between entries 4.5 hours
# lock = asyncio.Lock()  # global lock object


async def auto_balance_withdrawal(chat_id) -> None:
    last_message = await get_last_message(client, chat_id)
    await asyncio.sleep(random.uniform(1.9, 3.5))
    await click_button(client, chat_id, last_message, 'Биржа')
    await asyncio.sleep(random.uniform(1.9, 3.5))
    last_message = await get_last_message(client, chat_id)
    await click_button(client, chat_id, last_message, 'Продать')
    await asyncio.sleep(random.uniform(5, 12))
    last_message = await get_last_message(client, chat_id)
    balance = last_message.message.split('\n')[7].split()[1]
    balance = balance[:len(balance.split('.')[0]) + 2]
    await client.send_message(chat_id, balance)
    await asyncio.sleep(random.uniform(3, 5))
    last_message = await get_last_message(client, chat_id)
    await click_button(client, chat_id, last_message, 'Обменять')
    await asyncio.sleep(random.uniform(4, 7))
    last_message = await get_last_message(client, chat_id)
    await click_button(client, chat_id, last_message, "◀")
    await asyncio.sleep(random.uniform(6, 14))
    last_message = await get_last_message(client, chat_id)
    await click_button(client, chat_id, last_message, 'Профиль')
    await asyncio.sleep(random.uniform(1.8, 3))
    last_message = await get_last_message(client, chat_id)
    await click_button(client, chat_id, last_message, 'Вывести')
    await asyncio.sleep(random.uniform(5, 9))
    last_message = await get_last_message(client, chat_id)
    balance = last_message.message.split('\n')[4].split()[1]
    balance = balance[:len(balance.split('.')[0]) + 2]
    await client.send_message(chat_id, balance)


async def wait_until_morning() -> None:
    current_time = datetime.now().time()
    if dt_time(2, 0) <= current_time < dt_time(7, 0):
        sleep_until = datetime.combine(datetime.today(), dt_time(7, 0))
        sleep_duration = (sleep_until - datetime.now()).total_seconds() + random.uniform(2700, 18000)
        print(f"The script is on standby until the morning. Waiting time: {sleep_duration / 3600:.2f} hours.")
        await asyncio.sleep(sleep_duration)


async def collections_mining(chat_id: str):
    last_message = await get_last_message(client, chat_id)
    await asyncio.sleep(random.uniform(1.9, 3.3))
    await click_button(client, chat_id, last_message, "Майнинг")
    await asyncio.sleep(random.uniform(1.5, 2.8))
    last_message = await get_last_message(client, chat_id)
    await click_button(client, chat_id, last_message, "Собрать")
    await asyncio.sleep(random.uniform(1.8, 3))
    last_message = await get_last_message(client, chat_id)
    # print(last_message)
    await click_button(client, chat_id, last_message, "◀")
    await asyncio.sleep(random.uniform(1.5, 2.8))

    with open("log_for_mining.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - Function executed for client: {(await client.get_me()).phone} "
                       f"– {(await client.get_me()).username}\n")


async def time_based_task(chat_id: str):
    while True:
        now = datetime.now()
        current_time = now.time()

        # If the current time is between 12:00 am and 2:00 am and the task has not yet completed
        if dt_time(0, 0) <= current_time <= dt_time(2, 0):
            sleep_duration = random.uniform(0, 2 * 3600)  # случайное время между 0 и 2 часами
            await asyncio.sleep(sleep_duration)
            await collections_mining(chat_id)

            if int(str(current_time)[4:5]) % 2 == 0 and auto_withdrawal:
                await auto_balance_withdrawal(chat_id)

            # Set the next execution between 7:00 AM and 8:00 AM
            next_run = datetime.combine(now.date(), dt_time(7, 0))
            sleep_duration = (next_run - now).total_seconds()
            print(f"Script on standby until {next_run}. Waiting time: {sleep_duration / 3600:.2f} hours.")
            await asyncio.sleep(sleep_duration)
            continue

        # If the current time is between 7:00 AM and 8:00 AM and the task has not yet completed
        elif dt_time(7, 0) <= current_time < dt_time(8, 0):
            sleep_duration = random.uniform(0, 3600)  # случайное время между 0 и 1 часом
            await asyncio.sleep(sleep_duration)
            await collections_mining(chat_id)

            # We set the next execution for the next approach between 8:30 and 19:00
            next_run = datetime.combine(now.date(), dt_time(8, 30))
            sleep_duration = (next_run - now).total_seconds()
            print(f"Script on standby until {next_run}. Waiting time: {sleep_duration / 3600:.2f} hours.")
            await asyncio.sleep(sleep_duration)
            continue

        # If the current time is between 8:30 AM and 19:00 PM
        elif dt_time(8, 30) <= current_time < dt_time(19, 0):
            sleep_duration = random.uniform(1.5 * 3600, 2 * 3600)  # случайное время между 1.5 и 5 часами
            await asyncio.sleep(sleep_duration)
            now = datetime.now()  # Update the current time after waiting
            current_time = now.time()

            if dt_time(8, 30) <= current_time < dt_time(19, 0):
                await collections_mining(chat_id)

            # If the current time is after 19:00 and before 23:59
            if dt_time(19, 0) <= current_time < dt_time(23, 59):
                await collections_mining(chat_id)
                next_run = datetime.combine(now.date() + timedelta(days=1), dt_time(0, 0))
            else:
                # Time delay until next start in the range 8:30 - 19:00
                sleep_duration = random.uniform(1.5 * 3600, 5 * 3600)
                print(f"The script is in standby mode until the next launch in the range 8:30 - 19:00. "
                      f"Waiting time: {sleep_duration / 3600:.2f} hours.")
                await asyncio.sleep(sleep_duration)
                continue

            sleep_duration = (next_run - now).total_seconds()
            print(f"Script on standby until {next_run}. Waiting time: {sleep_duration / 3600:.2f} hours.")
            await asyncio.sleep(sleep_duration)


async def get_last_message(client: TelegramClient, chat_id: str) -> Message:
    history = await client(GetHistoryRequest(
        peer=chat_id,
        limit=1,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    if (len(history.messages[0].message.split('\n')) == 1 or not history.messages
            or 'успешно выведены!' in history.messages[0].message or not history.messages[0].reply_markup):
        await client.send_message(chat_id, '/start')
        await asyncio.sleep(random.uniform(1, 3))

        history = await client(GetHistoryRequest(
            peer=chat_id,
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

    return history.messages[0]


async def click_button(client: TelegramClient, chat_id: str, last_message: Message, text='Клик!') -> None:
    try:
        if last_message.reply_markup:
            for button_row in last_message.reply_markup.rows:
                for button in button_row.buttons:
                    if isinstance(button, KeyboardButtonCallback) and text in button.text:
                        client.loop.create_task(
                            client(GetBotCallbackAnswerRequest(
                                peer=chat_id,
                                msg_id=last_message.id,
                                data=button.data
                            ))
                        )
                        print(f"Click button: {button.text}")
    except Exception as error:
        print(f"The bot did not answer to the callback query in time: {error}")


async def calculate_limits(chat_id) -> tuple:
    last_message: Message = await get_last_message(client, chat_id)
    limit = int(last_message.message.split('\n')[4].split('/')[1])
    if limit in [300, 350, 400]:
        login_to_the_game = random.randint(1, 2)
    else:
        login_to_the_game = random.randint(2, 4)
    max_click = limit // login_to_the_game
    if login_to_the_game == 1:
        quantity_click = limit
    else:
        quantity_click = random.randint(max_click // 100 * 75, max_click)
    return limit, login_to_the_game, max_click, quantity_click


async def click_button_until_limit(chat_id: str) -> None:
    global new_day, login_to_the_game, now_time, max_click, quantity_click, max_hours_wait, limit, collections
    logging = 0
    click = 0

    while True:
        await wait_until_morning()

        last_message = await get_last_message(client, chat_id)
        if last_message is None:
            break

        if new_day:
            new_day = False
            now_time = time.time()
            collections = True
            await collections_mining(chat_id)
            await click_button(client, chat_id, last_message)
            delay = random.choice(click_delay)
            print(f"Delay: {delay} seconds")
            await asyncio.sleep(delay)
            last_message = await get_last_message(client, chat_id)

            limit, login_to_the_game, max_click, quantity_click = await calculate_limits(chat_id)
            print(
                f"A new day has begun. Limit: {limit}, Number of logins: {login_to_the_game}, "
                f"Max clicks per login: {max_click}")

            with open("log_for_click.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - New day, number of inputs = {login_to_the_game}. "
                               f"For client: {(await client.get_me()).phone} – {(await client.get_me()).username}\n")

        if "Лимит: 0" in last_message.message:
            new_day = True
            click = 1
            collections = True
            print("The limit has been reached.")
            times = 86400 - (int(str(time.time()).split('.')[0]) - int(str(now_time).split('.')[0]))
            await asyncio.sleep(random.uniform(times, times + 10_821))
            continue

        if logging != login_to_the_game:
            if (not collections) and mining:
                collections = True
                await collections_mining(chat_id)

            await click_button(client, chat_id, last_message)
            click += 1
            if click >= quantity_click and limit != 1:
                click = 0
                logging += 1
                collections = False
                quantity_click = random.randint(max_click // 100 * 65, max_click)
                await asyncio.sleep(random.uniform(1801, max_hours_wait))
            else:
                delay = random.choice(click_delay)
                print(f"Delay: {delay} seconds")
                await asyncio.sleep(delay)
        else:
            if (not collections) and mining:
                collections = True
                await collections_mining(chat_id)

            await click_button(client, chat_id, last_message)
            delay = random.choice(click_delay)
            print(f"Delay: {delay} seconds")
            await asyncio.sleep(delay)


async def main() -> None:
    # Enter chat ID
    chat_id: str = id_bot_touch

    # Opening the connection
    client.start()

    if mining:
        # Running tasks
        task1 = asyncio.create_task(click_button_until_limit(chat_id))
        task2 = asyncio.create_task(time_based_task(chat_id))

        await asyncio.gather(task1, task2)
    else:
        await click_button_until_limit(chat_id)


with client:
    client.loop.run_until_complete(main())
