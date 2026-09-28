"""
EduGenie: Summarization Module
Powered by Google Gemini to condense long academic texts, articles, and textbook passages
into high-yield, structured revision summaries.
"""

import gemini_client

SUMMARY_SYSTEM_PROMPT = (
    "You are EduGenie's Educational Summarizer. "
    "Your goal is to distill long educational texts into high-yield, clear, and structured revision summaries. "
    "Structure your summary into: "
    "1. **Core Concept Overview**: A 2-3 sentence executive summary of the central idea. "
    "2. **Key High-Yield Points**: Bullet points capturing critical facts, formulas, principles, or events. "
    "3. **Quick Revision Takeaway**: A 1-sentence bottom-line takeaway for exam prep. "
    "Eliminate redundancy, fluff, and conversational chatter."
)

def summarize_text(text: str) -> str:
    """
    Summarizes educational text or articles into a clear, concise study revision format.
    
    Args:
        text: Long educational passage or notes.
        
    Returns:
        Structured markdown summary string.
    """
    if not text or not text.strip():
        return "Please provide a passage or text to summarize."

    cleaned_text = text.strip()
    user_prompt = f"Please summarize the following educational material for quick revision:\n\n{cleaned_text}"

    return gemini_client.generate_text(
        prompt=user_prompt,
        system_prompt=SUMMARY_SYSTEM_PROMPT,
        json_mode=False
    )
