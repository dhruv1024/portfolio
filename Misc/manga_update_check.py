from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

class MainApp(App):
	def build(self):
		v_layout = BoxLayout(orientation="vertical")
		h_layout = BoxLayout()
		self.img = Image(source='/home/gemini/Pictures/Poller.png',
						allow_stretch=True,
						keep_ratio=False)
		self.search = TextInput(
			multiline=False, halign="left", font_size=55, size_hint=(3,1)
		)
		h_layout.add_widget(self.img)
		h_layout.add_widget(self.search)
		#vertical #1
		v_layout.add_widget(h_layout)

		h_layout = BoxLayout()
		tab_1 = Button(text='news', size_hint=(.5, 1))
		tab_1.bind(on_press=self.on_press_button)

		tab_2 = Button(text='news', size_hint=(.5, 1))
		tab_2.bind(on_press=self.on_press_button)

		h_layout.add_widget(tab_1)
		h_layout.add_widget(tab_2)
		#vertical #2
		v_layout.add_widget(h_layout)

		v_layout

		return v_layout

	def on_press_button(self, instance):
		print('shift tab!')

if __name__ == '__main__':
	app = MainApp()
	app.run()
