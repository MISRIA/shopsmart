import sqlite3
import os

db_path = os.path.join('instance', 'shopsmart.db')

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add the column to the order table
        try:
            cursor.execute("ALTER TABLE 'order' ADD COLUMN estimated_delivery DATETIME")
            print("Added estimated_delivery to order table")
        except sqlite3.OperationalError:
            pass
            
        # Add the column to the product table
        try:
            cursor.execute("ALTER TABLE 'product' ADD COLUMN is_fast_delivery BOOLEAN DEFAULT 0")
            print("Added is_fast_delivery to product table")
        except sqlite3.OperationalError:
            pass
            
        # Update existing records where it is NULL
        cursor.execute("UPDATE 'order' SET estimated_delivery = datetime(created_at, '+5 days') WHERE estimated_delivery IS NULL")
        
        conn.commit()
        conn.close()
        print("Success: Column 'estimated_delivery' added to 'order' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Notice: Column 'estimated_delivery' already exists.")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
else:
    print(f"Error: Database not found at {db_path}. Please make sure you are in the correct directory.")
