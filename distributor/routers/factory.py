import asyncio
import aiohttp
import json
from asyncio import Queue
from abc import ABC
from loguru import logger
from typing import Dict, Optional, List, Any
               



class Method:
    def __init__(self, 
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str):
        self._endpoint = f'{schema}://{host}:{port}/api/v1/{endpoint}'

    async def _process_response(self, response: aiohttp.ClientResponse) -> Any:
        return await response.json()



class MethodGetRead(Method):
    def __init__(self,
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = 'read'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)
    async def call(self, content: Optional[Dict] = None):
        async with aiohttp.ClientSession() as session:
            logger.info(f'get read method"s content: {content}')
            endpoint = self._endpoint + f'?id={content["id"]}'
            logger.info(f'get read method"s endpoint: {endpoint}')
            async with session.get(endpoint) as response:
                return await self._process_response(response)


class MethodGetFirstTimeLoadEmbeddings(Method):
    def __init__(self,
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = 'first_time_load_embeddings'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)
    async def call(self, content: Optional[Dict] = None):
        async with aiohttp.ClientSession() as session:
            logger.info(f'get first time load embeddings method"s content: {content}')
            endpoint = self._endpoint + f'?column_type={content["column_type"]}'
            logger.info(f'get first time load embeddings method"s endpoint: {endpoint}')
            async with session.get(endpoint) as response:
                return await self._process_response(response)
            

class MethodGetTFIDF(Method):
    def __init__(self, 
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = 'train_tfidf'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

    async def call(self, content: Optional[Dict] = None):
        async with aiohttp.ClientSession() as session:
            logger.info(f'get tfidf method"s content: {content}')
            endpoint = self._endpoint + f'?column_type={content["column_type"]}'
            logger.info(f'get read method"s endpoint: {endpoint}')
            async with session.get(self._endpoint, json=content) as response:
                return await self._process_response(response)

class MethodGetEmbeddingsSize(Method):
    def __init__(self,
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = 'embeddings_size'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)
    async def call(self, content: Optional[Dict] = None):   
        async with aiohttp.ClientSession() as session:
            logger.info(f'get embeddings size method"s content: {content}')
            endpoint = self._endpoint + f'?column_type={content["column_type"]}'
            logger.info(f'get embeddings size method"s endpoint: {endpoint}')
            async with session.get(endpoint) as response:
                return await self._process_response(response)   

class MethodPost(Method):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

    async def call(self, content: List[Dict]):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._endpoint, json=content) as response:
                return await self._process_response(response)

class MethodPostSearchPure(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'search_embeddings'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

class MethodPostSearchTFIDF(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'search_tfidf'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

class MethodPostSearchCombined(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'search_combined'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

class MethodPostIdea(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = 'add_idea'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)
    

class MethodDelete(Method):
    def __init__(self, 
            schema: str,
            host: str,
            port: int,
            endpoint: str = 'delete_idea'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

    async def call(self, content: Optional[Dict] = None):
        async with aiohttp.ClientSession() as session:
            logger.info(f'delete method"s content: {content}')
            endpoint = self._endpoint + f'?id_guid={content["id_guid"]}'
            logger.info(f'get delete method"s endpoint: {endpoint}')
            async with session.delete(endpoint, json=content) as response:
                return await self._process_response(response)
