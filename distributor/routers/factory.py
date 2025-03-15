import asyncio
import aiohttp

from asyncio import Queue
from abc import ABC
from typing import Dict, Optional, List

class Method:
    def __init__(self, 
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str):
        self._endpoint = f'{schema}://{host}:{port}/{endpoint}'
    

class MethodGetTFIDF(Method):
    def __init__(self, 
                 schema: str,
                 host: str,
                 port: int,
                 endpoint: str = '/train_tfidf'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)
    
    async def call(self, content: Optional[Dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._endpoint) as response:
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
                endpoint: str = '/add_idea'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)


class MethodPostSearchCombined(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = '/search_combined'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)


class MethodPostSearchPure(MethodPost):
    def __init__(self, 
                schema: str,
                host: str,
                port: int,
                endpoint: str = '/search_embeddings'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)


class MethodDelete(Method):
    def __init__(self, 
            schema: str,
            host: str,
            port: int,
            endpoint: str = '/delete_idea'):
        super().__init__(schema=schema, host=host, port=port, endpoint=endpoint)

    async def call(self, content: Dict):
        async with aiohttp.ClientSession() as session:
            async with session.delete(self._endpoint, json=content) as response:
                result = await response.read()
        return result