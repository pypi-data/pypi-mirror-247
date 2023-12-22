from glob_utils import APIClient
from pydantic import Field
from os import environ
from pinedantic._types import QueryRequest, QueryResponse, UpsertRequest, UpsertResponse, QueryMatch, UpsertVectors, Vector, Filter

class Pinecone(APIClient):
	base_url:str = Field(default=environ.get('PINECONE_URL', 'https://api.pinecone.io'))
	headers:dict[str,str] = Field(default_factory=lambda: {'api-key': environ.get('PINECONE_API_KEY')})

	async def query(self, vector:Vector, filter:Filter, topK:int=10) -> QueryResponse:
		request = QueryRequest(vector=vector, filter=filter, topK=topK)
		response = await self.post('/query', json=request.dict())
		return QueryResponse(**response)
	
	async def upsert(self, vectors:list[Vector]) -> UpsertResponse:
		request = UpsertRequest(vectors=vectors)
		response = await self.post('/vectors/upsert', json=request.dict())
		return UpsertResponse(**response)