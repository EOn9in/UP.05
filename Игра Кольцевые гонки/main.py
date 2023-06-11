import arcade
import arcade.gui
from Text import *
import random
from arcade.gui import UIManager
from arcade import load_texture
from arcade.gui.widgets import UITextArea, UITexturePane
from pyglet.image import load as pyglet_load
import math
import time

SCREEN_TITLE = "Кольцевые гонки"

CIRCLE_RADIUS_OUTER = 270
CIRCLE_RADIUS_INNER = 220
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

ELLIPSE_SEMIMAJOR_AXIS = 300
ELLIPSE_SEMIMINOR_AXIS = 170
ELLIPSE_SEMIMINOR_AXIS_OUTER = 270
ELLIPSE_SEMIMAJOR_AXIS_OUTER = 340


class ZastavkaView(arcade.View):
    def play_music(self):
        if not SettingsView.media_player:
            SettingsView.my_music = arcade.load_sound(SettingsView.songs[SettingsView.cur_song_index])
            SettingsView.media_player = SettingsView.my_music.play(loop=True)
    
    def on_show_view(self):
        Zastavki = ['Picture/Заставка 1.jpg', 'Picture/Заставка 2.jpg', 'Picture/Заставка 3.jpg', 'Picture/Заставка 4.jpeg', "Picture/Заставка 5.jpg", "Picture/Заставка 6.jpg", "Picture/Заставка 7.jpg"]
        fon = random.choice(Zastavki)
        self.background = arcade.load_texture(fon)
        self.play_music()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        self.width, self.height = self.window.get_size()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background)
    
        arcade.draw_rectangle_filled(self.width * 0.5, self.height * 0.4625, self.width * 0.875, self.height * 0.15, arcade.color.BLACK + (150,))
        arcade.draw_text("Здравствуйте, кликните мышью чтобы продолжить", self.width * 0.5, self.height * 0.4625,
                        arcade.color.WHITE, font_size=self.width * 0.025, anchor_x="center",  font_name="Arial")
        arcade.draw_text("Нажмите F, чтобы включить полноэкранный режим", self.width * 0.5, self.height * 0.415, arcade.color.WHITE, font_size=self.width* 0.0188, anchor_x="center",font_name="Arial")


    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.width, self.height = self.window.get_size()
            self.window.set_viewport(0, self.width, 0, self.height)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        menu_view = MenuView()
        menu_view.setup()
        self.window.show_view(menu_view)


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()


    def setup(self):
        self.window_size = self.window.get_size()   
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.width, self.height = self.window.get_size()

        self.background = arcade.load_texture("Picture/Fon.png")

        if self.width == 800:
            width_btn = 300
            height_btn = 50
        else:
            width_btn = 500
            height_btn = 70

 # Создайте вертикальную группу блоков для выравнивания кнопок
        self.v_box = arcade.gui.UIBoxLayout(x=self.width * 0.5, y= self.height * 0.5, align='center')

        start_button = arcade.gui.UIFlatButton(text="Играть", width=width_btn, height=height_btn)
        self.v_box.add(start_button.with_space_around(bottom=30))

        settings_button = arcade.gui.UIFlatButton(text="Настройки", width=width_btn, height=height_btn)
        self.v_box.add(settings_button.with_space_around(bottom=30))

        rules_button = arcade.gui.UIFlatButton(text="Об игре", width=width_btn, height=height_btn)
        self.v_box.add(rules_button.with_space_around(bottom=30))

        quit_button = QuitButton(text="Выход", width=width_btn, height=height_btn)
        self.v_box.add(quit_button)
#обработка нажатия на кнопку
        @start_button.event("on_click")
        def on_click_message(event):
            start_window = StartView()
            start_window.setup()
            self.window.show_view(start_window)
            managerclear(self)

        @settings_button.event("on_click")
        def on_click_message(event):
            settings_window = SettingsView()
            settings_window.setup()
            self.window.show_view(settings_window)
            managerclear(self)

        @rules_button.event("on_click")
        def on_click_rules(event):
            rules_window = RulesView()
            rules_window.setup()
            self.window.show_view(rules_window)
            managerclear(self)

#Создаются виджет для хранения виджета v_box, который будет центрировать кнопки
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))

    def on_draw(self):
        self.clear()
        self.width, self.height = self.window.get_size()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        arcade.draw_text("Кольцевые гонки", self.width * 0.5, self.height * 0.825,
                         arcade.color.BLACK, font_size=50, anchor_x="center", font_name="Kenney Future")
        
        self.manager.draw()


class StartView(arcade.View):
    pixel_button_created = False
    space_button_created = False

    def on_show_view(self):
        self.background = arcade.load_texture("Picture/Fon.png")
        
    def setup(self):
        self.width, self.height = self.window.get_size()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.keyword = ''
        
        
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        self.button_box = arcade.gui.UIBoxLayout()

        if self.width == 800:
            width_btn = 400
            height_btn = 50
            width_btn_back = 200
            height_btn_back = 50
            back_x, back_y = 250, -250
        else:
            width_btn = 600
            height_btn = 70
            width_btn_back = 250
            height_btn_back = 60
            back_x, back_y = 500, -300


        workout_style = {
            "font_name": ("Arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.CARIBBEAN_GREEN,

            # При наведении на кнопку
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.BOTTLE_GREEN,
            "font_color_pressed": arcade.color.BOTTLE_GREEN,
        }
         

        level_0 = arcade.gui.UIFlatButton(text="Тренировочный уровень", width=width_btn, height=height_btn, style=workout_style)
        self.button_box.add(level_0.with_space_around(bottom = 40))

        level_1 = arcade.gui.UIFlatButton(text="Уровень 1", width=width_btn, height=height_btn)
        self.button_box.add(level_1.with_space_around(bottom = 40))

        level_2 = arcade.gui.UIFlatButton(text="Уровень 2", width=width_btn, height=height_btn)
        self.button_box.add(level_2.with_space_around(bottom = 40))
 
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.button_box))
        
        back_button = arcade.gui.UIFlatButton(text="Назад",
                                               width=width_btn_back, height=height_btn_back)

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=back_x,align_y=back_y,
                child=back_button))
        
        @level_0.event("on_click")
        def on_click_message(event):
            level0_window = LevelWorkoutView()
            level0_window.setup()
            self.window.show_view(level0_window)
            managerclear(self)
            uimanagerclear(self)


        @level_1.event("on_click")
        def on_click_message(event):
            level1_window = Level1View()
            level1_window.setup()
            self.window.show_view(level1_window)
            managerclear(self)
            uimanagerclear(self)

        @level_2.event("on_click")
        def on_click_message(event):
            level2_window = Level2View()
            level2_window.setup()
            self.window.show_view(level2_window)
            managerclear(self)
            uimanagerclear(self)
        
        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)
        
        self.restore_buttons()  

    def on_key_press(self, key, modifiers):
        try:
            char = chr(key)
            if char.isalnum():
                self.keyword += char
        except OverflowError:
            pass

        if self.keyword[-5:].upper() == "PIXEL" and self.pixel_button_created == False:
            self.create_pixel_button()
            

        if self.keyword[-5:].upper() == "SPACE" and self.space_button_created == False:
            self.create_space_button()

    def restore_buttons(self):
        if StartView.pixel_button_created:
            self.create_pixel_button()
        
        if StartView.space_button_created:
            self.create_space_button()

    def create_pixel_button(self):
        StartView.pixel_button_created = True
        if self.width == 800:
            width_btn = 400
            height_btn = 50
        else:
            width_btn = 600
            height_btn = 70

        pixel_style = {
            "font_name": ("Arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.CADMIUM_ORANGE,

            # При наведении на кнопку
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.BUFF,
            "font_color_pressed": arcade.color.BUFF,
        }

        pixel_button = arcade.gui.UIFlatButton(text="Пиксель", width=width_btn, height=height_btn, style=pixel_style)

        self.button_box.add(pixel_button.with_space_around(bottom=30))

        @pixel_button.event("on_click")
        def on_click_message(event):
            levelpixel_window = LevelPixelView()
            levelpixel_window.setup()
            self.window.show_view(levelpixel_window)
            managerclear(self)
            uimanagerclear(self)
            

    def create_space_button(self):
        StartView.space_button_created = True
        if self.width == 800:
            width_btn = 400
            height_btn = 50
        else:
            width_btn = 600
            height_btn = 70

        space_style = {
            "font_name": ("Arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.CELADON_BLUE,

            # При наведении на кнопку
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.CERULEAN_BLUE,
            "font_color_pressed": arcade.color.CERULEAN_BLUE,
        }   

        space_button = arcade.gui.UIFlatButton(text="Космос", width=width_btn, height=height_btn, style=space_style)

        self.button_box.add(space_button.with_space_around(bottom=30))

        @space_button.event("on_click")
        def on_click_message(event):
            levelspace_window = LevelSpaceView()
            levelspace_window.setup()
            self.window.show_view(levelspace_window)
            managerclear(self)
            uimanagerclear(self)

    def on_draw(self):
        
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        if self.width == 800:
            arcade.draw_text("Выберите уровень", self.width / 2, self.height * 0.9,
                         arcade.color.BLACK, font_size=34, anchor_x="center")
        else:
            arcade.draw_text("Выберите уровень", self.width / 2, self.height * 0.9 - 50,
                         arcade.color.BLACK, font_size=44, anchor_x="center")
        self.manager.draw()
        self.uimanager.draw()


class SettingsView(arcade.View):
    media_player = None
    paused = True
    songs = [":resources:music/funkyrobot.mp3",
             ":resources:music/1918.mp3"]
    cur_song_index = 0
    my_music = None

    def setup(self):
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.width, self.height = self.window.get_size()
        if self.width == 800:
            size_sound_btn = 0.5
            width_btn_back = 200
            height_btn_back = 50
            back_x, back_y = 250, 320
            X_box,y_box = -140, 80
        else:
            size_sound_btn = 0.8
            width_btn_back = 250
            height_btn_back = 60
            back_x, back_y = 500, 340
            X_box,y_box = -180, 80

        self.manager = UIManager()
        self.manager.enable()
        self.cur_song_index = 0
        self.my_music = arcade.load_sound(self.songs[self.cur_song_index])   

        self.uimanager = arcade.gui.UIManager(self.window)

        box = arcade.gui.UIBoxLayout(vertical=False)

        # Кнопка Старт
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/"
                                             "sound_off.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                            "sound_off.png")
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/"
                                            "sound_off.png")

        self.start_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.start_button.on_click = self.start_button_clicked
        self.start_button.scale(size_sound_btn + 0.4)

        box.add(self.start_button)

        # Кнопка Убавить звук
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/down.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/down.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/down.png")

        self.down_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.down_button.on_click = self.volume_down
        self.down_button.scale(size_sound_btn)

        box.add(self.down_button)

        # Кнопка Прибавить Звук
        press_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png")
        normal_texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/up.png")
        hover_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/up.png")

        self.up_button = arcade.gui.UITextureButton(
            texture=normal_texture,
            texture_hovered=hover_texture,
            texture_pressed=press_texture,
        )

        self.up_button.on_click = self.volume_up
        self.up_button.scale(size_sound_btn)

        box.add(self.up_button)

        self.uimanager.add(arcade.gui.UIAnchorWidget(child=box, align_x= X_box, align_y= y_box))

        back_button = arcade.gui.UIFlatButton(text="Назад",
                                                    width=width_btn_back, height=height_btn_back)

        self.uimanager.add(
                    arcade.gui.UIAnchorWidget(align_x=back_x, align_y=-back_y,anchor_x = "center",anchor_y="center", child=back_button))
        
        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)


    def volume_down(self, *_):
        if self.media_player and self.media_player.volume > 0.2:
            self.media_player.volume -= 0.2

    def volume_up(self, *_):
        if self.media_player and self.media_player.volume < 1.0:
            self.media_player.volume += 0.2

    def sound_button_on(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_on.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_on.png")

    def sound_button_off(self):
        self.start_button.texture_pressed = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")
        self.start_button.texture = \
            arcade.load_texture(":resources:onscreen_controls/flat_dark/sound_off.png")
        self.start_button.texture_hovered = \
            arcade.load_texture(":resources:onscreen_controls/shaded_dark/sound_off.png")

    def start_button_clicked(self, *_):
        if SettingsView.paused == True:
            self.paused = not self.paused
            if not self.media_player:
                self.media_player = self.my_music.play()
                self.media_player.push_handlers(on_eos=self.music_over)
                self.sound_button_on()
            elif not self.media_player.playing and not self.paused:
                self.media_player.play()
                self.sound_button_on()
            elif self.media_player.playing and self.paused:
                self.media_player.pause()
                self.sound_button_off()


    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        if self.width == 800:
            arcade.draw_rectangle_filled(self.width // 2 - 5, 500, 420, 105, arcade.color.WHITE + (180,))
            arcade.draw_rectangle_filled(self.width // 2 - 5, 250, 420, 105, arcade.color.WHITE + (180,))
            arcade.draw_text("Звук", self.width * 0.26, self.height * 0.71,arcade.color.BLACK, font_size=18)
            arcade.draw_text("Экран", self.width * 0.26, self.height * 0.4,arcade.color.BLACK, font_size=18)
            arcade.draw_text("Нажмите F, чтобы сменить оконный/полный экран", self.width // 3 - 80, self.height * 0.3,arcade.color.BLACK, font_size=13)
            arcade.draw_text("Настройки", self.width // 2, self.height * 0.9,
                            arcade.color.BLACK, font_size=30, anchor_x="center")
            if self.media_player:
                volume = self.media_player.volume
                arcade.draw_text(f"Громкость: {volume:3.1f}",
                                start_x=self.width * 0.48, start_y=self.height * 0.59, color=arcade.color.BLACK, font_size=24)
        else:
            arcade.draw_rectangle_filled(self.width // 2 - 5, 500, 600, 125, arcade.color.WHITE + (180,))
            arcade.draw_rectangle_filled(self.width // 2 - 5, 250, 600, 125, arcade.color.WHITE + (180,))
            arcade.draw_text("Звук", self.width * 0.3, self.height * 0.71,arcade.color.BLACK, font_size=18)
            arcade.draw_text("Экран", self.width * 0.3, self.height * 0.4,arcade.color.BLACK, font_size=18)
            arcade.draw_text("Нажмите F, чтобы сменить оконный/полный экран", self.width // 3, self.height * 0.3,arcade.color.BLACK, font_size=16)
            arcade.draw_text("Настройки", self.width // 2, self.height * 0.9,
                            arcade.color.BLACK, font_size=44, anchor_x="center")
            if self.media_player:
                volume = self.media_player.volume
                arcade.draw_text(f"Громкость: {volume:3.1f}",
                                start_x=self.width * 0.52, start_y=self.height * 0.59 - 5, color=arcade.color.BLACK, font_size=28)
        
        self.manager.draw()
        self.uimanager.draw()


    def on_show_view(self):
        SettingsView.paused = True
        self.background = arcade.load_texture("Picture/Fon.png")
        self.uimanager.enable()
        if self.my_music is None:
            self.my_music = arcade.load_sound(self.songs[self.cur_song_index])

        # Pause the music if it's playing
        if self.media_player and self.media_player.playing:
            self.media_player.pause()
            self.sound_button_off()


    def on_hide_view(self):
        self.uimanager.disable()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.width, self.height = self.window.get_size()
            self.window.set_viewport(0, self.width, 0, self.height)

class RulesView(arcade.View):

    def on_show_view(self):
        self.width, self.height = self.window.get_size()
        if self.width == 800:
            self.background = arcade.load_texture("Picture/QR_fon_800.png")
        else:
            self.background = arcade.load_texture("Picture/QR_fon.png")
        
    def setup(self):
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.manager = UIManager()
        self.manager.enable()

        self.create_ui_elements()

    def create_ui_elements(self):
        self.width, self.height = self.window.get_size()
        if self.width == 800:
            width_btn_back = 200
            height_btn_back = 50
            font_size = 12
            back_x, back_y = 250, -290
        else:
            width_btn_back = 250
            height_btn_back = 60
            font_size = 15
            back_x, back_y = 500, -340

        bg_tex = load_texture("Picture/Panel.png")
        text_area = UITextArea(x=self.width / 4,
                               y=self.height / 3.2,
                               width=self.width / 2,
                               height=self.height / 2.4,
                               text=rules,
                               text_color=(0, 0, 0, 255),
                               font_size = font_size)
        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(20, 20, 20, 20)
            )
        )

        back_button = arcade.gui.UIFlatButton(text="Назад",
                                               width=width_btn_back,height=height_btn_back)

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=back_x,align_y=back_y,anchor_y="center",anchor_x='center',
                child=back_button))
        

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)

    def on_draw(self):
        self.width, self.height = self.window.get_size()
        self.window.set_viewport(0, self.width, 0, self.height)

        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background)
        if self.width == 800:
            arcade.draw_text("Об игре", self.width // 2, self.height * 0.9,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        else:
            arcade.draw_text("Об игре", self.width // 2, self.height * 0.9 - 55,
                         arcade.color.BLACK, font_size=44, anchor_x="center")
        
        self.manager.draw()
        self.uimanager.draw()


class Level1View(arcade.View):
    
    def setup(self):
        self.width, self.height = self.window.get_size()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("Picture/Трасса уровень 1.png")
        self.crash_sound = arcade.sound.load_sound("Sound/Звук столкновения.mp3")


        self.total_time = 0.0
        self.output = "00:00:00"

        self.car = Car("Picture/Car.png", 1)
        self.car_crash_texture = arcade.load_texture("Picture/Car_Crash.png")
        self.car_bot_crash = arcade.load_texture("Picture/Car_bot_Crash.png")
        if self.width == 800:
            self.car.center_x = CIRCLE_RADIUS_INNER - 50
            self.car.center_y = SCREEN_HEIGHT / 2
        else:
            self.car.center_x = CIRCLE_RADIUS_INNER + 280
            self.car.center_y = SCREEN_HEIGHT / 2

        self.car_bot = Car_Computer("Picture/Car_bot.png", 1)
        if self.width == 800:
            self.car_bot.center_x = CIRCLE_RADIUS_INNER + 350
            self.car_bot.center_y = SCREEN_HEIGHT / 3
            back_button = arcade.gui.UIFlatButton(text="⌂",
                                               width=40,height=40)
        else:
            self.car_bot.center_x = CIRCLE_RADIUS_INNER + 800
            self.car_bot.center_y = SCREEN_HEIGHT / 3 + 100
            back_button = arcade.gui.UIFlatButton(text="На Главную ⌂",
                                               width=150,height=50)

        
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=360,align_y=350,anchor_y="center",anchor_x='center',
                child=back_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            uimanagerclear(self)

        self.game_started = False
        self.color = arcade.color.BLACK
        self.time_since_last_color_change = time.time()

        self.pozarnay_car = arcade.Sprite('Picture/Пожарка.png', 0.2)
        if self.width == 800:
            self.pozarnay_car.center_x = 40
            self.pozarnay_car.center_y = 420
        else:
            self.pozarnay_car.center_x = 450
            self.pozarnay_car.center_y = 440

        self.pozarn_man = arcade.Sprite('Picture/Пожарный.png', 0.04)
        if self.width == 800:
            self.pozarn_man.center_x = 90
            self.pozarn_man.center_y = 390
        else:
            self.pozarn_man.center_x = 480
            self.pozarn_man.center_y = 395

    def on_draw(self):
        self.width, self.height = self.window.get_size()
        arcade.start_render()
        if self.width == 800:
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 1.7, 30, arcade.color.BLACK, 14)
            arcade.draw_text('ESCAPE - пауза', self.width / 20, self.height / 1.08, arcade.color.BLACK, 14)
            
        if self.width != 800:
            arcade.draw_lrwh_rectangle_textured(375, 33,
                                            SCREEN_WIDTH,SCREEN_HEIGHT,
                                            self.background)
            arcade.draw_text('ESCAPE - пауза', self.width / 4, self.height / 1.08, arcade.color.BLACK, 23)
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 1.7, 30, arcade.color.BLACK, 23)
        
        arcade.draw_text(self.output,
                         self.width // 2, self.height // 2,
                         arcade.color.BLACK, 60,
                         anchor_x="center")
        seconds = int(self.total_time) % 60
        if seconds >= 50:
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 2,
                         arcade.color.RED, 60,
                         anchor_x="center")
            
            arcade.draw_text("Осталось ещё немного!",
                         self.width // 2, self.height // 2.3,
                         arcade.color.VERMILION, 24,
                         anchor_x="center")
            
        if self.game_started:
            self.car.draw()
            self.car_bot.draw()
        else:
            self.car.draw()
            self.car_bot.draw()
            if self.width == 800:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 30, 700, 120, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 - 40, self.height / 2 - 60, self.color, 23)
            else:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 60, 870, 180, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 + 30, self.height / 2 - 60, self.color, 33)
        if self.car.crashed:
            self.car.texture = self.car_crash_texture
            self.car_bot.texture = self.car_bot_crash
            self.pozarnay_car.draw()
            self.pozarn_man.draw()

        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.car.inner_lane = not self.car.inner_lane

        if key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)

        if key == arcade.key.ENTER:
            self.game_started = True


    def on_update(self, delta_time):

        if time.time() - self.time_since_last_color_change >= 3:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.time_since_last_color_change = time.time()
        

        if self.game_started:
            self.car.update(self.window, self.game_started)
            self.car_bot.update(self.window, self.car)
            self.total_time += delta_time
        
        minutes = int(self.total_time) // 60


        seconds = int(self.total_time) % 60

        seconds_100s = int((self.total_time - seconds) * 100)

        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        if minutes == 1:
            win_window = WinView()
            win_window.setup()
            self.window.show_view(win_window)


        if (seconds % random.randint(4,8) == 0) and (seconds_100s == random.randint(1,100)):
            self.car_bot.inner_lane_bot = not self.car_bot.inner_lane_bot


        colliding = check_for_collision(self.car, self.car_bot)

        if colliding and not self.car.crashed:
            self.car.crashed = True
            self.car.crash_time = time.time()
            arcade.sound.play_sound(self.crash_sound)

        if self.car.crashed:
            if time.time() - self.car.crash_time >= 1:
                lose_window = LoseViewCrash()
                lose_window.setup()
                self.window.show_view(lose_window)

    
class Level2View(arcade.View):
    def setup(self):
        self.width, self.height = self.window.get_size()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("Picture/Трасса уровень 2.png")
        self.crash_sound = arcade.sound.load_sound("Sound/Звук столкновения.mp3")

        self.total_time = 0.0
        self.output = "00:00:00"

        if self.width == 800:
            size_car = 1
        else:
            size_car = 1.5
        self.car = Car_Level2("Picture/Car.png", size_car)
        self.car_crash_texture = arcade.load_texture("Picture/Car_Crash.png")
        self.car_bot_crash = arcade.load_texture("Picture/Car_bot_Crash.png")
        if self.width == 800:
            self.car.center_x = ELLIPSE_SEMIMAJOR_AXIS - 190
            self.car.center_y = SCREEN_HEIGHT / 2
        else:
            self.car.center_x = ELLIPSE_SEMIMAJOR_AXIS - 190
            self.car.center_y = SCREEN_HEIGHT / 2

        self.car_bot = Car_Computer_Level2("Picture/Car_bot.png", size_car)
        if self.width == 800:
            self.car_bot.center_x = ELLIPSE_SEMIMAJOR_AXIS_OUTER + 350
            self.car_bot.center_y = SCREEN_HEIGHT / 2
            back_button = arcade.gui.UIFlatButton(text="⌂",
                                               width=40,height=40)
        else:
            self.car_bot.center_x = ELLIPSE_SEMIMAJOR_AXIS_OUTER + 1050
            self.car_bot.center_y = SCREEN_HEIGHT / 3 + 40
            back_button = arcade.gui.UIFlatButton(text="На Главную ⌂",
                                               width=150,height=50)
        
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=360,align_y=350,anchor_y="center",anchor_x='center',
                child=back_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            uimanagerclear(self)

        self.game_started = False
        self.color = arcade.color.BLACK
        self.time_since_last_color_change = time.time()


    def on_draw(self):
        self.width, self.height = self.window.get_size()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)

        if self.width == 800:
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', 140, 40, arcade.color.BLACK, 24)
            arcade.draw_text('ESCAPE - пауза', 40, 740, arcade.color.BLACK, 16)
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 2 - 30,
                         arcade.color.BLACK, 70,
                         anchor_x="center")
            seconds = int(self.total_time) % 60
            if seconds >= 50:
                arcade.draw_text(self.output,
                            self.width // 2, self.height // 2 - 30,
                            arcade.color.RED, 70,
                            anchor_x="center")
        else:
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 4, 40, arcade.color.BLACK, 34)
            arcade.draw_text('ESCAPE - пауза', self.width / 6, 800, arcade.color.BLACK, 26)
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 2 - 30,
                         arcade.color.BLACK, 100,
                         anchor_x="center")
            seconds = int(self.total_time) % 60
            if seconds >= 50:
                arcade.draw_text(self.output,
                            self.width // 2, self.height // 2 - 30,
                            arcade.color.RED, 100,
                            anchor_x="center")
        if self.game_started:
            self.car.draw()
            self.car_bot.draw()
        else:
            self.car.draw()
            self.car_bot.draw()
            if self.width == 800:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 30, 700, 120, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 - 40, self.height / 2 - 60, self.color, 23)
            else:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 60, 1500, 210, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 + 30, self.height / 2 - 60, self.color, 33)

        if self.car.crashed:
            self.car.texture = self.car_crash_texture
            self.car_bot.texture = self.car_bot_crash

        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.car.inner_lane = not self.car.inner_lane
        if key == arcade.key.ESCAPE:
            pause = PauseViewLevel2(self)
            self.window.show_view(pause)
        if key == arcade.key.ENTER:
            self.game_started = True

    def update(self, delta_time):
        if time.time() - self.time_since_last_color_change >= 3:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.time_since_last_color_change = time.time()
        
        if self.game_started:
            self.car.update(self.window, self.game_started)
            self.car_bot.update(self.window, self.car)
            self.total_time += delta_time

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        seconds_100s = int((self.total_time - seconds) * 100)

        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        if minutes == 1:
            win_window = WinView()
            win_window.setup()
            self.window.show_view(win_window)

        if (seconds % random.randint(2,6) == 0) and (seconds_100s == random.randint(0,100)):
            self.car_bot.inner_lane_bot = not self.car_bot.inner_lane_bot


        colliding = check_for_collision(self.car, self.car_bot)
        if colliding and not self.car.crashed:
            self.car.crashed = True
            self.car.crash_time = time.time()
            arcade.sound.play_sound(self.crash_sound)

        if self.car.crashed:
            if time.time() - self.car.crash_time >= 1:
                lose_window = LoseViewCrash()
                lose_window.setup()
                self.window.show_view(lose_window)

class LevelPixelView(arcade.View):
    def __init__(self):
        super().__init__()
        self.stop_music()

    def stop_music(self):
        if SettingsView.media_player:
            SettingsView.media_player.pause()
            SettingsView.paused = True

    def resume_music(self):
        if SettingsView.media_player and SettingsView.paused:
            SettingsView.media_player.play()
            SettingsView.paused = False
    
    def setup(self):
        self.width, self.height = self.window.get_size()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        arcade.set_background_color(arcade.color.DARK_TANGERINE)
        self.background = arcade.load_texture("Picture/Pixel.png")
        self.crash_sound = arcade.sound.load_sound("Sound/Звук аварии 8 бит.mp3")
        self.background_music = arcade.sound.load_sound("Sound/Pixel.mp3")
        self.music_player = arcade.sound.play_sound(self.background_music, looping=True)
        self.paused = False


        self.total_time = 0.0
        self.output = "00:00:00"

        self.car = Car("Picture/PixelCar.png", 0.15)
        self.car_crash_texture = arcade.load_texture("Picture/PixelCarCrash.png")
        self.car_bot_crash = arcade.load_texture("Picture/PCarCrash.png")
        if self.width == 800:
            self.car.center_x = CIRCLE_RADIUS_INNER - 50
            self.car.center_y = SCREEN_HEIGHT / 2
        else:
            self.car.center_x = CIRCLE_RADIUS_INNER + 280
            self.car.center_y = SCREEN_HEIGHT / 2

        self.car_bot = Car_Computer("Picture/PCar.png", 0.15)
        if self.width == 800:
            self.car_bot.center_x = CIRCLE_RADIUS_INNER + 350
            self.car_bot.center_y = SCREEN_HEIGHT / 3
            back_button = arcade.gui.UIFlatButton(text="⌂",
                                               width=40,height=40)
            x = 360
            y = 350
        else:
            self.car_bot.center_x = CIRCLE_RADIUS_INNER + 800
            self.car_bot.center_y = SCREEN_HEIGHT / 3 + 100
            back_button = arcade.gui.UIFlatButton(text="На Главную ⌂",
                                               width=150,height=50)
            x = 660
            y = 350

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=x,align_y=y,anchor_y="center",anchor_x='center',
                child=back_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            uimanagerclear(self)
            arcade.sound.stop_sound(self.music_player)
            self.music_player = None

        self.game_started = False
        self.color = arcade.color.BLACK
        self.time_since_last_color_change = time.time()

    def on_draw(self):
        self.width, self.height = self.window.get_size()
        arcade.start_render()
        if self.width == 800:
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 1.7, 30, arcade.color.BLACK, 14)
            arcade.draw_text('ESCAPE - пауза', self.width / 20, self.height / 1.08, arcade.color.BLACK, 14)
            
        if self.width != 800:
            arcade.draw_lrwh_rectangle_textured(375, 33,
                                            SCREEN_WIDTH,SCREEN_HEIGHT,
                                            self.background)
            arcade.draw_text('ESCAPE - пауза', 0, self.height / 1.08, arcade.color.BLACK, 23)
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 1.7, 30, arcade.color.BLACK, 23)
        
        arcade.draw_text(self.output,
                         self.width // 2, self.height // 2,
                         arcade.color.ALICE_BLUE, 60,
                         anchor_x="center")
        seconds = int(self.total_time) % 60
        if seconds >= 50:
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 2,
                         arcade.color.COSMIC_LATTE, 60,
                         anchor_x="center")
            
            arcade.draw_text("Осталось ещё немного!",
                         self.width // 2, self.height // 2.3,
                         arcade.color.ALICE_BLUE, 20,
                         anchor_x="center")
            
        if self.game_started:
            self.car.draw()
            self.car_bot.draw()
        else:
            self.car.draw()
            self.car_bot.draw()
            if self.width == 800:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 30, 700, 120, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 - 40, self.height / 2 - 60, self.color, 23)
            else:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 60, 870, 180, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 + 30, self.height / 2 - 60, self.color, 33)
        if self.car.crashed:
            self.car.texture = self.car_crash_texture
            self.car_bot.texture = self.car_bot_crash

        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.car.inner_lane = not self.car.inner_lane

        if key == arcade.key.ESCAPE:
            pause = PauseViewPixel(self)
            self.window.show_view(pause)
            if self.music_player.playing:  # Поставить музыку на паузу
                self.music_player.pause()
                self.paused = True
            

        if key == arcade.key.ENTER:
            self.game_started = True


    def on_update(self, delta_time):

        if time.time() - self.time_since_last_color_change >= 3:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.time_since_last_color_change = time.time()
        

        if self.game_started:
            self.car.update(self.window, self.game_started)
            self.car_bot.update(self.window, self.car)
            self.total_time += delta_time
        
        minutes = int(self.total_time) // 60


        seconds = int(self.total_time) % 60

        seconds_100s = int((self.total_time - seconds) * 100)

        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        if minutes == 1:
            if self.music_player:
                arcade.sound.stop_sound(self.music_player)
                self.music_player = None
            win_window = WinView()
            win_window.setup()
            self.window.show_view(win_window)
                


        if (seconds % random.randint(2,10) == 0) and (seconds_100s == random.randint(1,100)):
            self.car_bot.inner_lane_bot = not self.car_bot.inner_lane_bot


        colliding = check_for_collision(self.car, self.car_bot)

        if colliding and not self.car.crashed:
            self.car.crashed = True
            self.car.crash_time = time.time()
            arcade.sound.play_sound(self.crash_sound)

        if self.car.crashed:
            if time.time() - self.car.crash_time >= 1:
                lose_window = LoseViewCrash()
                lose_window.setup()
                self.window.show_view(lose_window)
                arcade.sound.stop_sound(self.music_player)
                self.music_player = None

    def on_hide_view(self):
        self.resume_music()

class LevelSpaceView(arcade.View):
    def __init__(self):
        super().__init__()
        self.stop_music()

    def stop_music(self):
        if SettingsView.media_player:
            SettingsView.media_player.pause()
            SettingsView.paused = True

    def resume_music(self):
        if SettingsView.media_player and SettingsView.paused:
            SettingsView.media_player.play()
            SettingsView.paused = False
    def setup(self):
        self.width, self.height = self.window.get_size()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.background = arcade.load_texture("Picture/КосмосФон.jpg")
        self.crash_sound = arcade.sound.load_sound("Sound/Звук аварии 8 бит.mp3")
        self.background_music = arcade.sound.load_sound("Sound/Космос.mp3")
        self.music_player = arcade.sound.play_sound(self.background_music, looping=True)
        self.paused = False


        self.total_time = 0.0
        self.output = "00:00:00"

        self.car = Car("Picture/Ракета.png", 0.15)
        self.car_crash_texture = arcade.load_texture("Picture/Ракета горит.png")
        if self.width == 800:
            self.car.center_x = CIRCLE_RADIUS_INNER - 50
            self.car.center_y = SCREEN_HEIGHT / 2
        else:
            self.car.center_x = CIRCLE_RADIUS_INNER + 280
            self.car.center_y = SCREEN_HEIGHT / 2

        self.car_bot = Car_Computer("Picture/Астероид.png", 0.1)
        if self.width == 800:
            self.car_bot.center_x = CIRCLE_RADIUS_INNER + 350
            self.car_bot.center_y = SCREEN_HEIGHT / 3
            back_button = arcade.gui.UIFlatButton(text="⌂",
                                               width=40,height=40)
            x = 360
            y = 350
        else:
            self.car_bot.center_x = CIRCLE_RADIUS_INNER + 800
            self.car_bot.center_y = SCREEN_HEIGHT / 3 + 100
            back_button = arcade.gui.UIFlatButton(text="На Главную ⌂",
                                               width=150,height=50)
            x = 660
            y = 350
            
        self.planet = arcade.Sprite('Picture/Планета.png',0.35)
        self.planet.center_x = self.width / 2
        self.planet.center_y = self.height / 2


        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=x,align_y=y,anchor_y="center",anchor_x='center',
                child=back_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            uimanagerclear(self)
            arcade.sound.stop_sound(self.music_player)
            self.music_player = None

        self.game_started = False
        self.color = arcade.color.BLACK
        self.time_since_last_color_change = time.time()

    def on_draw(self):
        self.width, self.height = self.window.get_size()
        
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        if self.width == 800:
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 3.2 - 40, self.height / 8 - 50, arcade.color.WHITE, 18)
            arcade.draw_text('ESCAPE - пауза', 0, self.height / 1.03, arcade.color.WHITE, 18)
            
        if self.width != 800:
            arcade.draw_text('ESCAPE - пауза', 0, self.height / 1.04, arcade.color.WHITE, 25)
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 4, 30, arcade.color.WHITE, 25)
        self.planet.draw()
        arcade.draw_text(self.output,
                         self.width // 2, self.height // 1.1,
                         arcade.color.ALICE_BLUE, 60,
                         anchor_x="center")
        seconds = int(self.total_time) % 60
        if seconds >= 50:
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 1.1,
                         arcade.color.COSMIC_LATTE, 60,
                         anchor_x="center")
            
        if self.game_started:
            self.car.draw()
            self.car_bot.draw()
        else:
            self.car.draw()
            self.car_bot.draw()
            if self.width == 800:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 30, 700, 120, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 - 40, self.height / 2 - 60, self.color, 23)
            else:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 60, 870, 180, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 + 30, self.height / 2 - 60, self.color, 33)
        if self.car.crashed:
            self.car.texture = self.car_crash_texture

        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.car.inner_lane = not self.car.inner_lane

        if key == arcade.key.ESCAPE:
            pause = PauseViewSpace(self)
            self.window.show_view(pause)
            if self.music_player.playing:  # Поставить музыку на паузу
                self.music_player.pause()
                self.paused = True

        if key == arcade.key.ENTER:
            self.game_started = True
            


    def on_update(self, delta_time):

        if time.time() - self.time_since_last_color_change >= 3:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.time_since_last_color_change = time.time()
        

        if self.game_started:
            self.car.update(self.window, self.game_started)
            self.car_bot.update(self.window, self.car)
            self.total_time += delta_time
        
        minutes = int(self.total_time) // 60


        seconds = int(self.total_time) % 60

        seconds_100s = int((self.total_time - seconds) * 100)

        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        if minutes == 1:
            if self.music_player:
                arcade.sound.stop_sound(self.music_player)
                self.music_player = None
            win_window = WinView()
            win_window.setup()
            self.window.show_view(win_window)
                

        if (seconds % random.randint(2,10) == 0) and (seconds_100s == random.randint(1,100)):
            self.car_bot.inner_lane_bot = not self.car_bot.inner_lane_bot


        colliding = arcade.check_for_collision(self.car, self.car_bot)

        if colliding and not self.car.crashed:
            self.car.crashed = True
            self.car.crash_time = time.time()
            arcade.sound.play_sound(self.crash_sound)

        if self.car.crashed:
            if time.time() - self.car.crash_time >= 1:
                lose_window = LoseViewCrash()
                lose_window.setup()
                self.window.show_view(lose_window)
                arcade.sound.stop_sound(self.music_player)
                self.music_player = None

    def on_hide_view(self):
        self.resume_music()

class LevelWorkoutView(arcade.View):
    
    def setup(self):
        self.width, self.height = self.window.get_size()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.background = arcade.load_texture('Picture/трасса тренировка.png')
        self.crash_sound = arcade.sound.load_sound("Sound/Звук столкновения.mp3")

        self.total_time = 0.0
        self.output = "00:00:00"

        if self.width == 800:
            size_car = 1
        else:
            size_car = 1.5
        self.car = Car_Level2("Picture/Car.png", size_car)
        self.car_crash_texture = arcade.load_texture("Picture/Car_Crash.png")
        if self.width == 800:
            self.car.center_x = ELLIPSE_SEMIMAJOR_AXIS_OUTER + 350
            self.car.center_y = SCREEN_HEIGHT / 2
            back_button = arcade.gui.UIFlatButton(text="⌂",
                                               width=40,height=40)
            x,y = 360, 350
        else:
            self.car.center_x = ELLIPSE_SEMIMAJOR_AXIS_OUTER + 1050
            self.car.center_y = self.height / 2
            back_button = arcade.gui.UIFlatButton(text="На Главную ⌂",
                                               width=150,height=50)
            x,y = 630, 370
  
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=x,align_y=y,anchor_y="center",anchor_x='center',
                child=back_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            uimanagerclear(self)

        self.wall_list = arcade.SpriteList()

        a = random.randint(1,3)
        if a == 1:
            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS
                wall.center_y = 140
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 280
                wall.center_y = 160
            self.wall_list.append(wall)

            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMINOR_AXIS - 60
                wall.center_y = 400
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS - 80
                wall.center_y = 440
            self.wall_list.append(wall)

            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMINOR_AXIS + 360
                wall.center_y = 650
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 720
                wall.center_y = 700
            self.wall_list.append(wall)

        elif a == 2:
            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 430
                wall.center_y = 360
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 1010
                wall.center_y = 400
            self.wall_list.append(wall)

            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMINOR_AXIS + 20
                wall.center_y = 160
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 40
                wall.center_y = 170
            self.wall_list.append(wall)

            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMINOR_AXIS + 360
                wall.center_y = 650
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 720
                wall.center_y = 700
            self.wall_list.append(wall)

            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMINOR_AXIS + 300
                wall.center_y = 250
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 660
                wall.center_y = 280
            self.wall_list.append(wall)

        else:
            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 270
                wall.center_y = 540
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 390
                wall.center_y = 580
            self.wall_list.append(wall)

            if self.width == 800:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.25)
                wall.center_x = ELLIPSE_SEMIMINOR_AXIS + 20
                wall.center_y = 160
            else:
                wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",0.4)
                wall.center_x = ELLIPSE_SEMIMAJOR_AXIS + 40
                wall.center_y = 170
            self.wall_list.append(wall)

        self.game_started = False
        self.color = arcade.color.BLACK
        self.time_since_last_color_change = time.time()


    def on_draw(self):
        self.width, self.height = self.window.get_size()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        self.wall_list.draw()

        if self.width == 800:
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', 140, 40, arcade.color.BLACK, 24)
            arcade.draw_text('ESCAPE - пауза', 40, 740, arcade.color.BLACK, 16)
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 2 - 30,
                         arcade.color.BLACK, 70,
                         anchor_x="center")
            seconds = int(self.total_time) % 60
            if seconds >= 50:
                arcade.draw_text(self.output,
                            self.width // 2, self.height // 2 - 30,
                            arcade.color.BURNT_ORANGE, 70,
                            anchor_x="center")
        else:
            arcade.draw_text('ПРОБЕЛ - сменить полосу движения', self.width / 4, 40, arcade.color.BLACK, 34)
            arcade.draw_text('ESCAPE - пауза', self.width / 6, 800, arcade.color.BLACK, 26)
            arcade.draw_text(self.output,
                         self.width // 2, self.height // 2 - 30,
                         arcade.color.BLACK, 100,
                         anchor_x="center")
            seconds = int(self.total_time) % 60
            if seconds >= 50:
                arcade.draw_text(self.output,
                            self.width // 2, self.height // 2 - 30,
                            arcade.color.RED, 100,
                            anchor_x="center")
        if self.game_started:
            self.car.draw()
        else:
            self.car.draw()
            if self.width == 800:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 30, 700, 120, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 - 40, self.height / 2 - 60, self.color, 23)
            else:
                arcade.draw_rectangle_filled(self.width // 2, self.height // 2 - 60, 1500, 210, arcade.color.GLITTER + (180,))
                arcade.draw_text('Нажмите Enter, чтобы запустить уровень', self.width / 5 + 30, self.height / 2 - 60, self.color, 33)

        if self.car.crashed:
            self.car.texture = self.car_crash_texture

        self.uimanager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.car.inner_lane = not self.car.inner_lane
        if key == arcade.key.ESCAPE:
            pause = PauseViewWorkout(self)
            self.window.show_view(pause)
        if key == arcade.key.ENTER:
            self.game_started = True


    def update(self, delta_time):
        if time.time() - self.time_since_last_color_change >= 3:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.time_since_last_color_change = time.time()
        

        if self.game_started:
            self.car.update(self.window, self.game_started)
            self.total_time += delta_time

        minutes = int(self.total_time) // 60

        seconds = int(self.total_time) % 60

        seconds_100s = int((self.total_time - seconds) * 100)

        self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

        if minutes == 1:
            win_window = WinView()
            win_window.setup()
            self.window.show_view(win_window)

        colliding = arcade.check_for_collision_with_list(self.car, self.wall_list)
        if colliding and not self.car.crashed:
            self.car.crashed = True
            self.car.crash_time = time.time()
            arcade.sound.play_sound(self.crash_sound)


        if self.car.crashed:
            if time.time() - self.car.crash_time >= 1:
                lose_window = LoseViewCrash()
                lose_window.setup()
                self.window.show_view(lose_window)

class WinView(arcade.View):

    def on_show_view(self):
        self.background = arcade.load_texture("Picture/Fon 3.png")
        
    def setup(self):
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.manager = UIManager()
        self.manager.enable()
        self.width, self.height = self.window.get_size()
        bg_tex = load_texture("Picture/Panel_win.png")
        text_area = UITextArea(x=self.width / 4,
                               y=self.height / 3.2,
                               width=self.width / 2,
                               height=self.height / 2.5,
                               text=winer,
                               text_color=(0, 0, 0, 255),
                               font_size=23)
        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(20, 20, 20, 20)
            )
        )

        if self.width == 800:
            width_btn = 200
            height_btn = 50
        else:
            width_btn = 300
            height_btn = 65

        back_button = arcade.gui.UIFlatButton(text="На Главную",
                                               width=width_btn, height=height_btn)
        levels_button = arcade.gui.UIFlatButton(text="К выбору уровня", width=width_btn, height=height_btn)

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=250,align_y=-250,anchor_y="center",anchor_x='center',
                child=back_button))
        
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=-250,align_y=-250,anchor_y="center",anchor_x='center',
                child=levels_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)
        
        @levels_button.event("on_click")
        def on_click_message(event):
            main_window = StartView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)


    def on_draw(self): 
        self.width, self.height = self.window.get_size() 
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        arcade.draw_text("Поздравляем!", self.width // 2, self.height / 1.2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        
        self.manager.draw()
        self.uimanager.draw()


class LoseViewCrash(arcade.View):

    def on_show_view(self):
        self.background = arcade.load_texture("Picture/Fon 2.png")
        
    def setup(self):
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.manager = UIManager()
        self.manager.enable()
        self.width, self.height = self.window.get_size()
        bg_tex = load_texture("Picture/Panel_lose.png")
        text_area = UITextArea(x=self.width / 4,
                               y=self.height / 3.2,
                               width=self.width / 2,
                               height=self.height / 2.5,
                               text=lose_crash,
                               text_color=(0, 0, 0, 255),
                               font_size=23)
        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(20, 20, 20, 20)
            )
        )
        if self.width == 800:
            width_btn = 200
            height_btn = 50
        else:
            width_btn = 300
            height_btn = 65

        back_button = arcade.gui.UIFlatButton(text="На Главную",
                                               width=width_btn, height=height_btn)
        levels_button = arcade.gui.UIFlatButton(text="К выбору уровня", width=width_btn, height=height_btn)

        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=250,align_y=-250,anchor_y="center",anchor_x='center',
                child=back_button))
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(align_x=-250,align_y=-250,anchor_y="center",anchor_x='center',
                child=levels_button))

        @back_button.event("on_click")
        def on_click_message(event):
            main_window = MenuView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)

        @levels_button.event("on_click")
        def on_click_message(event):
            main_window = StartView()
            main_window.setup()
            self.window.show_view(main_window)
            managerclear(self)
            uimanagerclear(self)


    def on_draw(self):
        self.width, self.height = self.window.get_size()    
        self.clear()
        
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width,self.height,
                                            self.background)
        arcade.draw_text("К сожалению, Вы проиграли!", self.width // 2, self.height - 100,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        
        self.manager.draw()
        self.uimanager.draw()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)
    def on_draw(self):
        self.width, self.height = self.window.get_size()   
        self.clear()
        player_sprite = self.game_view.car
        player_sprite.draw()
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.BLIZZARD_BLUE + (200,))
        arcade.draw_text("ПАУЗА", self.width / 2, self.height / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите Esc,чтобы продолжить",
                         self.width / 2,
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Нажмите Enter, чтобы начать заново",
                         self.width / 2,
                         self.height / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # Пауза
            self.window.show_view(self.game_view)
            arcade.set_background_color(arcade.color.WHITE)
        if key == arcade.key.ENTER:  # Перезапуск
            game_window = Level1View()
            game_window.setup()
            self.window.show_view(game_window)

class PauseViewLevel2(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    def on_show_view(self):
        arcade.set_background_color(arcade.color.TEA_ROSE)
    def on_draw(self):
        self.width, self.height = self.window.get_size() 
        self.clear()
        player_sprite = self.game_view.car
        player_sprite.draw()
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.TEA_ROSE + (200,))
        arcade.draw_text("ПАУЗА", self.width / 2, self.height / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите Esc,чтобы продолжить",
                         self.width / 2,
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Нажмите Enter, чтобы начать заново",
                         self.width / 2,
                         self.height / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # Пауза
            self.window.show_view(self.game_view)
            arcade.set_background_color(arcade.color.WHITE)
        if key == arcade.key.ENTER:  # Перезапуск
            game_window = Level2View()
            game_window.setup()
            self.window.show_view(game_window)

class PauseViewPixel(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_TANGERINE)
    def on_draw(self):
        self.width, self.height = self.window.get_size()   
        self.clear()
        player_sprite = self.game_view.car
        player_sprite.draw()
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.DARK_TANGERINE + (200,))
        arcade.draw_text("ПАУЗА", self.width / 2, self.height / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите Esc,чтобы продолжить",
                         self.width / 2,
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Нажмите Enter, чтобы начать заново",
                         self.width / 2,
                         self.height / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # Возобновите музыку при возврате к игре
            self.window.show_view(self.game_view)
            arcade.set_background_color(arcade.color.DARK_TANGERINE)
            if self.game_view.paused:
                self.game_view.music_player.play()
                self.game_view.paused = False  # Пауза
                LevelPixelView.stop_music(self)
            
        if key == arcade.key.ENTER:  # Перезапуск
            game_window = LevelPixelView()
            game_window.setup()
            self.window.show_view(game_window)

class PauseViewSpace(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
    def on_draw(self):
        self.width, self.height = self.window.get_size()   
        self.clear()
        player_sprite = self.game_view.car
        player_sprite.draw()
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.BABY_BLUE_EYES + (200,))
        arcade.draw_text("ПАУЗА", self.width / 2, self.height / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите Esc,чтобы продолжить",
                         self.width / 2,
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Нажмите Enter, чтобы начать заново",
                         self.width / 2,
                         self.height / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # Пауза
            self.window.show_view(self.game_view)
            arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
            if self.game_view.paused:
                self.game_view.music_player.play()
                self.game_view.paused = False  # Пауза
                LevelSpaceView.stop_music(self)
        if key == arcade.key.ENTER:  # Перезапуск
            game_window = LevelSpaceView()
            game_window.setup()
            self.window.show_view(game_window)

class PauseViewWorkout(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ANDROID_GREEN)
    def on_draw(self):
        self.width, self.height = self.window.get_size()   
        self.clear()
        player_sprite = self.game_view.car
        player_sprite.draw()
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.ANDROID_GREEN + (200,))
        arcade.draw_text("ПАУЗА", self.width / 2, self.height / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите Esc,чтобы продолжить",
                         self.width / 2,
                         self.height / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Нажмите Enter, чтобы начать заново",
                         self.width / 2,
                         self.height / 2 - 30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # Пауза
            self.window.show_view(self.game_view)
            arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
        if key == arcade.key.ENTER:  # Перезапуск
            game_window = LevelWorkoutView()
            game_window.setup()
            self.window.show_view(game_window)

class Car(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.speed = 90
        self.inner_lane = True
        self.last_speed_increase_time = time.time()
        self.k = 1
        self.crashed = False
        self.crash_time = None

    def handle_collision(self):
        self.crash_time = time.time()

    def update(self, window, start):
        if self.crashed:
            time_since_crash = time.time() - self.crash_time
            if time_since_crash <1:  # Stop the car for 1 second after the crash
                return
            else:
                self.crashed = True

        self.radians = math.radians(self.speed)

        window_width, window_height = window.get_size()  # get the current window size

        if self.inner_lane:
            self.center_x = window_width / 2 + math.cos(self.radians) * CIRCLE_RADIUS_INNER
            self.center_y = window_height / 2 + math.sin(self.radians) * CIRCLE_RADIUS_INNER
        else:
            self.center_x = window_width / 2 + math.cos(self.radians) * CIRCLE_RADIUS_OUTER
            self.center_y = window_height / 2 + math.sin(self.radians) * CIRCLE_RADIUS_OUTER

        # Increase speed every 5 seconds
        self.StartGame = start
        if self.StartGame:
            current_time = time.time()
            if current_time - self.last_speed_increase_time >= 5:
                self.k += 0.2
                self.last_speed_increase_time = current_time
            self.speed -= self.k


class Car_Computer(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.angle = 120
        self.inner_lane_bot = True

    def update(self, window, player_car):
        self.radians = math.radians(self.angle)
        window_width, window_height = window.get_size()

        MIN_DISTANCE = 50

        if self.inner_lane_bot and self.distance_to_sprite(player_car) > MIN_DISTANCE:
            self.center_x = window_width / 2 + math.cos(self.radians) * CIRCLE_RADIUS_INNER
            self.center_y = window_height / 2 + math.sin(self.radians) * CIRCLE_RADIUS_INNER
        elif not self.inner_lane_bot and self.distance_to_sprite(player_car) > MIN_DISTANCE:
            self.center_x = window_width / 2 + math.cos(self.radians) * CIRCLE_RADIUS_OUTER
            self.center_y = window_height / 2 + math.sin(self.radians) * CIRCLE_RADIUS_OUTER

        self.angle += 2

    def distance_to_sprite(self, sprite):
        return math.sqrt((self.center_x - sprite.center_x)**2 + (self.center_y - sprite.center_y)**2)


class Car_Level2(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.speed = 90
        self.inner_lane = True
        self.last_speed_increase_time = time.time()
        self.k = 1
        self.crashed = False
        self.crash_time = None
        
    def handle_collision(self):
        self.crash_time = time.time()

    def update(self, window, start):
        if self.crashed:
            time_since_crash = time.time() - self.crash_time
            if time_since_crash <1:  # Stop the car for 1 second after the crash
                return
            else:
                self.crashed = True
        window_width, window_height = window.get_size()
        self.radians = math.radians(self.speed)
        if window_height == 800:
            if self.inner_lane:
                self.center_x = window_width / 2 + math.cos(self.radians) * ELLIPSE_SEMIMAJOR_AXIS
                self.center_y = window_height / 2 + math.sin(self.radians) * ELLIPSE_SEMIMINOR_AXIS
            else:
                self.center_x = window_width / 2 + math.cos(self.radians) * ELLIPSE_SEMIMAJOR_AXIS_OUTER
                self.center_y = window_height / 2 + math.sin(self.radians) * ELLIPSE_SEMIMINOR_AXIS_OUTER
        else:
            if self.inner_lane:
                self.center_x = window_width / 2 + math.cos(self.radians) * (ELLIPSE_SEMIMAJOR_AXIS + 280)
                self.center_y = window_height / 2 + math.sin(self.radians) * (ELLIPSE_SEMIMINOR_AXIS + 10)
            else:
                self.center_x = window_width / 2 + math.cos(self.radians) * (ELLIPSE_SEMIMAJOR_AXIS_OUTER + 320)
                self.center_y = window_height / 2 + math.sin(self.radians) * (ELLIPSE_SEMIMINOR_AXIS_OUTER + 10)
        self.StartGame = start
        if self.StartGame:
            current_time = time.time()
            if current_time - self.last_speed_increase_time >= 5:
                self.k += 0.25
                self.last_speed_increase_time = current_time
            self.speed -= self.k

class Car_Computer_Level2(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.speed = 180
        self.inner_lane_bot = True
        

    def update(self, window, player_car):
        MIN_DISTANCE = 40 
        window_width, window_height = window.get_size()
        self.radians = math.radians(self.speed)
        if window_height == 800:
            if self.inner_lane_bot and self.distance_to_sprite(player_car) > MIN_DISTANCE:
                self.center_x = window_width / 2 + math.cos(self.radians) * ELLIPSE_SEMIMAJOR_AXIS_OUTER
                self.center_y = window_height / 2 + math.sin(self.radians) * ELLIPSE_SEMIMINOR_AXIS_OUTER
                
            elif not self.inner_lane_bot and self.distance_to_sprite(player_car) > MIN_DISTANCE:
                self.center_x = window_width / 2 + math.cos(self.radians) * ELLIPSE_SEMIMAJOR_AXIS
                self.center_y = window_height / 2 + math.sin(self.radians) * ELLIPSE_SEMIMINOR_AXIS
            self.speed += 2
        else:
            if self.inner_lane_bot and self.distance_to_sprite(player_car) > MIN_DISTANCE:
                self.center_x = window_width / 2 + math.cos(self.radians) * (ELLIPSE_SEMIMAJOR_AXIS_OUTER + 320)
                self.center_y = window_height / 2 + math.sin(self.radians) * (ELLIPSE_SEMIMINOR_AXIS_OUTER + 10)
                
            elif not self.inner_lane_bot and self.distance_to_sprite(player_car) > MIN_DISTANCE:
                self.center_x = window_width / 2 + math.cos(self.radians) * (ELLIPSE_SEMIMAJOR_AXIS + 280)
                self.center_y = window_height / 2 + math.sin(self.radians) * (ELLIPSE_SEMIMINOR_AXIS + 10) 
            self.speed += 2

    def distance_to_sprite(self, sprite):
        return math.sqrt((self.center_x - sprite.center_x)**2 + (self.center_y - sprite.center_y)**2)


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

def managerclear(self):
    self.manager.clear()
def uimanagerclear(self):
    self.uimanager.clear()


def check_for_collision(sprite1, sprite2):
        # Получаем координаты и размеры спрайтов
        x1, y1, width1, height1 = sprite1.position[0], sprite1.position[1], sprite1.width / 1.3, sprite1.height / 1.7
        x2, y2, width2, height2 = sprite2.position[0], sprite2.position[1], sprite2.width / 1.3, sprite2.height / 1.7
        # Проверяем столкновение по осям x и y
        if abs(x1 - x2) < (width1 / 2 + width2 / 2) and abs(y1 - y2) < (height1 / 2 + height2 / 2):
            return True
        else:
            return False

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
    window.set_icon(pyglet_load('Picture/Icon.ico'))
    zast_view = ZastavkaView()
    window.show_view(zast_view)
    arcade.run()
    

if __name__ == "__main__":
    main()