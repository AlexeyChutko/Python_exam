"""
Для набора таблиц дифференциальной экспрессии генов, в которых есть
колонки-идентификаторы генов Q-value и LogFoldChange. Считать, что ген
значимо изменил уровень экспрессии, если Q-value у него меньше 0.05 и
логарифм изменения по модулю больше единицы. Нужно составить сводную
таблицу, где есть список идентификаторов генов, дальше количество
экспериментов, в которых уровень экспрессии генов повысился, и дальше
количество экспериментов, где уровень экспрессии генов понизился.
Отсортировать их в таком порядке, что в начале идут все гены, в которых
уровень экспрессии повысился, потом через незначимые изменения
экспрессии до генов, в которых во всех экспериментах уровень экспрессии
понизился.
"""
import os
import csv
from collections import defaultdict

def read_csv_files(directory):
    all_data = defaultdict(list)  # Словарь для хранения данных из всех файлов
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r', newline='') as file: #Открытие файла для чтения
                csv_reader = csv.reader(file)
                next(csv_reader)  # Пропуск заголовока
                for row in csv_reader:
                    gene_id, q_value, log_fold_change = row[0].split(';')  # Деление строк на компоненты
                    all_data[gene_id.strip()].append((float(q_value.strip()), float(log_fold_change.strip())))  # Добавление данных в словарь
    return all_data

def create_summary_table(all_data):
    summary_table = {}  # Пустой словарь для сводной таблицы
    for gene_id, experiments in all_data.items():
        increased = 0  # Эксперименты с повышением уровня экспрессии
        decreased = 0  # Эксперименты с понижением уровня экспрессии
        for q_value, log_fold_change in experiments:
            if log_fold_change > 0:
                increased += 1
            elif log_fold_change < 0:
                decreased += 1
        summary_table[gene_id] = (increased, decreased)
    return summary_table

def print_summary_table(summary_table):
    print("Gene ID\tIncreased\tDecreased")
    for gene_id, (increased, decreased) in summary_table.items():
        print(f"{gene_id}\t{increased}\t{decreased}")

def print_sorted_table(summary_table):
    sorted_table = sorted(summary_table.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
    print("Gene ID\tIncreased\tDecreased")
    for gene_id, (increased, decreased) in sorted_table:
        print(f"{gene_id}\t{increased}\t{decreased}")

# Путь к директории с файлами CSV
directory_path = '/content/exm'

#Чтение данных из всех файлов CSV в указанной директории
all_data = read_csv_files(directory_path)

# Создание и вывод сводной таблицы
summary_table = create_summary_table(all_data)

print_summary_table(summary_table)

# Создание и вывод отсортированной таблицы
print("\nОтсортированная таблица:")
print_sorted_table(summary_table)