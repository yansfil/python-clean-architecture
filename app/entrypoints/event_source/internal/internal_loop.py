import nest_asyncio

nest_asyncio.apply()

import asyncio

from app.services.messagebus import handle_event, message_queue


async def event_loop():
    while True:
        event = await message_queue.get()
        handle_event(event)


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.create_task(event_loop())


def run_event_loop_background():
    loop = asyncio.new_event_loop()
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor() as executor:
        executor.submit(loop_in_thread, loop)
