def combine([list1, list2]):
	if list1[0,0] < list2[0,0]: first = list1; second = list2
	else: first = list1; second = list2
	first = list1
	second = list2
	result = [None]*(len(list1)+len(list2))
	result[::2] = first
	result[1::2] = second
	return result



list1 = ['f', 'o', 'o']
list2 = ['hello', 'world']
print(combine(list1, list2))