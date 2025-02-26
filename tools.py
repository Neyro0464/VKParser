from datetime import datetime
import time

def input_dates(start_date_str, end_date_str):
   while True:
        try:
            # Запрашиваем у пользователя ввод дат
            if (start_date_str == '' and end_date_str == ''):
                start_date_str = input("Введите дату начала в формате dd.mm.yyyy: ")
                end_date_str = input("Введите дату конца в формате dd.mm.yyyy: ")

            # Преобразуем строки в объекты datetime.datetime
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y")

            # Получаем текущую дату и время
            now = datetime.now()

            # Проверяем, что дата начала не позже даты окончания
            if start_date > end_date:
                print("Ошибка: Дата начала не может быть позже даты окончания.")
                continue  # Повторяем запрос

            # Проверяем, что дата окончания не позже текущей даты и времени
            if end_date > now:
                print("Ошибка: Дата окончания не может быть позже текущей даты и времени.")
                continue  # Повторяем запрос

            return start_date, end_date

        except ValueError:
            print("Ошибка: Некорректный формат даты или дата не существует. Попробуйте снова.")


def timer(flag, start, end):
    # Засекаем начальное время
    if (flag == 0):
        start_time = time.time()
        return start_time

    # Засекаем конечное время
    elif(flag == 1):
        end_time = time.time()
        return end_time

    # Вычисляем время выполнения
    else:
        elapsed_time = end - start
        print(f"Время выполнения: {elapsed_time:.6f} секунд")