from directories.models import IT_OS
from datetime import datetime
import csv

def load_data_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропустить заголовок

        for row in reader:
            inv_dit = row[0]

            if IT_OS.objects.filter(inv_dit=inv_dit).exists():
                continue  # Пропустить текущую строку, если запись уже существует

            name_os = row[1]
            inpute_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            os_group = row[3]
            original_price = float(row[4])
            serial_number = row[5]

            IT_OS.objects.get_or_create(
                inv_dit=inv_dit,
                defaults={
                    'name_os': name_os,
                    'inpute_date': inpute_date,
                    'os_group': os_group,
                    'original_price': original_price,
                    'serial_number': serial_number
                }
            )

# Замените 'C:/Users/user/Downloads/excel_file — копия.csv' на путь к вашему файлу CSV
file_path = 'C:/Users/user/Downloads/excel_file — копия.csv'
load_data_from_csv(file_path)
