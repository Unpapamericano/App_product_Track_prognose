import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

kivy.require('2.0.0')

class KpiApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        self.label = Label(text="KPI Dashboard", size_hint_y=None, height=44)
        btn = Button(text="Zeige Prognose für Gesamtlieferungen", size_hint_y=None, height=44)
        btn.bind(on_press=self.show_plot)
        layout.add_widget(self.label)
        layout.add_widget(btn)
        return layout

    def on_start(self):
        # Daten sammeln (normalerweise aus einer Datenbank)
        self.data = {
            'Datum': pd.date_range(start="2023-01-01", periods=30, freq='D'),
            'Gesamtlieferungen': np.random.randint(50, 200, 30),
            'Produktretouren': np.random.randint(0, 50, 30),
            'DefekteProdukte': np.random.randint(0, 10, 30)
        }

    def show_plot(self, instance):
        # Erstelle DataFrame aus den gesammelten Daten
        df = pd.DataFrame(self.data)
        df['Datum'] = pd.to_datetime(df['Datum'])
        df.set_index('Datum', inplace=True)
        df = df.asfreq('D')  # Establecer frecuencia diaria

        # Diferenciación para hacer los datos estacionarios
        df_diff = df.diff().dropna()

        # ARIMA Prognose für Gesamtlieferungen
        model = ARIMA(df_diff['Gesamtlieferungen'], order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=5)

        # Integra el pronóstico para volver a la escala original
        forecast_original_scale = df['Gesamtlieferungen'].iloc[-1] + forecast.cumsum()

        # Erstelle einen Plot
        plt.figure(figsize=(10, 6))
        df['Gesamtlieferungen'].plot(label="Reale Daten")
        forecast_original_scale.plot(label="Prognose", linestyle="--")
        plt.title('Gesamtlieferungen über die Zeit mit Prognose')
        plt.ylabel('Anzahl')
        plt.xlabel('Datum')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    KpiApp().run()


