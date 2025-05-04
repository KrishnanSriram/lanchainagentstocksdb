from sys import exception
from langchain.tools import tool
import requests
import json
import os
import time


def should_use_local_data(local_file_path: str, cache_duration_seconds: int = 360) -> bool:
    try:
        if os.path.exists(local_file_path):
            file_modified_time = os.path.getmtime(local_file_path)
            current_time = time.time()
            if current_time - file_modified_time < cache_duration_seconds:
                print(f"Use LOCAL cached data from: {local_file_path}")
                return True
    except FileNotFoundError:
        print(f"Error: Local file not found at {local_file_path}")
    print(f"Local data does not exist or need to be refreshed.")
    return False

def get_data_from_remote(url: str, local_file_path: str) -> bool:
    print("Download this data locally.....")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        json_content = response.json()
        with open(local_file_path, 'w') as f:
            json.dump(json_content, f, indent=4)
    except requests.exceptions.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return False
    except IOError as e:
        print(f"Error writing to local file: {e}")
        return False
    return True


def get_stock_symbol_from_local(local_file_path: str, company_name: str) -> str:
    print(f"Company name - {company_name}")
    response = {}
    try:
        with open(local_file_path, 'r') as f:
            response = json.load(f)
    except IOError as e:
        print(f"Error reading from local file: {e}")
        exit()

    results = response.get("quotes", [])
    print(f"Results - {str(results)}")
    for result in results:
        symbol = result.get("symbol", "")
        if len(symbol) == 4 and result.get("exchange") in ["NYQ", "NMS"]:
            return f"{company_name} → {symbol}"
    return f"No 4-letter US stock symbol found for {company_name}"


@tool
def get_stock_symbol(company_name: str) -> str:
    """Give a company name, return a 4 letter symbol for the company from NASDAQ oe US Stock exchange listing"""
    local_file_path = "finance.json"
    print(f"Company name - {company_name}")
    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}&lang=en-US"
    if not should_use_local_data(local_file_path="finance.json"):
        get_data_from_remote(url=url, local_file_path=local_file_path)
    print("Look into local file for company info.....")
    return get_stock_symbol_from_local(local_file_path=local_file_path, company_name=company_name)

# if __name__ == "__main__":
#     company_name = "Oracle"
#     local_file_path = "finance.json"
#     print(f"Company name - {company_name}")
#     url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}&lang=en-US"
#     if not should_use_local_data(local_file_path="finance.json"):
#         get_data_from_remote(url=url, local_file_path=local_file_path)
#     print("Look into local file for company info.....")
#     print(get_stock_symbol(local_file_path=local_file_path, company_name=company_name))