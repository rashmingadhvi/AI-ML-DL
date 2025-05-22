from typing import List
#[-1, 5, 8, 10, 45, 57], -1
def binsearch(data: List[int], num_to_find: int) -> bool:
	
	endIndex = len(data)
	# if data is empty, return false
	
	startIndex = 0
	# if data is not empty, find the middle index
	middleIndex = int((endIndex + startIndex)/2)
	while endIndex >= startIndex:
		if data[middleIndex] == num_to_find:
			return True
		elif data[middleIndex] < num_to_find:
			startIndex = middleIndex + 1 # 4
			
		else:
			endIndex = middleIndex - 1
			
		middleIndex = int((endIndex + startIndex)/2)
		print(f" MI = {middleIndex} - D = {data[middleIndex]}")
		print(data)
		print("#######")
	return False

print(binsearch([-1, 5, 8, 10, 45, 57], 1))