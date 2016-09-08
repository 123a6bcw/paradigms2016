# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    lst1 = []
    for i in range (len(lst) - 1):
        if lst[i] != lst[i + 1]:
            lst1.append(lst[i])
    lst1.append(lst[-1])
    return lst1

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    i = 0
    j = 0
    lst3 = []
    while i < len(lst1) and j < len(lst2):
        if (lst1[i] < lst2[j]):
            lst3.append(lst1[i])
            i += 1
        else:
            lst3.append(lst2[j])
            j += 1
    lst3.extend(lst1[i:])
    lst3.extend(lst2[j:])
    return lst3

