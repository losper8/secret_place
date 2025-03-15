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

    def _create_embs_map(self, embs_cfg):
        d = {}
        for emb in embs_cfg:
            d[emb.emb_name] = {
                {
                    'POST': {
                        'idea': MethodPostIdea(schema=emb.schema, host=emb.host, port=emb.port),
                        'pure': MethodPostSearchPure(schema=emb.schema, host=emb.host, port=emb.port),
                        'combined': MethodPostSearchCombined(schema=emb.schema, host=emb.host, port=emb.port)
                    }
                        ,
                    'GET': { 
                            'tfidf': MethodGetTFIDF(schema=emb.schema, host=emb.host, port=emb.port)
                    },
                    'DELETE': {
                            'delete': MethodDelete(schema=emb.schema, host=emb.host, port=emb.port)
                    }
                }
            }
        return d

    async def _process_event(self, event):
        emb_name, method, idx, content = event.emb_name, event.method, event.idx, event.content

        embedder = self._methods_map[emb_name][method][idx]
        try:
            await embedder.call(content=content)
        except aiohttp.ClientConnectionError as e:
            self._log.error(f'connection error while sending event: {content}')
        except aiohttp.ClientTimeout as e:
            self._log.error(f'timeout error while sending event: {content}')
        except Exception as e:
            self._log.error(
                f'an unexpected error occurred while sending event: {content}')
        finally:
            self._queue.task_done()

    async def put_event(self, event):
        try:
            await self._queue.put(event)
        except Exception as e:
            self._log.error(f"an exception while putting into queue {e}")
            raise

    async def process_queue(self):
        while True:
            if self._queue.empty():
                self._log.info(f'queue is empty - sleep mode for {SLEEP_MODE} seconds')
                await asyncio.sleep(SLEEP_MODE)
                continue

            event = await self._queue.get()
            await self._process_event(event)
