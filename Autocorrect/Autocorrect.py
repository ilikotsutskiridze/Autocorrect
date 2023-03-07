import sys
import re


class Autocorrector:
    def __init__(self, array: list) -> None:
        self.__dict = []
        self.__size_dict = int(array.pop(0))
        self.__input_words = []
        self.__2darray = []
        self.__result = []
        # Сложность O(n) поскольку зависит от размера словаря. n - размер словаря
        for i in range(0, self.__size_dict):
            if str(array[0]).lower() not in self.__dict:
                self.__dict.append(str(array.pop(0)).lower())
            else:
                array.pop(0)
        for i in array:
            self.__input_words.append(i)
        del array
        self.calc_distance()

    def __str__(self):
        return "".join([f"{self.create_result()[i]}\n" for i in range(len(self.create_result()))])

    

    def calc_distance(self):
        """
         создаем двумерный массив с количеством строк равным  словам, а столбцов словарю
         затем вычисляем расстояния Дамерау — Левенштейна
         сложность:
            здесь проход по каждому слову и по каждому слову из словаря
            len(список слов) - n, len(список слов из словаря) - k. Сложность O(n*k)
        """
        self.__2darray = [[0 for _ in range(len(self.__dict))] for _ in range(len(self.__input_words))]
        for i in range(len(self.__input_words)):
            temp1 = []
            temp2 = []
            for j in range(len(self.__dict)):
                self.__2darray[i][j] = self.damerau_levenshtein_distance(str(self.__input_words[i]).lower(), str(self.__dict[j]))
                if (int(self.__2darray[i][j]) == 0):
                    temp1.append("ok")
                    self.__result.append(temp1)
                    break
                if (int(self.__2darray[i][j]) == 1):
                    temp2.append(self.__dict[j])
                if (j == len(self.__dict)-1) and (len(temp2) != 0):
                    temp2.sort()
                    self.__result.append(temp2)
                if j == len(self.__dict)-1 and len(temp1) == 0 and len(temp2) == 0:
                    temp1.append("?")
                    self.__result.append(temp1)  

    def create_result(self) -> list:
        """
        возвращает:
            массив с результатом
        сложность:
            цикл работает от длины списка слов
            len(список слов) - n,  Сложность O(n)
        """
        result = []
        for i in range(0, len(self.__input_words)):
            if self.__size_dict != 0:
                if (self.__result[i][0] == "ok"):
                    result.append(str(self.__input_words[i]) + " - ok")
                elif (self.__result[i][0] == "?"):
                    result.append(str(self.__input_words[i]) + " -?")
                elif (self.__result[i][0] != "ok") and (self.__result[i][0] != "?"):
                    result.append(self.__input_words[i] + " -> " + ", ".join(self.__result[i]))
            else:
                result.append(str(self.__input_words[i]) + " -?")
        return result

    def damerau_levenshtein_distance(self, str1: str, str2: str) -> dict:
        """
        принимает:
            два слова: первый из слов второй из словаря
        возвращает:
            расстояние символов между двумя строками
        сложность:
            по скольку функция принимает две строки то оно будет длины первой строки умноженной на длину второй строки
            len(str1) - n, len(str2) - k. Сложность O(n*k)
        """
        distance = {}
        distance_value = 0
        for i in range(-1, len(str1)+1):
            distance[(i, -1)] = i+1
        for i in range(-1, len(str2)+1):
            distance[(-1, i)] = i+1
        for i in range(len(str1)):
            for j in range(len(str2)):
                cost = 0 if str1[i] == str2[j] else 1
                distance[(i, j)] = min(
                                distance[(i-1, j)] + 1,  # удаленние символа
                                distance[(i, j-1)] + 1,  # вставка символа
                                distance[(i-1, j-1)] + cost)  # замена символа
                if i and j and str1[i]==str2[j-1] and str1[i-1] == str2[j]:
                    distance[(i, j)] = min(distance[(i, j)], distance[i-2, j-2] + cost)  # перемещение символа
                if i == len(str1)-1 and j == len(str2)-1:
                    distance_value = distance[(i, j)]
                    del distance
        return distance_value

    


if __name__ == "__main__":
    autocorrector = Autocorrector([str(re.findall(r'.+', line)[0]) for line in sys.stdin if len(re.findall(r'.+', line)) != 0])
    print(autocorrector)

