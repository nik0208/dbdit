from django import forms
from .models import *
import re
import logging
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)


class ApplForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = Applications
        fields = '__all__'


    def clean(self):


        cleaned_data = super().clean()
        content = cleaned_data.get('content')

        lines = content.split('\n')

    

        if "Заявка на организацию рабочего места" in lines[0]:	

            cleaned_data['num'] = re.search(r'Заявка на организацию рабочего места №(.*)', content).group(1)
            cleaned_data['avtor'] = re.search(r'Автор: \((.*?)\) (\w+ \w+)', content).group(2)
            cleaned_data['user'] = re.search(r'Фамилия: (.*?)\nИмя: (.*?)\nОтчество:', content, re.DOTALL).group(0).strip()
            cleaned_data['requested_equipment'] = re.search(r'Необходимое оборудование:(.*?)============================================================', content, re.DOTALL).group(1).strip()
            cleaned_data['department'] = re.search(r'Подразделение: (.*)', content).group(1)
            
            logging.debug(f"deadline: {cleaned_data['deadline']}")
            date_str = re.search(r'Дата выхода: (.*)', content).group(1)
            try:
                parsed_date = datetime.strptime(date_str, '%d.%m.%Y')  # Предполагается, что исходный формат даты: дд.мм.гггг
                formatted_date = parsed_date.strftime('%Y/%m/%d')
                cleaned_data['deadline'] = formatted_date
            except Exception as e:
                logging.debug(f"Error while parsing date: {e}")
        else:

            cleaned_data['num'] = re.search(r'Заявка на ИТ оборудование №(.*)', content).group(1)
            cleaned_data['avtor'] = re.search(r'Автор: \((.*?)\) (\w+ \w+)', content).group(2)
            cleaned_data['user'] = re.search(r'Для кого закуп: \((.*?)\) (\w+ \w+)', content).group(2)
            cleaned_data['requested_equipment'] = re.search(r'Необходимое оборудование:(.*?)Обоснование:(.*)', content, re.DOTALL).group(1).strip()
            cleaned_data['department'] = re.search(r'Подразделение: (.*)', content).group(1)

        return cleaned_data