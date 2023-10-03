import os
import pandas as pd


data = pd.read_excel('Склады.xlsx')

# Сохранение данных в CSV-файл
data.to_csv('Склады.csv', index=False)
