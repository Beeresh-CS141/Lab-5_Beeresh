"""
Inventory Management System

This module provides a class-based inventory system with functionalities
to add, remove, check, save, and load items. Logging and safe operations
are implemented to ensure code quality and security.
"""

import json
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Inventory:
    """Class to manage inventory items."""

    def __init__(self, file_path: str = "inventory.json") -> None:
        """
        Initialize the inventory and load data from JSON file.

        Args:
            file_path (str): Path to the JSON file for storing
                inventory data.
        """
        self.stock_data: Dict[str, int] = {}
        self.file_path: str = file_path
        self.load_data()

    def add_item(self, item: str, qty: int) -> None:
        """
        Add a quantity of an item to the inventory.

        Args:
            item (str): Name of the item.
            qty (int): Quantity to add.
        """
        if not isinstance(item, str) or not isinstance(qty, int):
            logging.warning("Invalid item name or quantity type.")
            return

        if qty < 0:
            logging.warning("Cannot add negative quantity: %d", qty)
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        logging.info("Added %d of %s", qty, item)

    def remove_item(self, item: str, qty: int) -> None:
        """
        Remove a quantity of an item from the inventory.

        Args:
            item (str): Name of the item.
            qty (int): Quantity to remove.
        """
        if not isinstance(item, str) or not isinstance(qty, int):
            logging.warning("Invalid item name or quantity type.")
            return

        if item not in self.stock_data:
            logging.warning("Tried to remove non-existent item: %s", item)
            return

        if qty < 0:
            logging.warning("Cannot remove negative quantity: %d", qty)
            return

        self.stock_data[item] -= qty

        if self.stock_data[item] <= 0:
            del self.stock_data[item]
            logging.info("Removed %s completely from stock.", item)
        else:
            logging.info("Removed %d of %s", qty, item)

    def get_qty(self, item: str) -> int:
        """
        Return the quantity of a given item.

        Args:
            item (str): Name of the item.

        Returns:
            int: Quantity of the item (0 if not present).
        """
        return self.stock_data.get(item, 0)

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """
        Return a list of items with quantity below the given threshold.

        Args:
            threshold (int): Minimum quantity to avoid low stock.

        Returns:
            List[str]: List of item names below threshold.
        """
        return [
            item for item, qty in self.stock_data.items()
            if qty < threshold
        ]

    def save_data(self) -> None:
        """Save the current inventory to a JSON file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(self.stock_data, file, indent=4)
            logging.info("Inventory data saved successfully.")
        except OSError as error:
            logging.error("Error saving inventory data: %s", error)

    def load_data(self) -> None:
        """Load inventory data from a JSON file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.stock_data = json.load(file)
            logging.info("Inventory data loaded successfully.")
        except FileNotFoundError:
            logging.warning(
                "File %s not found. Starting fresh.",
                self.file_path,
            )
            self.stock_data = {}
        except json.JSONDecodeError:
            logging.error("Error decoding JSON file. Starting fresh.")
            self.stock_data = {}

    def print_data(self) -> None:
        """Print the inventory report."""
        if not self.stock_data:
            print("Inventory is empty.")
        else:
            print("Inventory Report:")
            for item, qty in sorted(self.stock_data.items()):
                print(f"{item} -> {qty}")


def main() -> None:
    """Main function to demonstrate inventory operations."""
    inventory = Inventory()

    inventory.add_item("apple", 10)
    inventory.add_item("banana", 2)
    inventory.add_item("orange", 6)

    inventory.remove_item("apple", 3)
    inventory.remove_item("orange", 10)

    print(f"Apple stock: {inventory.get_qty('apple')}")
    print(f"Low items: {inventory.check_low_items()}")

    inventory.save_data()
    inventory.load_data()
    inventory.print_data()


if __name__ == "__main__":
    main()
