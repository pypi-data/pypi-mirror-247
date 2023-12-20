from __future__ import annotations

import asyncio
import json
import logging
import os
import ssl
import threading
from dataclasses import asdict
from typing import TYPE_CHECKING, Any, Callable, Iterable, MutableMapping, Optional

from pydantic.dataclasses import dataclass
from websockets import Headers
from websockets.client import connect

from ert.async_utils import background_tasks
from ert.job_queue.queue import EVTYPE_ENSEMBLE_CANCELLED, EVTYPE_ENSEMBLE_STOPPED
from ert.scheduler.driver import Driver, JobEvent
from ert.scheduler.job import Job
from ert.scheduler.local_driver import LocalDriver

if TYPE_CHECKING:
    from ert.ensemble_evaluator._builder._realization import Realization


logger = logging.getLogger(__name__)


@dataclass
class _JobsJson:
    ens_id: str
    real_id: str
    dispatch_url: str
    ee_token: Optional[str]
    ee_cert_path: Optional[str]
    experiment_id: str


class Scheduler:
    def __init__(self, driver: Optional[Driver] = None) -> None:
        if driver is None:
            driver = LocalDriver()
        self.driver = driver
        self._jobs: MutableMapping[int, Job] = {}
        self._tasks: MutableMapping[int, asyncio.Task[None]] = {}

        self._events: Optional[asyncio.Queue[Any]] = None
        self._cancelled = False
        # will be read from QueueConfig
        self._max_submit: int = 2

        self._ee_uri = ""
        self._ens_id = ""
        self._ee_cert: Optional[str] = None
        self._ee_token: Optional[str] = None

    async def ainit(self) -> None:
        # While supporting Python 3.8, this statement must be delayed.
        if self._events is None:
            self._events = asyncio.Queue()

    def add_realization(self, real: Realization, callback_timeout: Any = None) -> None:
        self._jobs[real.iens] = Job(self, real)

    def kill_all_jobs(self) -> None:
        self._cancelled = True
        for task in self._tasks.values():
            task.cancel()

    def stop_long_running_jobs(self, minimum_required_realizations: int) -> None:
        pass

    def set_ee_info(
        self, ee_uri: str, ens_id: str, ee_cert: Optional[str], ee_token: Optional[str]
    ) -> None:
        self._ee_uri = ee_uri
        self._ens_id = ens_id
        self._ee_cert = ee_cert
        self._ee_token = ee_token

    async def _publisher(self) -> None:
        if not self._ee_uri:
            return
        tls: Optional[ssl.SSLContext] = None
        if self._ee_cert:
            tls = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            tls.load_verify_locations(cadata=self._ee_cert)
        headers = Headers()
        if self._ee_token:
            headers["token"] = self._ee_token

        if self._events is None:
            await self.ainit()
        assert self._events is not None

        async with connect(
            self._ee_uri,
            ssl=tls,
            extra_headers=headers,
            open_timeout=60,
            ping_timeout=60,
            ping_interval=60,
            close_timeout=60,
        ) as conn:
            while True:
                event = await self._events.get()
                await conn.send(event)

    def add_dispatch_information_to_jobs_file(self) -> None:
        for job in self._jobs.values():
            self._update_jobs_json(job.iens, job.real.run_arg.runpath)

    async def execute(
        self,
        semaphore: Optional[threading.BoundedSemaphore] = None,
        queue_evaluators: Optional[Iterable[Callable[..., Any]]] = None,
    ) -> str:
        if queue_evaluators is not None:
            logger.warning(f"Ignoring queue_evaluators: {queue_evaluators}")

        async with background_tasks() as cancel_when_execute_is_done:
            cancel_when_execute_is_done(self._publisher())
            cancel_when_execute_is_done(self._process_event_queue())
            cancel_when_execute_is_done(self.driver.poll())

            start = asyncio.Event()
            sem = asyncio.BoundedSemaphore(
                semaphore._initial_value if semaphore else 10  # type: ignore
            )
            for iens, job in self._jobs.items():
                self._tasks[iens] = asyncio.create_task(
                    job(start, sem, self._max_submit)
                )

            start.set()
            for task in self._tasks.values():
                await task

            await self.driver.finish()

        if self._cancelled:
            return EVTYPE_ENSEMBLE_CANCELLED

        return EVTYPE_ENSEMBLE_STOPPED

    async def _process_event_queue(self) -> None:
        if self.driver.event_queue is None:
            await self.driver.ainit()
        assert self.driver.event_queue is not None

        while True:
            iens, event = await self.driver.event_queue.get()
            if event == JobEvent.STARTED:
                self._jobs[iens].started.set()
            elif event == JobEvent.COMPLETED:
                self._jobs[iens].returncode.set_result(0)
            elif event == JobEvent.FAILED:
                self._jobs[iens].returncode.set_result(1)
            elif event == JobEvent.ABORTED:
                self._jobs[iens].aborted.set()

    def _update_jobs_json(self, iens: int, runpath: str) -> None:
        jobs = _JobsJson(
            experiment_id="_",
            ens_id=self._ens_id,
            real_id=str(iens),
            dispatch_url=self._ee_uri,
            ee_token=self._ee_token,
            ee_cert_path=self._ee_cert,
        )
        jobs_path = os.path.join(runpath, "jobs.json")
        with open(jobs_path, "r") as fp:
            data = json.load(fp)
        with open(jobs_path, "w") as fp:
            data.update(asdict(jobs))
            json.dump(data, fp)
