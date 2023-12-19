import asyncio
from openai_session_handler.models.genericassistant import GenericAssistant


async def resource_watcher(task_queue):
    try:
        while True:
            print("hi")
            print(GenericAssistant.list_assistants())
                        
            await asyncio.sleep(5)  # Interval between checks for new entities
    except Exception as e:
        log_error('ResourceWatcher', e)


def log_error(source, error):
    # Implement your logging here
    pass

async def main() :
    task_queue = []

    watcher_task = asyncio.create_task(resource_watcher(task_queue))
    task_queue.append(watcher_task)
    await asyncio.gather(*task_queue)

if __name__ == "__main__":
    asyncio.run(main())