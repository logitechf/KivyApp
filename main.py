from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from collections import Counter
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.selectioncontrol import MDCheckbox


class TextProcessorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        #Чекбоксы для "С ъ" и "Без ъ"
        checkboxes_layout = BoxLayout(size_hint=(1, 0.6))
        self.with_x_checkbox = MDCheckbox(active=True, size_hint=(0.6, 1))
        self.without_x_checkbox = MDCheckbox(size_hint=(0.6, 1))
        checkboxes_layout.add_widget(MDLabel(text='С ъ'))
        checkboxes_layout.add_widget(self.with_x_checkbox)
        checkboxes_layout.add_widget(MDLabel(text='Без ъ'))
        checkboxes_layout.add_widget(self.without_x_checkbox)
        layout.add_widget(checkboxes_layout)

        #Поле ввода текста
        self.input_text = MDTextField(multiline=True, hint_text='Введите текст', size_hint=(1, 3))
        layout.add_widget(self.input_text)

        #Кнопки "Разделить" и "Обработать"
        action_buttons_layout = BoxLayout(size_hint=(None, None), size=(200, 100),
                                          orientation='horizontal',
                                          pos_hint={'center_x': 0.5})

        process_button = MDRaisedButton(text='Обработать', size_hint=(None, None), size=(200, 50))
        process_button.bind(on_press=self.process_text)

        action_buttons_layout.add_widget(process_button)
        layout.add_widget(action_buttons_layout)

        #ScrollView для прокручиваемого элемента
        scrollview = ScrollView(size_hint=(2, 1.5), pos_hint={'x': 0.2})
        self.empty_label = MDLabel(text='', size_hint=(None, None), size=(200, 200))

        scrollview.add_widget(self.empty_label)
        layout.add_widget(scrollview)

        self.empty_label2 = MDLabel(text='', size_hint=(1, 1), pos_hint={'x': 0.2})
        layout.add_widget(self.empty_label2)

        scrollview2 = ScrollView(size_hint=(2, 1.5), pos_hint={'x': 0.2})
        self.empty_label3 = MDLabel(text='', size_hint=(None, None), size=(200, 200))
        scrollview2.add_widget(self.empty_label3)
        layout.add_widget(scrollview2)

        return layout

    def process_text(self, instance):
        input_text = self.input_text.text
        result_text = ""

        # Проверка состояния чекбоксов
        if self.with_x_checkbox.active:
            for char in input_text:
                if char.isalnum() or char.isspace():
                    result_text += char

            #обработка съ
            result_lst = "".join([i + "ъ" if i[-1] not in "аиеёоуыэюяйъь" else i for i in result_text.split()])

            result_str = ""

            for i in result_lst:
                if i.isalpha():
                    result_str += i

        elif self.without_x_checkbox.active:
            for char in input_text:
                if char.isalnum() or char.isspace():
                    result_text += char

            result_str = ""

            for i in result_text:
                if i.isalpha():
                    result_str += i

        # Обработка результатов и вывод
        counts = Counter(result_str.lower())

        result = []
        sum_count = 0
        multiplied_count = 0

        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        for index, (char, count) in enumerate(sorted_counts, start=1):
            sum_count += count
            multiplied_count += index * count
            result.append(f"{char} - {count} - {index * count}\n")

        result_str2 = ''.join(result)

        self.empty_label.text = result_str2
        self.empty_label2.text = f"{sum_count} | {multiplied_count}"
        self.empty_label3.text = result_str.lower()


if __name__ == "__main__":
    app = TextProcessorApp()
    app.run()
