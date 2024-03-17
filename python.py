from PySide6.QtWidgets import QApplication, QTextEdit, QHBoxLayout, QVBoxLayout, QWidget, QListView, QLabel
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QListWidgetItem

from PySide6.QtGui import QStandardItemModel, QStandardItem

from deep_translator import GoogleTranslator
import wikipedia
from wikipedia.exceptions import PageError



import random


def wiki_description(query):
    try:
        summary = wikipedia.summary(query, sentences=1, auto_suggest=True)
        return (summary)
    except wikipedia.exceptions.DisambiguationError as e:
        # print(e.options)
        query = e.options[0]
    except Exception:
        return (query + " has no description")

    return (query + " has no description")


def translate_query(query):
    translated = GoogleTranslator(source='auto', target='ru').translate(query)
    return (translated)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a horizontal layout for the pairs of label and ListView
        self.main_layout = QHBoxLayout()

        self.label_input = QLabel("input")
        self.text_edit = QTextEdit()

        self.layout_input = QVBoxLayout()
        self.layout_input.addWidget(self.label_input)
        self.layout_input.addWidget(self.text_edit)
        self.main_layout.addLayout(self.layout_input)

        self.Process_button = QPushButton("Process Text")
        self.Process_button.setMinimumSize(100, 200)  # Set the size to make it wide and tall
        self.main_layout.addWidget(self.Process_button)
        self.Process_button.clicked.connect(lambda: process_text(self))

        # Create the first pair of label and ListView
        self.label_desription = QLabel("list_widget_desription")
        self.list_widget_desription = QListView()

        # Create the second pair of label and ListView
        self.label_translation = QLabel("list_widget_translation")
        self.list_widget_translation = QListView()

        # Create vertical layouts for each pair and add them to the main layout
        self.layout_desription = QVBoxLayout()
        self.layout_desription.addWidget(self.label_desription)
        self.layout_desription.addWidget(self.list_widget_desription)
        self.main_layout.addLayout(self.layout_desription)

        self.layout_translation = QVBoxLayout()
        self.layout_translation.addWidget(self.label_translation)
        self.layout_translation.addWidget(self.list_widget_translation)
        self.main_layout.addLayout(self.layout_translation)

        # Set the main layout to the central widget
        self.central_widget.setLayout(self.main_layout)

    def populate_list_view(self, list_view, items):
        model = QStandardItemModel()
        list_view.setModel(model)
        for item in items:
            standard_item = QStandardItem(item)
            model.appendRow(standard_item)

def process_text(window):
    # Get the text from the multiline input
    text = window.text_edit.toPlainText()

    text_Array = text.split()

    # Clear the list
    model_desription = QStandardItemModel()
    window.list_widget_desription.setModel(model_desription)

    model_translation = QStandardItemModel()
    window.list_widget_translation.setModel(model_translation)


    with open('description.txt', 'w+', encoding='utf-8') as file:
        for word in text_Array:
            description = wiki_description(word)
            item = QStandardItem(description)
            model_desription.appendRow(item)

            file.write(f"{description}\n")

    with open('translation.txt', 'w+', encoding='utf-8') as file:
        for word in text_Array:
            try:
                translation = translate_query(word)
            except:
                translation = word + ' no translation'

            item = QStandardItem(translation)
            model_translation.appendRow(item)
            file.write(f"{translation}\n")



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
