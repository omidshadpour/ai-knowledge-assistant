from app.services.retrieval import retrieve_documents
from app.llm.groq_service import generate_answer , generate_answer_stream
from app.core.exceptions import DocumentNotFoundError , LLMError
from app.core.logger import get_logger
from app.services.memory import get_history , add_message

logger = get_logger("rag")

def build_context(retrieved_docs):
    context = ""
    for doc in retrieved_docs:
        context += doc.page_content + "\n\n"

    return context

def create_prompt(question , context , history):
    history_text = ""
    
    for msg in history:
        history_text += f"{msg['role']} : {msg['content']}\n"

    prompt = f"""
You are a helpful AI assistant.

Use chat history and document context to answer.

Chat History:
{history_text}

Context:
{context}

Question:
{question}

If the answer is not in the context, say:
"I don't know based on the document."
"""
    return prompt

def extract_sources(retrieved_docs):
    seen = set()
    sources = []

    for doc in retrieved_docs:
        page = doc.metadata.get("page")
        source = doc.metadata.get("source")
        key = (source , page)

        if key not in seen:
            seen.add(key)
        
            sources.append(
                {
                    "page" : page,
                    "source" : source
                }
            )

    return sources



def ask_question(question: str , document_id : str , session_id: str):
    logger.info(f"Question received for document_id: {document_id}")
    
    history = get_history(session_id)
    docs = retrieve_documents(question , document_id)
    logger.debug(f"Retrieved {len(docs)} documents")

    if not docs:
        logger.warning(f"No documents found for document_id : {document_id}")
        raise DocumentNotFoundError(document_id)
    
    
    context = build_context(docs)
    prompt = create_prompt(question , context , history)
    try:
        answer = generate_answer(prompt)
    except Exception as e:
            logger.error(f"LLM failed: {str(e)}")
            raise LLMError(str(e))
    
    add_message(session_id , "user" , question)
    add_message(session_id , "assistant" , answer)
    
    logger.info(f"Answer generated successfully")
    sources = extract_sources(docs)
    
    return {
        "answer": answer,
        "sources": sources
    }

def ask_question_stream(question: str ,document_id : str , session_id: str):
    logger.info(f"Stream question received for document_id: {document_id}")

    history = get_history(session_id)
    docs = retrieve_documents(question , document_id)
    logger.debug(f"Retrieved {len(docs)} documents")

    if not docs:
        logger.warning(f"No documents found for document_id : {document_id}")
        raise DocumentNotFoundError(document_id)
    
    context = build_context(docs)
    prompt = create_prompt(question , context , history)

    full_answer = ""

    for token in generate_answer_stream(prompt):
        full_answer += token
        yield token

    add_message(session_id , "user" , question)
    add_message(session_id , "assistant" , full_answer)
    logger.info("Stream answer completed")