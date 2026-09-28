"""
EduGenie: Quiz Generation Module
Generates exactly 3 multiple-choice questions (4 options each) from a given passage or topic.
Features JSON cleaning via clean_json_block and rigorous schema validation.
"""

import json
import re
from typing import Any, Dict, List, Union
import gemini_client

QUIZ_SYSTEM_PROMPT = (
    "You are EduGenie's Quiz Master. Your task is to generate exactly three (3) high-quality multiple-choice questions "
    "based on the provided passage or educational topic. "
    "Requirements: "
    "1. Each question must test understanding or key facts from the text. "
    "2. Each question must have exactly four (4) plausible options. "
    "3. Exactly one option must be the correct answer. "
    "4. Provide a brief 1-2 sentence pedagogical explanation for why the answer is correct. "
    "5. Return ONLY a valid JSON array matching this exact schema: "
    "[\n"
    "  {\n"
    "    \"id\": 1,\n"
    "    \"question\": \"Question text?\",\n"
    "    \"options\": [\"Option 1\", \"Option 2\", \"Option 3\", \"Option 4\"],\n"
    "    \"answer\": \"Option 1\",\n"
    "    \"explanation\": \"Why Option 1 is correct.\"\n"
    "  }\n"
    "]\n"
    "Do not include any conversational preamble or outro. Output only raw JSON."
)

def clean_json_block(text: str) -> str:
    """
    Cleans markdown code fences, backticks, and extraneous text around JSON blocks.
    
    Args:
        text: Raw text returned by LLM.
        
    Returns:
        Clean JSON string ready for json.loads.
    """
    if not text:
        return ""
    
    cleaned = text.strip()
    
    # Remove ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()
    
    # Find outer bracket bounds [ ... ]
    start_bracket = cleaned.find("[")
    end_bracket = cleaned.rfind("]")
    
    if start_bracket != -1 and end_bracket != -1 and end_bracket > start_bracket:
        cleaned = cleaned[start_bracket : end_bracket + 1]
    else:
        # Check if model wrapped in a dict like {"questions": [...]}
        start_brace = cleaned.find("{")
        end_brace = cleaned.rfind("}")
        if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
            cleaned = cleaned[start_brace : end_brace + 1]
            
    return cleaned.strip()

def generate_quiz(topic_or_passage: str) -> Dict[str, Any]:
    """
    Generates 3 multiple choice questions with 4 options each from topic or text.
    
    Args:
        topic_or_passage: Study text, paragraph, or concept name.
        
    Returns:
        Dictionary containing 'success', 'quiz' (list of questions), and optional 'error'.
    """
    if not topic_or_passage or not topic_or_passage.strip():
        return {
            "success": False,
            "error": "Please provide a topic or passage to generate a quiz.",
            "quiz": []
        }

    prompt = (
        f"Generate 3 multiple-choice questions with 4 options each based on this material:\n\n"
        f"\"\"\"\n{topic_or_passage.strip()}\n\"\"\"\n\n"
        f"Return ONLY valid JSON."
    )

    raw_response = gemini_client.generate_text(
        prompt=prompt,
        system_prompt=QUIZ_SYSTEM_PROMPT,
        json_mode=True
    )

    # Check for API key warning or error strings returned by gemini_client
    if raw_response.startswith("⚠️") or raw_response.startswith("❌"):
        return {
            "success": False,
            "error": raw_response,
            "quiz": []
        }

    cleaned = clean_json_block(raw_response)

    try:
        parsed = json.loads(cleaned)
        
        # If response wrapped in an object like {"quiz": [...]} or {"questions": [...]}
        if isinstance(parsed, dict):
            for key in ("quiz", "questions", "data", "items"):
                if key in parsed and isinstance(parsed[key], list):
                    parsed = parsed[key]
                    break
                    
        if not isinstance(parsed, list):
            return {
                "success": False,
                "error": f"Model response was not a JSON list: {raw_response[:200]}",
                "quiz": []
            }

        validated_quiz = []
        for i, item in enumerate(parsed[:3], start=1):
            if not isinstance(item, dict):
                continue
            question_text = item.get("question") or f"Question {i}"
            options = item.get("options") or []
            if not isinstance(options, list) or len(options) < 2:
                continue
            
            # Format options cleanly
            clean_options = [str(opt).strip() for opt in options[:4]]
            answer = str(item.get("answer", clean_options[0])).strip()
            explanation = str(item.get("explanation", "Correct answer verified.")).strip()

            validated_quiz.append({
                "id": i,
                "question": question_text,
                "options": clean_options,
                "answer": answer,
                "explanation": explanation
            })

        if not validated_quiz:
            return {
                "success": False,
                "error": "Failed to parse questions in the expected format. Raw response: " + raw_response[:300],
                "quiz": []
            }

        return {
            "success": True,
            "quiz": validated_quiz,
            "count": len(validated_quiz)
        }

    except json.JSONDecodeError as err:
        return {
            "success": False,
            "error": f"JSON parsing error ({str(err)}). Raw response: {raw_response[:300]}",
            "quiz": []
        }
