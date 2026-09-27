from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import math

class PoissonApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.12, 1)
        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        title = Label(text='[b]POISSON ANALİZ MOTORU[/b]', markup=True, font_size='22sp', size_hint_y=None, height=40)
        root.add_widget(title)

        scroll = ScrollView()
        form = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))

        # Ev Sahibi
        form.add_widget(Label(text='[color=3399ff]EV SAHİBİ[/color]', markup=True, size_hint_y=None, height=30))
        self.ev_adi = TextInput(text='Beşiktaş', multiline=False, size_hint_y=None, height=40)
        self.ev_mac = TextInput(text='10', input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.ev_att = TextInput(text='18', input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.ev_def = TextInput(text='10', input_filter='int', multiline=False, size_hint_y=None, height=40)
        
        for w in [self.ev_adi, self.ev_mac, self.ev_att, self.ev_def]:
            form.add_widget(w)

        # Deplasman
        form.add_widget(Label(text='[color=ff9933]DEPLASMAN[/color]', markup=True, size_hint_y=None, height=30))
        self.dep_adi = TextInput(text='Trabzonspor', multiline=False, size_hint_y=None, height=40)
        self.dep_mac = TextInput(text='10', input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.dep_att = TextInput(text='14', input_filter='int', multiline=False, size_hint_y=None, height=40)
        self.dep_def = TextInput(text='12', input_filter='int', multiline=False, size_hint_y=None, height=40)

        for w in [self.dep_adi, self.dep_mac, self.dep_att, self.dep_def]:
            form.add_widget(w)

        scroll.add_widget(form)
        root.add_widget(scroll)

        btn = Button(text='HESAPLA', size_hint_y=None, height=50, background_color=(0.2, 0.7, 0.3, 1))
        btn.bind(on_press=self.hesapla)
        root.add_widget(btn)

        self.sonuc_label = Label(text='Sonuçlar burada görünecek...', markup=True, size_hint_y=None, height=120)
        root.add_widget(self.sonuc_label)

        return root

    def hesapla(self, instance):
        try:
            ev_m, ev_a, ev_d = float(self.ev_mac.text), float(self.ev_att.text), float(self.ev_def.text)
            dep_m, dep_a, dep_d = float(self.dep_mac.text), float(self.dep_att.text), float(self.dep_def.text)

            xg_ev = ((ev_a / ev_m) * (dep_d / dep_m)) / 1.40
            xg_dep = ((dep_a / dep_m) * (ev_d / ev_m)) / 1.40

            matrix = {}
            for h in range(7):
                for a in range(7):
                    p_h = (math.pow(xg_ev, h) * math.exp(-xg_ev)) / math.factorial(h)
                    p_a = (math.pow(xg_dep, a) * math.exp(-xg_dep)) / math.factorial(a)
                    matrix[(h, a)] = p_h * p_a

            ms1 = sum(p for (h, a), p in matrix.items() if h > a)
            ms0 = sum(p for (h, a), p in matrix.items() if h == a)
            ms2 = sum(p for (h, a), p in matrix.items() if h < a)

            res = f"[b]xG:[/b] {self.ev_adi.text}: {xg_ev:.2f} | {self.dep_adi.text}: {xg_dep:.2f}\n"
            res += f"[b]MS 1:[/b] %{ms1*100:.1f} | [b]MS 0:[/b] %{ms0*100:.1f} | [b]MS 2:[/b] %{ms2*100:.1f}"
            self.sonuc_label.text = res
        except Exception as e:
            self.sonuc_label.text = "Hata oluştu! Değerleri kontrol edin."

if __name__ == '__main__':
    PoissonApp().run()
