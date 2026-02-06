import google.generativeai as genai
import os
from flask import current_app

def get_chatbot_response(message, context_data=None):
    """
    Get response from Gemini API.
    context_data: String containing product info or other context.
    """
    api_key = current_app.config.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    try:
        current_app.logger.info("Gemini key present: %s", bool(api_key))
    except Exception:
        pass
    if not api_key:
        # Fallback / Demo Mode
        if context_data:
            return (
                "Thinking Process (Demo Mode):\n"
                "I see you are interested in some products. "
                "Since my AI brain isn't connected (API Key missing), I can only give you this simple response.\n\n"
                f"{context_data}\n"
                "To enable full AI chat, please set GEMINI_API_KEY in your environment or .env file."
            )
        return "I'm in Demo Mode (No API Key). I can help you find products if you type their names!"

    try:
        genai.configure(api_key=api_key)
        
        # Try multiple models in order of preference; on failure, keep trying next.
        # These IDs are taken from your list_models output and should be supported.
        models_to_try = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-pro-latest']
        
        system_prompt = (
            "You are ShopSmart Assistant, a helpful, witty, and professional AI shopping assistant for ShopSmart (an Amazon-like e-commerce platform). "
            "Your goal is to help users find products, answer questions, and provide recommendations. "
            "Keep answers concise and friendly. "
        )
        
        if context_data:
            system_prompt += f"\n\nContext Information:\n{context_data}\n"
            
        full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
        
        last_error = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                try:
                    current_app.logger.info("Trying Gemini model: %s", model_name)
                except Exception:
                    pass
                response = model.generate_content(full_prompt)
                return response.text
            except Exception as api_error:
                last_error = api_error
                try:
                    current_app.logger.warning("Gemini model failed: %s", model_name)
                    current_app.logger.debug("Error: %s", api_error)
                except Exception:
                    print(f"Gemini model failed {model_name}: {api_error}")
                continue

        # All models failed; fall back to demo response
        try:
            current_app.logger.exception("All Gemini models failed")
        except Exception:
            print(f"Gemini API Error: {last_error}")
        if context_data:
            return (
                "**Note: AI is offline (API Error), showing Demo Response:**\n\n"
                "Based on your search, here are the details you might be looking for:\n\n"
                f"{context_data}\n"
                "*(Please check your API Key configuration to enable full AI chat)*"
            )
        return "I'm currently in Demo Mode (AI Offline). I can help you browse products if you mention them!"

    except Exception as e:
        print(f"Gemini API Setup Error: {e}")
        return "System Error. Please check logs."
