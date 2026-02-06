from flask import Blueprint, request, jsonify
from app.models import Product
from app.services.chatbot import get_chatbot_response
from app.services.recommendation import get_recommendations
import re

api_bp = Blueprint('api', __name__)


def _extract_price_and_keywords(message: str):
    text = message.lower().replace(',', '')
    numbers = re.findall(r"\d+\.?\d*", text)
    if not numbers:
        return None, []
    amount = float(numbers[0])
    if any(w in text for w in ["under", "below", "less than", "upto", "up to", "maximum", "max"]):
        direction = "max"
    elif any(w in text for w in ["over", "above", "more than", "minimum", "min"]):
        direction = "min"
    else:
        direction = "max"
    keywords = []
    for kw in ["phone", "mobile", "laptop", "headphone", "watch", "tv", "camera", "shoe", "dress", "kurta"]:
        if kw in text:
            keywords.append(kw)
    return (direction, amount), keywords


@api_bp.route('/chatbot', methods=['POST'])
def chatbot_query():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'response': "Hello! How can I help you today?"})
    
    words = message.split()
    products = []

    price_filter, keywords = _extract_price_and_keywords(message)
    if price_filter:
        direction, value = price_filter
        query = Product.query
        if direction == "max":
            query = query.filter(Product.price <= value)
        else:
            query = query.filter(Product.price >= value)

        text = message.lower()
        if any(k in keywords for k in ["phone", "mobile"]):
            query = query.filter(Product.category.ilike('%Electronics%'))
        if any(k in keywords for k in ["dress", "kurta"]):
            query = query.filter(Product.category.ilike('%Fashion%'))

        products = query.order_by(Product.price.asc() if direction == "max" else Product.price.desc()).limit(3).all()

    if not products:
        products = Product.query.filter(
            (Product.name.ilike(f'%{message}%')) | 
            (Product.description.ilike(f'%{message}%')) |
            (Product.category.ilike(f'%{message}%'))
        ).limit(3).all()
    
    if not products and len(words) > 0:
        key_word = max(words, key=len)
        if len(key_word) > 3:
            products = Product.query.filter(Product.name.ilike(f'%{key_word}%')).limit(3).all()
    
    context = ""
    if products:
        context = "Relevant Products in ShopSmart inventory:\n"
        for p in products:
            context += f"- {p.name} (Category: {p.category}, Price: ${p.price}, Stock: {p.stock}). Description: {p.description}\n"
    
    response_text = get_chatbot_response(message, context)
    
    return jsonify({'response': response_text})

@api_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Online'})

@api_bp.route('/gemini/test', methods=['GET'])
def gemini_test():
    try:
        from flask import current_app
        import os
        import google.generativeai as genai
        api_key = current_app.config.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'ok': False, 'error': 'Missing GEMINI_API_KEY'}), 500
        genai.configure(api_key=api_key)
        last_error = None
        # Use the same supported models as the chatbot service
        for model_name in ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-pro-latest']:
            try:
                m = genai.GenerativeModel(model_name)
                r = m.generate_content("Respond only with: OK")
                return jsonify({'ok': True, 'model': model_name, 'text': r.text})
            except Exception as e:
                last_error = str(e)
                continue
        return jsonify({'ok': False, 'error': last_error or 'Unknown error'}), 500
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@api_bp.route('/recommendations/<int:product_id>')
def recommendations(product_id):
    products = get_recommendations(product_id)
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'image_url': p.image_url,
            'price': p.price
        } for p in products
    ])
