##### ДЗ Тема 9. Асинхронне програмування, Тема 10. Вступ до паралельних обчислень


##### Тема 10. Вступ до паралельних обчислень

### Завдання 2

'''
Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси, 
аналізує частоту використання слів у тексті за допомогою парадигми MapReduce 
і візуалізує топ-слова з найвищою частотою використання у тексті.

Покрокова інструкція

1. Імпортуйте необхідні модулі (matplotlib та інші).
2. Візьміть код реалізації MapReduce з конспекту.
3. Створіть функцію visualize_top_words для візуалізації результатів.
4. У головному блоці коду отримайте текст за URL, застосуйте MapReduce та візуалізуйте результати.
👉🏼 Наприклад, для топ 10 найчастіше вживаних слів побудова графіка може виглядати так:

Критерії прийняття

- Код завантажує текст із заданої URL-адреси.
- Код виконує аналіз частоти слів із використанням MapReduce.
- Візуалізація відображає топ-слова за частотою використання.
- Код використовує багатопотоковість.
- Код читабельний та відповідає стандартам PEP 8.
'''

import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
import requests


def get_text(url):
    #TODO Додати обробку помилок
    try: 
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP - response.raise_for_status(): Цей метод перевіряє статус-код у відповіді. - Якщо статус-код вказує на успіх (наприклад, 200 OK), то метод нічого не робить, і виконання переходить до наступного рядка. - Якщо статус-код вказує на помилку (наприклад, 404 Not Found або 500 Internal Server Error), то цей метод викликає виняток requests.HTTPError. Цей виняток буде перехоплений блоком except, і функція поверне None.
        return response.text
    except requests.RequestException as e:
        print(f'- Error of access to url: {e}')



# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

#TODO Дописати функцію reduce_function
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
def map_reduce(text, search_words=None):
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Крок 1: Виконати паралельний маппінг використавши ThreadPoolExecutor()
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Крок 3: Виконати паралельну редукцію використавши ThreadPoolExecutor()
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(result, top_n=10):
    # Визначення топ-N найчастіше використовуваних слів
    top_words = Counter(result).most_common(top_n)  # Список відсортований за кількістю у порядку спадання (від найбільшої до найменшої). Аргумент top_n (за замовчуванням 10) вказує, скільки елементів потрібно повернути. Результат: Змінній top_words присвоюється список, наприклад: [('слово_А', 50), ('слово_Б', 45), ('слово_В', 30), ...]

    # Розділення даних на слова та їх частоти
    words, counts = zip(*top_words)                 # zip повертає ітератор, який після розпакування на дві змінні створює: words = ('слово_А', 'слово_Б', 'слово_В', ...); counts = (50, 45, 30, ...)

    # Створення графіка
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top {} Most Frequent Words'.format(top_n))
    plt.gca().invert_yaxis()  # Перевернути графік, щоб найбільші значення були зверху
    plt.show()



if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    # Виконання MapReduce на вхідному тексті
    result = map_reduce(text)
    visualize_top_words(result)

    # Для перевірки на умову виконання PEP8 рекомендую використати pycodestyle
    # Приклад застосування "pycodestyle --show-source --show-pep8 goit-cs-hw-051.py"





