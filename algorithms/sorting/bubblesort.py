def bubble_sort(arr, callback=None):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if callback:
                callback(arr, j, j + 1)  # 콜백 호출: 현재 비교하는 인덱스
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    if callback:
        callback(arr, None, None)  # 정렬 완료 후 콜백 호출
    return arr
