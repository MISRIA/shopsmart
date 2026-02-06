import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from app.extensions import db
from app.models import Transaction, Product

def get_recommendations(product_id):
    """
    Generate recommendations using Apriori algorithm based on Transaction history.
    Returns a list of Product objects.
    """
    try:
        # 1. Fetch data
        transactions = Transaction.query.all()
        
        # Heuristic: If we don't have enough data, fallback immediately to save time
        if len(transactions) < 5: 
            return fallback_recommendations(product_id)

        # Create DataFrame
        data = [{'user_id': t.user_id, 'product_id': t.product_id, 'quantity': 1} for t in transactions]
        df = pd.DataFrame(data)

        # 2. One-Hot Encoding
        # Pivot table: Users x Products
        basket = (df.groupby(['user_id', 'product_id'])['quantity']
                  .sum().unstack().reset_index().fillna(0)
                  .set_index('user_id'))
        
        # Encode (1/0)
        def encode_units(x):
            return 1 if x >= 1 else 0

        basket_sets = basket.applymap(encode_units)
        
        # 3. Apriori
        # min_support low because data is sparse in demo
        frequent_itemsets = apriori(basket_sets, min_support=0.05, use_colnames=True)
        if frequent_itemsets.empty:
            return fallback_recommendations(product_id)
            
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
        
        # 4. Filter rules where antecedent contains current product
        # Note: product_id is int. Column names in basket_sets are ints.
        relevant_rules = rules[rules['antecedents'].apply(lambda x: product_id in x)]
        
        if relevant_rules.empty:
            return fallback_recommendations(product_id)
            
        # Sort by lift
        relevant_rules = relevant_rules.sort_values(by='lift', ascending=False).head(3)
        
        rec_ids = set()
        for index, row in relevant_rules.iterrows():
            # consequents is a frozenset
            for item in row['consequents']:
                rec_ids.add(item)
                
        if not rec_ids:
            return fallback_recommendations(product_id)

        # Fetch actual Product objects
        recommended_products = Product.query.filter(Product.id.in_(rec_ids)).all()
        return recommended_products
        
    except Exception as e:
        print(f"Recommendation Engine Error: {e}")
        # Build logic resilient to failure
        return fallback_recommendations(product_id)

def fallback_recommendations(product_id):
    """
    Fallback: Recommend products from the same category OR specific cross-sell items.
    """
    current_product = Product.query.get(product_id)
    if not current_product:
        return []
    
    # 1. Custom Cross-Sell Mapping (FBT Logic)
    cross_sell_map = {
        'Apple MacBook Pro 14-inch': ['Logitech MX Master 3S Mouse', 'Mechanical Gaming Keyboard RGB', 'Sony WH-1000XM5 Headphones'],
        'Samsung Galaxy S24 Ultra': ['Spigen Armor Phone Case', '65W USB-C Fast Charger', 'Sony WH-1000XM5 Headphones'],
        'Embroidered Cotton Kurta Top': ['Silk Blend Leggings', 'Handcrafted Leather Sandals'],
        'Nintendo Switch OLED Model': ['Logitech MX Master 3S Mouse', 'Sony WH-1000XM5 Headphones']
    }
    
    related_names = cross_sell_map.get(current_product.name, [])
    if related_names:
        recs = Product.query.filter(Product.name.in_(related_names)).all()
        if recs: return recs

    # 2. Category Fallback
    return Product.query.filter(
        Product.category == current_product.category, 
        Product.id != product_id
    ).order_by(Product.rating.desc()).limit(3).all()
