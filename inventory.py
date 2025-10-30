"""Inventory management module for tracking stock items."""

import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item to the inventory.
    
    Args:
        item: The item name (default: "default")
        qty: The quantity to add (default: 0)
        logs: Optional list to append log messages to
    """
    if logs is None:
        logs = []
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove an item from the inventory.
    
    Args:
        item: The item name
        qty: The quantity to remove
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logger.warning("Item '%s' not found in inventory", item)


def get_qty(item):
    """Get the quantity of an item.
    
    Args:
        item: The item name
        
    Returns:
        The quantity of the item, or 0 if not found
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file.
    
    Args:
        file: The file path (default: "inventory.json")
    """
    global stock_data  # pylint: disable=global-statement
    with open(file, "r", encoding="utf-8") as f:
        stock_data = json.loads(f.read())


def save_data(file="inventory.json"):
    """Save inventory data to a JSON file.
    
    Args:
        file: The file path (default: "inventory.json")
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data))


def print_data():
    """Print the current inventory data."""
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])


def check_low_items(threshold=5):
    """Check for items below a threshold quantity.
    
    Args:
        threshold: The minimum quantity threshold (default: 5)
        
    Returns:
        A list of item names below the threshold
    """
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result


def main():
    """Main function to demonstrate inventory operations."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    # Using print directly instead of eval for security
    print('eval used')


main()
