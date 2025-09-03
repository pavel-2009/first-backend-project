class MaxHeap:
    def __init__(self):
        # Инициализация пустой кучи
        self.heap = []

    def insert(self, val):
        """
        Вставка нового элемента в кучу.
        1. Добавляем элемент в конец массива.
        2. Восстанавливаем свойство кучи с помощью sift-up.
        """
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        """
        Извлечение максимального элемента (корня).
        1. Сохраняем корень.
        2. Перемещаем последний элемент в корень.
        3. Удаляем последний элемент.
        4. Восстанавливаем свойство кучи с помощью sift-down.
        """
        if not self.heap:
            return None  # Куча пуста
        max_val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return max_val

    def _sift_up(self, idx):
        """
        Восстановление свойства кучи снизу вверх.
        Пока родитель меньше текущего элемента — меняем их местами.
        """
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] > self.heap[parent]:
            # Меняем местами с родителем
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx):
        """
        Восстановление свойства кучи сверху вниз.
        Находим большего из потомков и меняем местами с ним, если он больше текущего.
        """
        n = len(self.heap)
        while True:
            left = 2 * idx + 1  # Индекс левого потомка
            right = 2 * idx + 2 # Индекс правого потомка
            largest = idx       # Индекс наибольшего элемента
            # Проверяем левый потомок
            if left < n and self.heap[left] > self.heap[largest]:
                largest = left
            # Проверяем правый потомок
            if right < n and self.heap[right] > self.heap[largest]:
                largest = right
            # Если текущий элемент больше обоих потомков — завершаем
            if largest == idx:
                break
            # Меняем местами с наибольшим потомком
            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            idx = largest

# Пример использования:
if __name__ == "__main__":
    heap = MaxHeap()
    heap.insert(10)
    heap.insert(20)
    heap.insert(5)
    heap.insert(30)
    print("Куча:", heap.heap)
    print("Максимум:", heap.extract_max())
    print("Куча после извлечения максимума:", heap.heap)
