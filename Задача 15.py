"""
Написать программу, которая получает на вход имена двух bed файлов и
возвращает bed файл, содержащий результат пересечения интервалов из двух
входных файлов.
"""

def load_bed_file(file_path): #Загружает bed файл и возвращает список кортежей с координатами.
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            chromosome = parts[0]
            start = int(parts[1])
            end = int(parts[2])
            data.append((chromosome, start, end))
    return data

def intersect_bed_files(file1, file2):
    """Выполняет пересечение интервалов из двух bed файлов."""
    bed1 = load_bed_file(file1)
    bed2 = load_bed_file(file2)
    intersected = []

    for interval1 in bed1:
        for interval2 in bed2:
            if interval1[0] == interval2[0]:  # Проверка, что интервалы находятся на одном хромосоме
                start = max(interval1[1], interval2[1])  # Начало пересечения
                end = min(interval1[2], interval2[2])  # Конец пересечения
                if start < end:  # Проверка, что пересечение не пустое
                    intersected.append((interval1[0], start, end))

    return intersected

def write_bed_file(file_path, data): #Записывает результат пересечения в bed файл.
    with open(file_path, 'w') as file:
        for interval in data:
            file.write('\t'.join(map(str, interval)) + '\n')

# Пути к двум bed файлам
bed_file1 = '/content/chr1.bed'
bed_file2 = '/content/chr2.bed'


intersected_intervals = intersect_bed_files(bed_file1, bed_file2)

# Запись результата в новый bed файл
output_file = '/content/путь_к_результирующему_bed_файлу.bed'
write_bed_file(output_file, intersected_intervals)