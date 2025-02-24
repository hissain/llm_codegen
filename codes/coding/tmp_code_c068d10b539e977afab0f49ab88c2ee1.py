def binary_search(list, target):
  low = 0
  high = len(list) - 1

  while low <= high:
    mid = (low + high) // 2
    guess = list[mid]
    if guess == target:
      return mid
    if guess > target:
      high = mid - 1
    else:
      low = mid + 1
  return None

# Example usage:
my_list = [2, 5, 7, 8, 11, 12]
target = 13
result = binary_search(my_list, target)

if result is not None:
  print(f"Target {target} found at index {result}")
else:
  print(f"Target {target} not found in the list")