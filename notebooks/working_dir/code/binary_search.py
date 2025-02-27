
import os

def binary_search(sorted_list, target):
    """
    Performs a binary search on a sorted list.

    Args:
        sorted_list: A sorted list of numbers.
        target: The number to search for.

    Returns:
        The index of the target if found, otherwise -1.  Raises TypeError if input is invalid.
    """
    if not isinstance(sorted_list, list):
        raise TypeError("sorted_list must be a list")
    if not all(isinstance(item, (int, float)) for item in sorted_list):
        raise TypeError("sorted_list must contain only numbers")
    if not isinstance(target, (int, float)):
        raise TypeError("target must be a number")

    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2  # Integer division

        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1  # Target not found
