from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ChatRequest, ChatResponse
from app.services.llm_client import LLMClient
from app.services.embeddings import EmbeddingsStore
from app.api.deps import get_db_session, get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

llm_client = LLMClient()
emb_store = EmbeddingsStore()


@router.post("/query", response_model=ChatResponse)
async def chat_query(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(get_current_user),
):
    question = payload.question

    # 1. Embed question
    q_emb = emb_store.embed_text(question)

    # 2. Retrieve docs from vector store (stub)
    docs = emb_store.similarity_search(q_emb, top_k=payload.top_k)

    # 3. Build context
    context_text = "\n\n".join([d.get("text", "") for d in docs])

    system_prompt = (
        "You are Bullock, an AI-powered investment & trading assistant. "
        "Use provided context and general financial knowledge to answer questions. "
        "If context is empty, still provide helpful general guidance, but avoid "
        "giving strict financial or legal guarantees."
    )

    full_user_message = f"Context:\n{context_text}\n\nUser question:\n{question}"

    answer = llm_client.chat(system_prompt=system_prompt, user_message=full_user_message)

    return ChatResponse(
        answer=answer,
        sources=[d.get("id", "") for d in docs],
    )
