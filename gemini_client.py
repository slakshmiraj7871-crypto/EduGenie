"""
Gemini Client Helper for EduGenie
Handles Google Gemini API initialization, model resolution, and resilient text generation.
Supports automatic model fallback across active Google Gemini models.
"""

import os
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
FALLBACK_MODELS: List[str] = [
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
]

def get_api_key() -> Optional[str]:
    """Retrieve the Gemini API key from environment variables."""
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if key and key.strip() and key.strip() != "your_gemini_api_key_here":
        return key.strip()
    return None

def is_api_key_configured() -> bool:
    """Check if a valid Gemini API key is configured."""
    return get_api_key() is not None

def generate_text(prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
    """
    Generate content using Google Gemini with robust error handling and model fallback.
    
    Args:
        prompt: The user input or instructional prompt.
        system_prompt: Optional system instruction for pedagogical tuning.
        json_mode: Whether to enforce application/json response format.
        
    Returns:
        The generated text string or a user-friendly error explanation.
    """
    api_key = get_api_key()
    if not api_key:
        return (
            "⚠️ **Gemini API Key Missing**: Please set your `GEMINI_API_KEY` in the `.env` file.\n\n"
            "1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate a free key.\n"
            "2. Open the `.env` file in the project folder and set `GEMINI_API_KEY=your_key_here`.\n"
            "3. Restart the server or try again."
        )

    # Check if modern google-genai is installed
    try:
        from google import genai
        from google.genai import types
        has_google_genai = True
    except ImportError:
        has_google_genai = False

    # Check if legacy google-generativeai is installed
    try:
        import google.generativeai as legacy_genai
        has_legacy_genai = True
    except ImportError:
        has_legacy_genai = False

    if not has_google_genai and not has_legacy_genai:
        return "❌ Neither `google-genai` nor `google-generativeai` package is installed. Run `pip install google-genai`."

    raw_model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    primary_model = raw_model.strip().strip("'\"").replace(" ", "-").lower() if raw_model else DEFAULT_MODEL
    
    # Build unique list of models to try in sequence
    models_to_try = [primary_model]
    for fb in FALLBACK_MODELS:
        if fb not in models_to_try:
            models_to_try.append(fb)

    last_error = ""

    # Strategy 1: Use modern google-genai SDK
    if has_google_genai:
        try:
            client = genai.Client(api_key=api_key)
            config_args = {}
            if system_prompt:
                config_args["system_instruction"] = system_prompt
            if json_mode:
                config_args["response_mime_type"] = "application/json"

            config = types.GenerateContentConfig(**config_args) if config_args else None

            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=config,
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception as model_err:
                    err_msg = str(model_err)
                    last_error = err_msg

                    # If API key itself is invalid, no model will work
                    if "API_KEY_INVALID" in err_msg or "API key not valid" in err_msg:
                        return "❌ **Invalid API Key**: The provided `GEMINI_API_KEY` is not valid. Please check your key at Google AI Studio."
                    if "RESOURCE_EXHAUSTED" in err_msg:
                        return "⚠️ **Rate Limit Reached**: Gemini quota exceeded. Please wait a moment before trying again."
                    
                    # If model is deprecated (404) or busy (503), continue to next model in list
                    continue

            return f"❌ All candidate Gemini models failed. Last error: {last_error}"

        except Exception as client_err:
            last_error = str(client_err)

    # Strategy 2: Legacy google-generativeai SDK fallback
    if has_legacy_genai:
        try:
            legacy_genai.configure(api_key=api_key)
            generation_config = {}
            if json_mode:
                generation_config["response_mime_type"] = "application/json"

            for model_name in models_to_try:
                try:
                    kwargs = {"model_name": model_name}
                    if system_prompt:
                        kwargs["system_instruction"] = system_prompt
                    model = legacy_genai.GenerativeModel(**kwargs)
                    response = model.generate_content(
                        prompt,
                        generation_config=generation_config if generation_config else None
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception as leg_err:
                    last_error = str(leg_err)
                    continue

            return f"❌ Gemini API Error: {last_error}"
        except Exception as e:
            return f"❌ Gemini API Error: {str(e)}"

    return f"❌ Could not generate response. Error: {last_error}"
