from __future__ import annotations
from typing import TypeAlias, Literal, Union
from pydantic import BaseModel, Field
from uuid import uuid4

Vector: TypeAlias = list[float]
RelationalOperator: TypeAlias = Literal["$eq", "$gt", "$gte", "$in", "$lt", "$lte", "$ne", "$nin"]
LogicalOperator: TypeAlias = Literal["$and", "$or"]
Value: TypeAlias = Union[str, int, float, bool, list[str]]
Filter: TypeAlias = Union[dict[str,dict[RelationalOperator,Value]],dict[LogicalOperator,list[dict[str,dict[RelationalOperator,Value]]]]] 

class QueryRequest(BaseModel):
	vector: Vector
	includeMetadata: bool = Field(default=True)
	filter: Filter = Field(default_factory=dict)
	topK: int = Field(default=10)

class QueryMatch(BaseModel):
	id: str
	score: float
	metadata: dict[str,Value]

class QueryResponse(BaseModel):
	matches: list[QueryMatch]

class UpsertVectors(BaseModel):
	id: str = Field(default_factory=lambda: str(uuid4()))
	values: list[Vector]
	metadata: dict[str,Value]

class UpsertRequest(BaseModel):
	vectors: list[UpsertVectors]

class UpsertResponse(BaseModel):
	upsertedCount: int