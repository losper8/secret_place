import asyncio
import aiohttp

from asyncio import Queue
from abc import ABC
from loguru import logger
from typing import Dict, Optional, List
           



class Method:
    def __init__(self, 
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str):
        self._endpoint = f'{schema}://{host}:{port}/api/v1/{endpoint}'


class MethodGetREAD(Method):
    def __init__(self,
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = 'read'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)
    async def call(self, content: Optional[Dict] = None):
        async with aiohttp.ClientSession() as session:
            logger.info(f'get read method"s xontent: {content}')
            endpoint = self._endpoint + f'?id={content["id"]}'
            logger.info(f'get read method"s endpoint: {endpoint}')
            async with session.get(endpoint) as response:
                result = await response.read()
        return result


class MethodGetTFIDF(Method):
    def __init__(self, 
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = 'train_tfidf'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

        async def call(self, content: Optional[Dict] = None):
            async with aiohttp.ClientSession() as session:
                logger.info(f'get read method"s xontent: {content}')
                endpoint = self._endpoint + f'?column_type={content["column_type"]}'
                logger.info(f'get read method"s endpoint: {endpoint}')
                async with session.get(self._endpoint, json=content) as response:
                    result = await response.read()
            return result

class MethodPost(Method):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

    async def call(self, content: Dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._endpoint, json=content) as response:
                result = await response.read()
        return result


class MethodPostIdea(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'add_idea'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)


class MethodPostSearchCombined(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'search_combined'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)


class MethodPostSearchPure(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'search_embeddings'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)


class MethodDelete(Method):
    def __init__(self, 
            schema: str,
            host: str,
            port: int,
            endpoint: str = 'delete_idea'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

    async def call(self, content: Dict):
        async with aiohttp.ClientSession() as session:
	  
            async with session.delete(self._endpoint, json=content) as response:
                result = await response.read()
        return result
