import asyncio
import logging
import inspect
import datetime

class Scheduler:

    def __init__(self, name: str):
        self.name = name
        self._log = logging.getLogger(f'{__name__}.{name}')

        self._scheduled_tasks = {}

    def schedule(self, task_id, coroutine):

        if task_id in self._scheduled_tasks:
            self._log.debug(f"Task #{task_id} was already scheduled")
            coroutine.close()
            return

        task = asyncio.create_task(coroutine, name=f"{self.name}_{task_id}")
        self._scheduled_tasks[task_id] = task
        self._log.debug(f"Scheduled task #{task_id}")

    def schedule_at(self, time, task_id, coroutine):
        now = datetime.now(time.tzinfo) if time.tzinfo else datetime.utcnow()
        delay = (time - now).total_seconds()

        if delay > 0:
            coroutine = self._await_task(delay, task_id, coroutine)
        
        self.schedule(coroutine)

    async def _await_task(self, delay, task_id, coroutine):
        try:
            await asyncio.sleep(delay)
            self._log(f"Scheduled task #{task_id} running")
            await asyncio.shield(coroutine)
        finally:
            state = inspect.getcoroutinestate(coroutine)

            if state == "CORO_CREATED":
                self._log.debug(f"Explicitly closing the coroutine for #{task_id}.")
                coroutine.close()
            else:
                self._log.debug(f"Finally block reached for #{task_id}; {state=}")