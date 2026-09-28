"""
EduGenie: Academic Question & Answering (QnA) Module
Powered by Google Gemini to answer academic, scientific, and general knowledge questions.
"""

import gemini_client

QNA_SYSTEM_PROMPT = (
    "You are EduGenie's Academic Q&A Specialist. "
    "Your goal is to provide accurate, smart, concise, and structured answers to student questions. "
    "Structure your response with: "
    "1. A direct, clear answer in the first sentence. "
    "2. Key supporting facts, concepts, or historical context. "
    "3. A 'Did You Know?' or quick summary takeaway. "
    "Keep explanations educational, accessible, and free of unnecessary fluff."
)

def answer_question(question: str) -> str:
    """
    Answers academic and general knowledge questions concisely and accurately.
    
    Args:
        question: The user's query or study question.
        
    Returns:
        Structured response string.
    """
    if not question or not question.strip():
        return "Please provide a valid question to receive an answer."

    cleaned_question = question.strip()
    user_prompt = f"Question: {cleaned_question}\n\nPlease provide a clear, accurate, and educational answer."
    
    return gemini_client.generate_text(
        prompt=user_prompt,
        system_prompt=QNA_SYSTEM_PROMPT,
        json_mode=False
    )
