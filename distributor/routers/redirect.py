import asyncio
import aiohttp

from asyncio import Queue
from abc import ABC
from typing import Dict, Optional, List

from loguru import logger

from distributor.common.utilies import Singleton
from distributor.routers.factory import MethodPostSearchTFIDF, MethodPostIdea, MethodPostSearchPure, MethodPostSearchCombined, MethodGetEmbeddingsSize, MethodGetTFIDF, MethodGetRead, MethodGetFirstTimeLoadEmbeddings, MethodDelete

SLEEP_MODE = 5


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
                        'search_tfidf': MethodPostSearchTFIDF(schema=emb.schema, host=emb.host, port=emb.port),
                        'add_idea': MethodPostIdea(schema=emb.schema, host=emb.host, port=emb.port),
                        'search_embeddings': MethodPostSearchPure(schema=emb.schema, host=emb.host, port=emb.port),
                        'search_combined': MethodPostSearchCombined(schema=emb.schema, host=emb.host, port=emb.port)
                    },
                    'GET': { 
                        'embeddings_size': MethodGetEmbeddingsSize(schema=emb.schema, host=emb.host, port=emb.port),
                        'train_tfidf': MethodGetTFIDF(schema=emb.schema, host=emb.host, port=emb.port),
                        'read': MethodGetRead(schema=emb.schema, host=emb.host, port=emb.port),
                        'first_time_load_embeddings': MethodGetFirstTimeLoadEmbeddings(schema=emb.schema, host=emb.host, port=emb.port)     
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
            self._log.info(f'embedder was chosen')
            result = await embedder.call(content=content)
            self._log.info(f'result was recieved')
            future.set_result(result)
        except aiohttp.ClientConnectionError as e:
            self._log.error(f'connection error while sending event: {e}')
        except aiohttp.ConnectionTimeoutError as e:
            self._log.error(f'timeout error while sending event: {e}')
        except KeyError as e:
            self._log.error(f'user input error please review request parameters')
        except Exception as e:
            self._log.error(
                f'an unexpected error occurred {type(e)} while sending event: {e}')
        finally:
            self._queue.task_done()
            if not future.done():  # Проверка состояния future
                future.set_result(result)
            self._log.info('the result was set')

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
            try:
                self._log.info(f'check if queue is empty')
                if not self._queue.empty():
                    self._log.info(f'queue is not empty')
                    future, event = await self._queue.get()
                    await self._process_event(future=future, event=event)
                    self._log.info(f'process finished')
                elif self._queue.empty():
                    self._log.info(f'queue is empty - sleep mode for {SLEEP_MODE} seconds')
                    await asyncio.sleep(SLEEP_MODE)
            except Exception as e:
                self._log.error(f'there is an exception type {type(e)} during test: {e}')
                self._log.warning(f'activate sleep mode for {SLEEP_MODE} seconds')
                await asyncio.sleep(SLEEP_MODE)

    async def run(self):
        tsks = []
        tsks.append(self._process_queue())
        await asyncio.gather(*tsks)

    def process_queue(self):
        self._major_task = asyncio.create_task(self.run())
