"""
EduGenie: Learning Path & Recommendations Module
Powered by Google Gemini to construct personalized, structured step-by-step
learning roadmaps from beginner to advanced levels, complete with timelines and resources.
"""

import gemini_client

LEARNING_PATH_SYSTEM_PROMPT = (
    "You are EduGenie's Curriculum Architect and AI Learning Mentor. "
    "Your objective is to craft comprehensive, structured, and realistic step-by-step learning roadmaps "
    "for any subject, skill, or academic discipline. "
    "Format each roadmap clearly using Markdown: "
    "1. **Roadmap Overview & Objectives**: What the learner will achieve. "
    "2. **Stage 1: Beginner Foundations**: Key topics, estimated time commitment, milestone project. "
    "3. **Stage 2: Intermediate Mastery**: Core practical skills, applied exercises, timeline. "
    "4. **Stage 3: Advanced & Industry-Level**: Deep concepts, best practices, portfolio project. "
    "5. **Curated Resources & Tools**: Recommended books, documentation, video channels, and practice platforms. "
    "Be specific, encouraging, actionable, and structured."
)

def get_learning_recommendations(topic: str) -> str:
    """
    Generates a personalized, structured learning path for any given skill or topic.
    
    Args:
        topic: The topic, career goal, or skill (e.g., 'SQL for Data Science', 'Quantum Computing').
        
    Returns:
        Structured learning path markdown string.
    """
    if not topic or not topic.strip():
        return "Please enter a topic or subject to generate a learning path."

    cleaned_topic = topic.strip()
    user_prompt = (
        f"Generate a structured, beginner-to-advanced learning roadmap for: '{cleaned_topic}'. "
        f"Include realistic timelines, core sub-topics, milestone projects, and curated learning resources."
    )

    return gemini_client.generate_text(
        prompt=user_prompt,
        system_prompt=LEARNING_PATH_SYSTEM_PROMPT,
        json_mode=False
    )
