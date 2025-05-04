import os
import psycopg2
from pydantic import BaseModel


class WatchEntry(BaseModel):
    symbol: str
    threshold_price: float
    quantity: int

def db_connection():
  conn = psycopg2.connect(
      host=os.getenv("HOST"),
      database=os.getenv("DATABASE"),
      user=os.getenv("DB_USER"),
      password=os.getenv("PASSWORD")
    )
  return conn


def add_stock(symbol: str, price: float, quantity: int)->str:
    print(f"Add stock - Buy {quantity} of {symbol} at price ${price}")
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO watchlist (symbol, threshold_price, quantity) VALUES (%s, %s, %s) ON CONFLICT (symbol) DO NOTHING",
            (symbol, price, quantity))
        conn.commit()
        conn.close()
        return f"Added {symbol}"
    except Exception as e:
        return f"ERROR: Failed to add Stock into WatchList DB - {str(e)}"

def list_stocks():
    print("List all stocks")
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, threshold_price, quantity FROM watchlist")
    results = cursor.fetchall()
    conn.close()
    return [{"symbol": r[0], "threshold_price": r[1], "quantity": r[2]} for r in results]

def delete_stock(symbol: str)->str:
    print(f"Delete stock {symbol}")
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watchlist WHERE symbol=%s", (symbol,))
        conn.commit()
        conn.close()
        return f"Deleted {symbol}"
    except Exception as e:
        return f"Error: {str(e)}"


def update_stock(symbol: str, price: float, quantity: int)->str:
    print(f"Update stock {symbol} to ${price} for {quantity}")
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE watchlist SET threshold_price=%s, quantity=%s WHERE symbol=%s",
                       (price, quantity, symbol))
        conn.commit()
        conn.close()
        return f"Updated {symbol}"
    except Exception as e:
        return f"ERROR: Failed to {str(e)}"