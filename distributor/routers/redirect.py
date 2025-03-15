import asyncio
import aiohttp

from asyncio import Queue
from abc import ABC
from typing import Dict, Optional, List

from loguru import logger

from distributor.common.utilies import Singleton
from distributor.routers.factory import MethodGetTFIDF, MethodPostIdea, MethodPostSearchCombined, MethodPostSearchPure, MethodDelete

SLEEP_MODE = 15


class Curator(metaclass=Singleton):
    def __init__(self, queue: Optional[Queue] = None, embs_cfg: Optional[List] = None):
        self._queue = queue
        self._log = logger
        self._embs_map = self._create_embs_map(embs_cfg)
        self._major_task = None

    def _create_embs_map(self, embs_cfg):
        d = {}
        for emb in embs_cfg:
            d[emb.emb_name] = {
                    'POST': {
                        'idea': MethodPostIdea(schema=emb.schema, host=emb.host, port=emb.port),
                        'pure': MethodPostSearchPure(schema=emb.schema, host=emb.host, port=emb.port),
                        'combined': MethodPostSearchCombined(schema=emb.schema, host=emb.host, port=emb.port)
                    },
                    'GET': { 
                            'tfidf': MethodGetTFIDF(schema=emb.schema, host=emb.host, port=emb.port)
                    },
                    'DELETE': {
                            'delete': MethodDelete(schema=emb.schema, host=emb.host, port=emb.port)
                    }
                }
        return d

    async def _process_event(self, future, event):
        self._log.info(f'there is an event: {event}')
        result = 'err'
        try:
            emb_name, method, idx, content = event.emb_name, event.method, event.idx, event.content
            embedder = self._embs_map[emb_name][method][idx]
            result = await embedder.call(content=content)
        except aiohttp.ClientConnectionError as e:
            self._log.error(f'connection error while sending event: {content}')
        except aiohttp.ClientTimeout as e:
            self._log.error(f'timeout error while sending event: {content}')
        except KeyError as e:
            self._log.error(f'user input error please review request parameters')
        except Exception as e:
            self._log.error(
                f'an unexpected error occurred while sending event: {content}')
        finally:
            self._queue.task_done()
            future.set_result(result)

    async def put_event(self, event):
        try:
            future = asyncio.Future()
            await self._queue.put((future, event))
            return await future
        except Exception as e:
            self._log.error(f"an exception while putting into queue {e}")
            raise

    async def _process_queue(self):
        while True:
            if self._queue.empty():
                self._log.info(f'queue is empty - sleep mode for {SLEEP_MODE} seconds')
                await asyncio.sleep(SLEEP_MODE)
                continue

            future, event = await self._queue.get()
            await self._process_event(future=future, event=event)

    def process_queue(self):
        self._major_task = asyncio.create_task(self._process_queue())
