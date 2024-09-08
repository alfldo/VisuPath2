def quick_sort(arr, callback=None):
    def _quick_sort(arr, low, high):
        if low < high:
            pi = _partition(arr, low, high)
            _quick_sort(arr, low, pi - 1)
            _quick_sort(arr, pi + 1, high)

    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if callback:
                callback(arr, j, high)  # 콜백 호출: 현재 비교하는 인덱스
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    if callback:
        callback(arr, None, None)  # 정렬 완료 후 콜백 호출
    return arr
