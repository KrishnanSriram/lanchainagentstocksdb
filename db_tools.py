from sys import exception
from langchain.tools import tool
from dbops import add_stock, update_stock, list_stocks, delete_stock

@tool
def add_stock_tool(input:str)->str:
    """Adds a stock to watchlist: with input in format 'SYMBOL:PRICE:QTY'. Extract only the symbol, price and quantity there should not be any other text to input. Also ensure these fields are separated by : and no other characters"""
    try:
        symbol, strprice, strquantity = input.split(':')
        strprice = strprice.replace('$', '')
        price = float(strprice)
        quantity = int(strquantity)
        # Validate all of these parmeters and invoke db ops
        add_stock(symbol=symbol, price=price, quantity=quantity)
        return f"Successfully ADDED stock information to watchlist - {symbol}"
    except exception as e:
        return f"ERROR: Failed to ADD stock to Watchlist - {str(e)}"



@tool
def list_stock_tool(input:str)->str:
    """List all stocks we track from database"""
    try:
        stocks = list_stocks()
        return  stocks
    except exception as e:
        return f"ERROR: Failed to RETRIEVE stocks from Watchlist - {str(e)}"



@tool
def update_stock_tool(input:str)->str:
    """Update stock to the watchlist: input must be 'SYMBOL:PRICE:QTY'."""
    try:
        symbol, strprice, strquantity = input.split(':')
        price = float(strprice)
        quantity = int(strquantity)
        # Validate all of these parmeters and invoke db ops
        update_stock(symbol=symbol, price=price, quantity=quantity)
        return f"Successfully UPDATED stock information to watchlist - {symbol}"
    except exception as e:
        return f"ERROR: Failed to UPDATE Watchlist - {str(e)}"


@tool
def delete_stock_tool(input:str)->str:
    """Delete a stock from watchlist: input must be 'SYMBOL'."""
    try:
        symbol = input # Assuming, we don't need to do any gimmicks to get the symbol information
        delete_stock(symbol=symbol)
    except exception as e:
        return f"ERROR: Failed to DELETE stock in watchlist - {str(e)}"
