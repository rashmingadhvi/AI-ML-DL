def bubblesort(arr):
    """
    Perform bubble sort on a list.

    :param arr: List of elements to be sorted
    :return: Sorted list
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j]> arr[j+1]:
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp

    return arr

print(bubblesort([64, 34, 25, 12, 22, 11, 90]))

