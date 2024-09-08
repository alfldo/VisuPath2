def merge_sort(arr, callback=None):
    def _merge_sort(arr, l, r):
        if l < r:
            m = (l + r) // 2
            _merge_sort(arr, l, m)
            _merge_sort(arr, m + 1, r)
            _merge(arr, l, m, r)

    def _merge(arr, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = arr[l:l + n1]
        R = arr[m + 1:m + 1 + n2]
        i = j = 0
        k = l
        while i < n1 and j < n2:
            if callback:
                callback(arr, l + i, m + 1 + j)  # 콜백 호출: 현재 비교하는 인덱스
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    _merge_sort(arr, 0, len(arr) - 1)
    if callback:
        callback(arr, None, None)  # 정렬 완료 후 콜백 호출
    return arr
