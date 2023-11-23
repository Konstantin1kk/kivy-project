from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.popup import Popup
from functools import partial
from kivy.uix.slider import Slider
import os
import random


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        main_screen = Paint(name='paint')
        sm.add_widget(FirstWindow(name='first'))
        sm.add_widget(LovePercent(name='love'))
        sm.add_widget(Photo(name='photo'))
        sm.add_widget(main_screen)
        sm.add_widget(Stress(name='stress'))

        sm.current = 'first'
        return sm


class FirstWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        fl = FloatLayout()

        # Creation
        self.button_left = Button(text='check for fidelity', size_hint=(None, None), size=(200, 100))
        self.button_right = Button(text='take a picture', size_hint=(None, None), size=(200, 100))
        self.button_up = Button(text='stress canvas', size_hint=(None, None), size=(200, 100))
        self.button_down = Button(text='mini paint', size_hint=(None, None), size=(200, 100))
        self.label = Label(text='I hope you enjoy this', size=(200, 100), color='pink')

        # Editing
        self.button_left.pos_hint = {'left': 1, 'center_y': 0.5}
        self.button_left.id = 'love'
        self.button_left.direction = 'right'
        self.button_right.pos_hint = {'right': 1, 'center_y': 0.5}
        self.button_right.id = 'photo'
        self.button_right.direction = 'left'
        self.button_up.pos_hint = {'top': 1, 'center_x': 0.5}
        self.button_up.id = 'stress'
        self.button_up.direction = 'down'
        self.button_down.pos_hint = {'bottom': 1, 'center_x': 0.5}
        self.button_down.id = 'paint'
        self.button_down.direction = 'up'
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add to layout
        fl.add_widget(self.button_left)
        fl.add_widget(self.button_right)
        fl.add_widget(self.button_up)
        fl.add_widget(self.button_down)
        fl.add_widget(self.label)

        # Bind buttons to functions
        self.button_left.bind(on_press=self.next_screen)
        self.button_right.bind(on_press=self.next_screen)
        self.button_down.bind(on_press=self.next_screen)
        self.button_up.bind(on_press=self.next_screen)

        self.add_widget(fl)

    def next_screen(self, button_info):
        self.manager.transition = SlideTransition(direction=button_info.direction)
        self.manager.current = button_info.id


class LovePercent(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fl = FloatLayout()

        # Creation
        label_name1 = Label(text="first person's name", size=(200, 100))
        self.input_name1 = TextInput(multiline=False, size_hint=(None, None), size=(200, 100))
        label_name2 = Label(text='the name of the second person', size=(200, 100))
        self.input_name2 = TextInput(multiline=False, size_hint=(None, None), size=(200, 100))
        result_button = Button(text='find out the results', size_hint=(None, None), size=(200, 100))
        back_button = Button(text='back', size_hint=(None, None))
        back_button.id = 'first'
        self.current_label = None

        # Editing
        label_name1.pos_hint = {'center_x': 0.4, 'center_y': 0.65}
        self.input_name1.pos_hint = {'x': 0.65, 'y': 0.60}

        label_name2.pos_hint = {'center_x': 0.4, 'center_y': 0.45}
        self.input_name2.pos_hint = {'center_x': 0.78, 'center_y': 0.45}

        result_button.pos_hint = {'center_x': 0.5, 'bottom': 1}
        back_button.pos_hint = {'right': 1}

        # Add to layout
        self.fl.add_widget(label_name1)
        self.fl.add_widget(self.input_name1)
        self.fl.add_widget(label_name2)
        self.fl.add_widget(self.input_name2)
        self.fl.add_widget(result_button)
        self.fl.add_widget(back_button)

        # Bind
        back_button.bind(on_press=self.back)
        result_button.bind(on_press=self.result)

        self.add_widget(self.fl)

    def back(self, button_info):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = button_info.id

    def result(self, button_info):
        percent = random.randrange(0, 100)
        label = Label(text=f'you are {percent}% compatible', pos_hint={'center_x': 0.25, 'center_y': 0.60}, color='red')
        popup = Popup(title='Error', content=Label(text='Incorrect values were entered'), size_hint=(None, None))
        popup.size, popup.pos_hint = (300, 150), {'top': 1}
        if self.current_label is not None and (self.on_text(self.input_name1.text) and self.on_text(self.input_name2.text)):
            self.fl.remove_widget(self.current_label)
        elif not (self.on_text(self.input_name1.text) and self.on_text(self.input_name2.text)):
            if self.current_label == None:
                self.current_label = Label(text='', pos_hint={''})
            self.fl.remove_widget(self.current_label)
            label.text = ' '
            popup.open()

        self.current_label = label
        self.current_label.pos_hint = {'center_x': 0.20, 'center_y': 0.091}
        self.fl.add_widget(self.current_label)

    def on_text(self, text):
        return text.isalpha()


class Photo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fl = FloatLayout()

        # Creating
        button_get_photo = Button(text='take a photo', size_hint=(None, None), size=(200, 100))
        back_button = Button(text='back', size_hint=(None, None))
        self.current_image = None

        # Editing
        button_get_photo.pos_hint = {'center_x': 0.5, 'bottom': 1}
        back_button.id = 'first'

        # Add to layout
        self.fl.add_widget(button_get_photo)
        self.fl.add_widget(back_button)

        # Bind
        button_get_photo.bind(on_press=self.rd_image)
        back_button.bind(on_press=self.back)

        self.add_widget(self.fl)

    def rd_image(self, button_info):
        list_files = os.listdir('kivy_images')
        img = Image(source=f'kivy_images/{random.choice(list_files)}', size_hint=(None, None), size=(400, 400), pos=(200, 150))
        if self.current_image is not None:
            self.fl.remove_widget(self.current_image)

        self.fl.add_widget(img)
        self.current_image = img

    def back(self, button_info):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = button_info.id


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Editing
        self.x = (800 / 2) - (200 / 2)
        self.a = 1
        self.r, self.g, self.b = .0, .0, .0

    def on_touch_down(self, touch):
        color = self.r, self.g, self.b, self.a
        with self.canvas:
            Color(*color, mode='rgba')
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class Paint(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fl = FloatLayout()

        # Creating
        self.paint = MyPaintWidget()
        button_back = Button(text='back', size_hint=(None, None), pos_hint={'mid': 1, 'right': 1})
        button_clear = Button(text='clear', size_hint=(None, None), pos_hint={'center_x': 0.5, 'bottom': 1})
        self.slider_r = Slider(min=0, max=1, size_hint=(None, None), pos_hint={'center_y': 0.15, 'center_x': 0.16})
        self.slider_g = Slider(min=0, max=1, size_hint=(None, None), pos_hint={'center_y': 0.1, 'center_x': 0.16})
        self.slider_b = Slider(min=0, max=1, size_hint=(None, None), pos_hint={'center_y': 0.05, 'center_x': 0.16})

        # Editing and binding
        button_back.id = 'first'
        self.slider_r.id, self.slider_g.id, self.slider_b.id = 'r', 'g', 'b'
        self.slider_r.size = (255, 20)
        self.slider_g.size = (255, 20)
        self.slider_b.size = (255, 20)

        button_back.bind(on_press=self.back)
        button_clear.bind(on_press=self.clear)
        self.slider_r.bind(on_touch_move=self.change_color)
        self.slider_g.bind(on_touch_move=self.change_color)
        self.slider_b.bind(on_touch_move=self.change_color)

        # Add to layout
        self.fl.add_widget(self.slider_r)
        self.fl.add_widget(self.slider_g)
        self.fl.add_widget(self.slider_b)
        self.fl.add_widget(button_clear)
        self.fl.add_widget(button_back)
        self.fl.add_widget(self.paint)

        self.add_widget(self.fl)

    def clear(self, button):
        self.paint.canvas.clear()

    def change_color(self, slider, value):
        if slider.id == 'r':
            self.paint.r = slider.value
        elif slider.id == 'g':
            self.paint.g = slider.value
        elif slider.id == 'b':
            self.paint.b = slider.value

    def back(self, button_info):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = button_info.id


class Stress(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        wid = Widget(width=200, height=200, x=1, y=1)
        layout = BoxLayout(size_hint=(1, None), height=50)

        # Create widgets
        label = Label(text='0')
        btn_add100 = Button(text='+ 100 rects', on_press=partial(self.add_rects, label, wid, 100))
        btn_add500 = Button(text='+ 500 rects', on_press=partial(self.add_rects, label, wid, 500))
        btn_back = Button(text='back', on_press=self.back)
        btn_reset = Button(text='reset', on_press=partial(self.reset_rects, label, wid))

        # Editing
        btn_back.id = 'first'

        # Add to layout
        layout.add_widget(btn_add100)
        layout.add_widget(btn_add500)
        layout.add_widget(btn_reset)
        layout.add_widget(label)
        layout.add_widget(btn_back)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(wid)
        main_layout.add_widget(layout)

        self.add_widget(main_layout)

    def add_rects(self, label, wid, count, *largs):
        label.text = str(int(label.text) + count)
        with wid.canvas:
            for x in range(count):
                Color(random.random(), 1, 1, mode='hsv')
                Rectangle(pos=(random.randint(0, wid.width) + wid.x, random.randint(0, wid.height) + wid.y), size=(20, 20))

    def back(self, button):
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = button.id

    def reset_rects(self, label, wid, *largs):
        label.text = '0'
        wid.canvas.clear()


app = MyApp()
app.title = 'TikTok'
app.run()
