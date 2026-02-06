import numpy as np

from rag.llm import ask_llm


def semantic_rag_answer(question: str,index,texts,model,top_k: int = 5)->str:
    """
    Perform semantic search + LLM reasoning."""

    query_embedings=model.encode([question],convert_to_numpy=True)

    distances,indices=index.search(
        np.array(query_embedings),
        top_k
    )

    retrieved_context = "\n\n".join(
    texts[i] for i in indices[0])


    prompt = f"""You are a cybersecurity analyst.
    Answer the question using ONLY the context below....

    CONTEXT: {retrieved_context} 
    QUESTION: {question} 
    Provide: 
    1. Explanation 
    2. Risk impact 
    3. Recommended actions

    """


    return ask_llm(prompt)
    

