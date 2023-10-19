import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

kivy.require('2.0.0')

class KpiApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {
            'Datum': pd.date_range(start="2023-01-01", periods=30, freq='D'),
            'Gesamtlieferungen': np.random.randint(50, 200, 30),
            'Produktretouren': np.random.randint(0, 50, 30),
            'DefekteProdukte': np.random.randint(0, 10, 30)
        }

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.label = Label(text="KPI Dashboard", size_hint_y=None, height=44)
        
        # Eingabefeld hinzufügen, um Daten zu bearbeiten
        self.last_data_input = TextInput(hint_text=str(self.data['Gesamtlieferungen'][-1]), size_hint_y=None, height=44)
        layout.add_widget(Label(text="Letzte Daten von Gesamtlieferungen bearbeiten:", size_hint_y=None, height=44))
        layout.add_widget(self.last_data_input)
        
        btn = Button(text="Visualisierung anzeigen", size_hint_y=None, height=44)
        btn.bind(on_press=self.show_plot)
        
        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def show_plot(self, instance):
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        
        # Liniendiagramm
        axs[0].plot(self.data['Datum'], self.data['Gesamtlieferungen'], label="Gesamtlieferungen")
        axs[0].set_title("Liniendiagramm")
        axs[0].legend()
        
        # Balkendiagramm
        bar_width = 0.35
        index = np.arange(len(self.data['Datum']))
        bar1 = axs[1].bar(index, self.data['Gesamtlieferungen'], bar_width, label="Gesamtlieferungen")
        bar2 = axs[1].bar(index + bar_width, self.data['Produktretouren'], bar_width, label="Produktretouren")
        axs[1].set_title("Balkendiagramm")
        axs[1].set_xticks(index + bar_width / 2)
        axs[1].set_xticklabels(self.data['Datum'].strftime('%Y-%m-%d'), rotation=45)
        axs[1].legend()

        # Kreisdiagramm
        total = sum(self.data['Gesamtlieferungen'])
        percentages = [sum(self.data['Gesamtlieferungen'])/total, sum(self.data['Produktretouren'])/total, sum(self.data['DefekteProdukte'])/total]
        labels = ["Gesamtlieferungen", "Produktretouren", "DefekteProdukte"]
        axs[2].pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90)
        axs[2].set_title("Kreisdiagramm")
        
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    KpiApp().run()
