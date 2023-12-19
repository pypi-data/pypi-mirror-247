#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : embeddings
# @Time         : 2023/7/31 10:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/abetlen/llama-cpp-python/blob/main/llama_cpp/server/app.py

from meutils.pipe import *
from chatllm.schemas.embedding import EmbeddingRequest

from fastapi import Depends, FastAPI, APIRouter, Request, Response
from openai.types.create_embedding_response import CreateEmbeddingResponse, Embedding, Usage
from sentence_transformers import SentenceTransformer

router = APIRouter()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "/Users/betterme/PycharmProjects/AI/embeddings/m3e-small")
model = SentenceTransformer(model_name_or_path=EMBEDDING_MODEL)


@router.post("/embeddings", summary="Embedding")  # request.model_dump(exclude={"user"})
async def create_embeddings(request: EmbeddingRequest) -> CreateEmbeddingResponse:
    texts = request.input
    if isinstance(texts, str):
        texts = [texts]

    embeddings = model.encode(texts).tolist()
    data = [Embedding(index=i, embedding=e, object="embedding") for i, e in enumerate(embeddings)]

    usage = Usage(prompt_tokens=100 * len(texts), total_tokens=100 * len(texts))

    return CreateEmbeddingResponse(data=data, model=request.model, object="list", usage=usage)


if __name__ == '__main__':
    model
