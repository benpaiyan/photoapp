import json
import os
import copy
import random
import math
import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, NumericProperty, DictProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from colorpickercustom import ColorPickerCustom
from filebrowser import FileBrowser
from configparser import ConfigParser

from generalcommands import to_bool
from generalelements import LimitedScatterLayout, MenuButton, NormalLabel, NormalPopup,NormalButton, ConfirmPopup, ScanningPopup, NormalDropDown, AlbumSortDropDown, PhotoRecycleViewButton, PhotoRecycleThumbWide, AsyncThumbnail, StencilViewTouch
from generalconstants import *
Logger.setLevel('DEBUG')  
Logger.debug("Debug logging enabled")  
from kivy.lang.builder import Builder
Builder.load_string("""
<ColorDropDown>:
    ColorPickerCustom:
        size_hint_y: None
        height: self.parent.width * 1.5
        size_hint_x: 1
        color: root.owner.collage_background
        on_color: root.owner.collage_background = self.color

<ResolutionDropDown>:
    MenuButton:
        text: 'Medium'
        on_release: 
            root.owner.resolution = self.text
            root.dismiss()
    MenuButton:
        text: 'High'
        on_release: 
            root.owner.resolution = self.text
            root.dismiss()
    MenuButton:
        text: 'Low'
        on_release: 
            root.owner.resolution = self.text
            root.dismiss()

<ExportAspectRatioDropDown>:
    MenuButton:
        text: '16:9 (Wider)'
        on_release:
            root.owner.aspect = 1.7778
            root.owner.aspect_text = '16:9'
            root.dismiss()
    MenuButton:
        text: '4:3 (Wide)'
        on_release:
            root.owner.aspect = 1.3333
            root.owner.aspect_text = '4:3'
            root.dismiss()
    MenuButton:
        text: '1:1 (Square)'
        on_release:
            root.owner.aspect = 1
            root.owner.aspect_text = '1:1'
            root.dismiss()
    MenuButton:
        text: '3:4 (Tall)'
        on_release:
            root.owner.aspect = 0.75
            root.owner.aspect_text = '3:4'
            root.dismiss()
    MenuButton:
        text: '9:16 (Taller)'
        on_release:
            root.owner.aspect = 0.5625
            root.owner.aspect_text = '9:16'
            root.dismiss()
            


<AddRemoveDropDown>:
    MenuButton:
        text: '  Add All  '
        on_release: 
            root.owner.add_all()
            root.dismiss()
    MenuButton:
        text: '  Remove Selected  '
        warn: True
        on_release: 
            root.owner.delete_selected()
            root.dismiss()
    MenuButton:
        text: '  Clear All  '
        warn: True
        on_release: 
            root.owner.clear_collage()
            root.dismiss()

<Collage>:
    canvas.before:
        Color:
            rgb: self.collage_background
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: 1, 1

<CollageTypeDropDown>:
    MenuButton:
        text: 'Photo Pile'
        on_release: 
            root.owner.collage_type = 'Pile'
            root.dismiss()
    MenuButton:
        text: 'Grid 1'
        on_release:
            root.owner.collage_type = '1'
            root.dismiss()
    MenuButton:
        text: 'Grid 2'
        on_release:
            root.owner.collage_type = '2'
            root.dismiss()
    MenuButton:
        text: 'Grid 3'
        on_release:
            root.owner.collage_type = '3'
            root.dismiss()
    MenuButton:
        text: 'Grid 2x2'
        on_release: 
            root.owner.collage_type = '2x2'
            root.dismiss()
    MenuButton:
        text: 'Grid 2:1:2'
        on_release:
            root.owner.collage_type = '5'
            root.dismiss()
    MenuButton:
        text: 'Grid 2x3'
        on_release:
            root.owner.collage_type = '2x3'
            root.dismiss()
    MenuButton:
        text: 'Grid 3x2'
        on_release:
            root.owner.collage_type = '3x2'
            root.dismiss()
    MenuButton:
        text: 'Grid 3:1:3'
        on_release:
            root.owner.collage_type = '7'
            root.dismiss()
    MenuButton:
        text: 'Grid 3x3'
        on_release:
            root.owner.collage_type = '3x3'
            root.dismiss()

<CollageScreen>:
    canvas.before:
        Color:
            rgba: app.theme.background
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        MainHeader:
            NormalButton:
                text: 'Back'
                on_release: root.back()
            HeaderLabel:
                text: root.current_page_key
            # InfoLabel:
            # DatabaseLabel:
            # InfoButton:
            # SettingsButton:
        BoxLayout:
            orientation: 'horizontal'
            SplitterPanelLeft:
                id: leftpanel
                #width: app.leftpanel_width
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: .25
                    Header:
                        size_hint_y: None
                        height: app.button_scale
                        ShortLabel:
                            text: 'Events:'
                        MenuStarterButtonWide:
                            id: sortButton
                            text: root.selected_event
                            on_release: root.event_dropdown.open(self)
                        # ReverseToggle:
                        #     id: sortReverseButton
                        #     state: root.sort_reverse_button
                        #     on_release: root.resort_reverse(self.state)
                    # ScrollView:
                    #     size_hint_y: None
                    #     bar_width: 5
                    #     scroll_type: ['bars', 'content']
                    # GridLayout:
                    #     id: eventListBox
                    #     cols: 1
                    #     height: app.button_scale
                    PhotoListRecycleView:
                        size_hint: 1, 1
                        id: albumContainer
                        viewclass: 'PhotoRecycleThumb'
                        scroll_distance: 10
                        scroll_timeout: 200
                        bar_width: int(app.button_scale * .5)
                        bar_color: app.theme.scroller_selected
                        bar_inactive_color: app.theme.scroller
                        scroll_type: ['bars', 'content']
                        SelectableRecycleGrid:
                            cols: int((self.width - app.button_scale) / (app.button_scale * 3))
                            multiselect: False
                            spacing: 10
                            id: album
                            default_size: (app.button_scale * 3), (app.button_scale * 3)
            MainArea:
                size_hint: .75, 1
                orientation: 'vertical'
                AnchorLayout:
                    canvas.before:
                        Color:
                            rgba: 1-root.collage_background[0], 1-root.collage_background[1], 1-root.collage_background[2], .333
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    anchor_x: 'center'
                    anchor_y: 'center'
                    RelativeLayout:
                        size_hint: None, None
                        height: self.parent.height if (self.parent.width >= (self.parent.height * root.aspect)) else (self.parent.width / root.aspect)
                        width: int(self.height * root.aspect)
                        id: collageHolder
                Header:
                    size_hint_y: None
                    height: app.button_scale
                    NormalToggle:
                        id: moveButton
                        text: '  Move  '
                        on_press: root.change_transform('move')
                        group: 'transform'
                        state: 'down'
                        size_hint_y: None
                        width: 0 if app.simple_interface else self.texture_size[0] + 20
                        opacity: 0 if app.simple_interface else 1
                        disabled: True if app.simple_interface else False
                    NormalToggle:
                        id: rotateButton
                        text: '  Rotate/Scale  '
                        on_press: root.change_transform('rotscale')
                        group: 'transform'
                        width: 0 if app.simple_interface else self.texture_size[0] + 20
                        opacity: 0 if app.simple_interface else 1
                        disabled: True if app.simple_interface else False
                    Label:
                        size_hint_x: None
                        width: 0 if app.simple_interface else app.button_scale * 2
                    MenuStarterButtonWide:
                        text: '  Add/Remove  '
                        on_release: root.add_remove.open(self)
                    MenuStarterButtonWide:
                        text: '  Background Color  '
                        on_release: root.color_select.open(self)
                    # MenuStarterButtonWide:
                    #     text: '  Shape: '+str(root.aspect_text)+'  '
                    #     on_release: root.aspect_select.open(self)
                    # MenuStarterButtonWide:
                    #     text: '  Export Size: '+root.resolution+'  '
                    #     on_release: root.resolution_select.open(self)
                    MenuStarterButtonWide:
                        id: collageTypeButton
                        text: '  Collage Type: '+root.collage_type+'  '
                        on_release: root.collage_type_select.open(self)
                    NormalButton:
                        id: saveButton
                        text: "Save Work"
                        on_release: root.save_album()
                    NormalButton:
                        text: '  Export  '
                        on_release: root.export()
                BoxLayout:
                    size_hint_y: None
                    height: app.button_scale
                    spacing: dp(20)
                    padding: dp(10), 0
                    NormalButton:
                        text: '<< Prev'
                        on_release: root.show_prev_collage()
                    NormalLabel:
                        text: root.page_status
                        size_hint_x: None
                        width: dp(120)
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.size

                    NormalButton:
                        text: 'Next >>'
                        on_release: root.show_next_collage()


<ScatterImage>:
    AsyncThumbnail:
        canvas.after:
            Color:
                rgba: 0, 1, 0, (.2 if root.selected else 0)
            Rectangle:
                size: self.size
                pos: self.pos
        id: image
        size_hint: 1, 1
        photoinfo: root.photoinfo
        mirror: root.mirror
        disable_rotate: True
        #angle: root.image_angle
        loadfullsize: root.loadfullsize
        lowmem: root.lowmem
        source: root.source

<GridImage>: #GANESH
    canvas.before:
        Color: 
            rgba: 1, 1, 1, .5 if root.show_guides else 0
        Rectangle:
            pos: [root.pos[0] + (root.width/20), root.pos[1] + (root.width/20)]
            size: [root.size[0] - (root.width/10), root.size[1] - (root.width/10)]

<GridCollage3>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
    GridImageWithLayers:
    
<GridCollage2>:
    orientation: 'horizontal'
    GridImageWithLayers:
    GridImageWithLayers:
    
<GridCollage1>:
    orientation: 'horizontal'
    GridImageWithLayers:


<GridCollage2x2>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:

<GridCollage2x3>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:

        
<GridCollage5>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
    GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        
<GridCollage7>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:
    GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:
        
<GridImageWithLayers>:   #GANESH
    Image:
        id: background_layer
        # source: "data/bg2.jpeg"
        source: root.background_source
        # size: self.parent.size
        keep_ratio: False
        allow_stretch: False
        # size_hint: (1, 1)
        # pos_hint: {"center_x": 0.5, "center_y": 0.5}
        # pos: self.parent.pos
        # z_index: 3  # Lowest layer

    GridImage:
        # id: grid_image
        # source: "grid_image.png"
        # size_hint: (0.9, 0.9)
        # pos_hint: {"center_x": 0.5, "center_y": 0.5}
        # # z_index: 2  # Middle layer
    Image:
        id: foreground_layer
        # source: "data/l2.png"
        source: root.foreground_source
        # size: self.parent.size
        keep_ratio: False
        allow_stretch: False
        # size_hint: (1, 1)
        # pos_hint: {"center_x": 0.5, "center_y": 0.5}
        # # pos: self.parent.pos
        # z_index: 1  # Top layer




<GridCollage3x2>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:

<GridCollage3x3>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:
    BoxLayout:
        orientation: 'vertical'
        GridImageWithLayers:
        GridImageWithLayers:
        GridImageWithLayers:

""")


class GridImage(StencilViewTouch):
    show_guides = BooleanProperty(True)


class ScatterImage(LimitedScatterLayout):
    source = StringProperty()
    mirror = BooleanProperty(False)
    loadfullsize = BooleanProperty(False)
    image_angle = NumericProperty(0)
    photoinfo = ListProperty()
    fake_touch = ObjectProperty(allownone=True)
    owner = ObjectProperty()
    selected = BooleanProperty(False)
    lowmem = BooleanProperty(False)
    aspect = NumericProperty(1)

    def set_transform_mode(self, transform_mode):
        Logger.debug("photomanager screencollege scatterImage.set_transform_mode")
        if transform_mode == 'rotscale':
            self.do_rotation = True
            self.do_scale = True
            self.do_translation = False
        elif transform_mode == 'rotate':
            self.do_rotation = True
            self.do_scale = False
            self.do_translation = False
        elif transform_mode == 'scale':
            self.do_rotation = False
            self.do_scale = True
            self.do_translation = False
        else:
            self.do_rotation = True
            self.do_scale = True
            self.do_translation = True
        # if self.owner and hasattr(self.owner, "owner") and hasattr(self.owner.owner, "update_album_json"):
        #     # owner = ScatterCollage, owner.owner = CollageScreen
        #     self.owner.owner.update_album_json()

    def on_scale(self, *_):
        Logger.debug("photomanager screencollege scatterImage.on_scale")
        app = App.get_running_app()
        if (self.width * self.scale) > app.thumbsize:
            self.loadfullsize = True

    def on_touch_down(self, touch):
        Logger.debug("photomanager screencollege scatterImage.on_touch_down")
        self.set_transform_mode(self.owner.transform_mode)
        if self.collide_point(*touch.pos):
            self.owner.deselect_images()
            self.selected = True
        super().on_touch_down(touch)

    def on_touch_up(self, touch):
        Logger.debug("photomanager screencollege scatterImage.on_touch_up")
        if self.fake_touch:
            self._touches.remove(self.fake_touch)
            self.fake_touch = None
        super().on_touch_up(touch)
        # if self.owner and hasattr(self.owner, "owner") and hasattr(self.owner.owner, "update_album_json"):
        #     # owner = ScatterCollage, owner.owner = CollageScreen
        #     self.owner.owner.update_album_json()

    def transform_with_touch(self, touch):
        Logger.debug("photomanager screencollege scatterImage.transform_with_touch")
        if not self.selected:
            return
        right_click = False
        if hasattr(touch, 'button'):
            if touch.button == 'right':
                right_click = True
        if ((not self.do_translation_x and not self.do_translation_y) or right_click) and (self.do_rotation or self.do_scale) and len(self._touches) == 1:
            #Translation is disabled, no need for multitouch to rotate/scale, so if not multitouch, add a new fake touch point to the center of the widget
            self.fake_touch = copy.copy(touch)
            self.fake_touch.pos = self.center
            self._last_touch_pos[self.fake_touch] = self.fake_touch.pos
            self._touches.insert(0, self.fake_touch)
        super().transform_with_touch(touch)


class CollageTypeDropDown(NormalDropDown):
    Logger.debug("photomanager screencollege CollageTypeDropDown")
    owner = ObjectProperty()


class ColorDropDown(NormalDropDown):
    Logger.debug("photomanager screencollege ColorDropDown")
    owner = ObjectProperty()


class ResolutionDropDown(NormalDropDown):
    Logger.debug("photomanager screencollege ResolutionDropDown")
    owner = ObjectProperty()


class ExportAspectRatioDropDown(NormalDropDown):
    Logger.debug("photomanager screencollege ExportAspectRatioDropDown")
    owner = ObjectProperty()



class AddRemoveDropDown(NormalDropDown):
    Logger.debug("photomanager screencollege AddRemoveDropDown")
    owner = ObjectProperty()


class Collage(Widget):
    Logger.debug("photomanager screencollege Collage")
    collage_background = ListProperty([0, 0, 0, 1])
    images = []
    transform_mode = StringProperty('')
    show_guides = BooleanProperty(True)
    owner = ObjectProperty(None)

    def show_guides(self, show):
        pass

    def drop_image(self, fullpath, position, aspect=1):
        pass

    def clear(self):
        pass

    def deselect_images(self):
        pass

    def delete_selected(self):
        pass

    def add_photos(self, photos):
        pass


class ScatterCollage(Collage, StencilViewTouch):
    def clear(self):
        Logger.debug("photomanager screencollege scatterCollage.clear")
        self.clear_widgets()
        self.images = []

    def reset_background(self):
        Logger.debug("photomanager screencollege scatterCollage.reset_background")
        self.collage_background = [0, 0, 0, 1]

    def delete_selected(self):
        Logger.debug("photomanager screencollege scatterCollage.delete_selected")
        for image in self.children:
            if image.selected:
                self.remove_widget(image)
            if image in self.images:
                self.images.remove(image)
        # if self.owner and hasattr(self.owner, "owner") and hasattr(self.owner.owner, "update_album_json"):
        #     # owner = ScatterCollage, owner.owner = CollageScreen
        #     self.owner.owner.update_album_json()

    def deselect_images(self):
        Logger.debug("photomanager screencollege scatterCollage.deselect_images")
        for image in self.children:
            image.selected = False

    def add_collage_image(self, fullpath, position, size=0.5, angle=0, lowmem=False, aspect=1):
        Logger.debug("photomanager screencollege scatterCollage.add_collage_image")
        if not lowmem:
            if len(self.images) > 8:
                lowmem = True
        if self.collide_point(*position):
            self.deselect_images()
            app = App.get_running_app()
            photoinfo = app.database_exists(fullpath)
            file = os.path.join(photoinfo[2], photoinfo[0])
            orientation = photoinfo[13]
            if orientation == 3 or orientation == 4:
                angle_offset = 180
            elif orientation == 5 or orientation == 6:
                angle_offset = 270
            elif orientation == 7 or orientation == 8:
                angle_offset = 90
            else:
                angle_offset = 0
            if orientation in [2, 4, 5, 7]:
                mirror = True
            else:
                mirror = False
            width = self.width
            image_holder = ScatterImage(owner=self, source=file, rotation=angle+angle_offset, mirror=mirror, image_angle=0, photoinfo=photoinfo, lowmem=lowmem, aspect=aspect)
            image_holder.scale = size
            image_holder.selected = True
            if aspect < 1:
                image_holder.width = width * aspect
                image_holder.height = width
            else:
                image_holder.width = width
                image_holder.height = width / aspect
            self.images.append(image_holder)
            image_holder.pos = (position[0] - (width * size / 2), position[1] - (width * size / 2))
            self.add_widget(image_holder)
            # if self.owner and hasattr(self.owner, "owner") and hasattr(self.owner.owner, "update_album_json"):
            #     Clock.schedule_once(lambda dt: self.owner.owner.update_album_json(), 0.1)

    def drop_image(self, fullpath, position, aspect=1):
        Logger.debug("photomanager screencollege scatterCollage.drop_image")
        self.add_collage_image(fullpath, position, aspect=aspect)

    def add_photos(self, photos):
        Logger.debug("photomanager screencollege scatterCollage.add_photos")
        #adds all photos to the collage using a fimonacci spiral pattern
        size = (1 / (len(photos) ** 0.5))  #average scale of photo
        random.shuffle(photos)

        tau = (1+5**0.5)/2
        inc = (2-tau)*2*math.pi
        theta = 0

        max_x = 0
        max_y = 0
        coords = []
        offset_scale = .5
        app = App.get_running_app()
        app.message("Added "+str(len(photos))+" images.")
        #Generate basis coordinates and determine min/max
        for index in range(0, len(photos)):
            offset = (random.random()*offset_scale) - (.5*offset_scale)  #random angle variation
            r = index**0.5
            theta = theta + inc + offset
            pos_x = 0.5 + r*math.cos(theta)
            if abs(pos_x) > max_x:
                max_x = abs(pos_x)
            pos_y = 0.5 + r*math.sin(theta)
            if abs(pos_y) > max_y:
                max_y = abs(pos_y)
            coords.append((pos_x, pos_y))

        #add photos to collage
        for index, photo in enumerate(photos):
            rand_angle = random.randint(-33, 33)
            pos_x, pos_y = coords[index]
            #scale points down by max size
            pos_x = pos_x / max_x
            pos_y = pos_y / max_y
            #scale points down to prevent photos overlapping edges
            pos_x = pos_x * (1 - (size/2))
            pos_y = pos_y * (1 - (size/2))
            #convert to kivy's coordinate system
            pos_x = (pos_x + 1) / 2
            pos_y = (pos_y + 1) / 2
            #offset points to correct for photo size
            pos_x = pos_x - (size / 2)
            pos_y = pos_y - (size / 2)
            position = (self.width * pos_x, self.height * pos_y)

            #forces lowmem mode if more than a certain number of photos
            if len(photos) > 8:
                lowmem = True
            else:
                lowmem = False
            self.add_collage_image(photo[0], position, size=size, angle=rand_angle, lowmem=lowmem)
        self.deselect_images()


class GridCollage(Collage, BoxLayout):
    image_widgets = []

    def show_guides(self, show):
        Logger.debug("photomanager screencollege GridCollage.show_guides")
        for child in self.walk(restrict=True, loopback=True):
            if isinstance(child, GridImage):
                child.show_guides = show

    def drop_image(self, fullpath, position, aspect=1):
        Logger.debug("photomanager screencollege GridCollage.drop_image")
        for child in self.walk(restrict=True, loopback=True):
            #check for GridImage children, and find which one the position collides with.
            if isinstance(child, GridImage):
                # if child.collide_point(*position): #ORIGINAL
                    # the position is absolute X,Y but child position is(0,0) due to  relativelayout
                    # so we need to compare the collide point with the parent's absolute position .
                if child.parent.collide_point(*position):
                    self.add_collage_image(child, fullpath, aspect=aspect)
                    return

    # def add_collage_image(self, widget, fullpath, size=1, angle=0, lowmem=False, aspect=1):
    #     # self.owner.update_album_ini()
    #     Logger.debug("photomanager screencollege GridCollage.add_collage_image")
    #     widget.clear_widgets()
    #     self.images = [img for img in self.images if img.parent != widget]
    #     if not lowmem:
    #         if len(self.images) > 8:
    #             lowmem = True
    #     self.deselect_images()
    #     app = App.get_running_app()
    #     photoinfo = app.database_exists(fullpath)
    #     file = os.path.join(photoinfo[2], photoinfo[0])
    #     orientation = photoinfo[13]
    #     if orientation == 3 or orientation == 4:
    #         angle_offset = 180
    #     elif orientation == 5 or orientation == 6:
    #         angle_offset = 270
    #     elif orientation == 7 or orientation == 8:
    #         angle_offset = 90
    #     else:
    #         angle_offset = 0
    #     if orientation in [2, 4, 5, 7]:
    #         mirror = True
    #     else:
    #         mirror = False
    #     image_holder = ScatterImage(owner=self, source=file, rotation=angle+angle_offset, mirror=mirror, image_angle=0, photoinfo=photoinfo, lowmem=lowmem, aspect=aspect)
    #     image_holder.scale = size
    #     image_holder.selected = True
    #     if angle_offset in [90, 270]:
    #         image_holder.width = widget.height
    #         image_holder.height = widget.width
    #     else:
    #         image_holder.width = widget.width
    #         image_holder.height = widget.height
    #     image_holder.pos = widget.pos
    #     widget.add_widget(image_holder)
    #     self.images.append(image_holder)
    #     self.owner.update_album_json()
        
    def add_collage_image1(self, widget, fullpath, size=1, angle=0, lowmem=False, aspect=1, position=None):
        Logger.debug("photomanager screencollege GridCollage.add_collage_image")
        Logger.debug(f" - adding: {fullpath}")
        Logger.debug(f" - position: {position}, size: {size}, angle: {angle}, aspect: {aspect}")

        widget.clear_widgets()
        self.images = [img for img in self.images if img.parent != widget]
        if not lowmem and len(self.images) > 8:
            lowmem = True

        self.deselect_images()
        app = App.get_running_app()
        if "organized_folder" in fullpath:
            try:
                rel_path = fullpath.split("organized_folder" + os.sep, 1)[1].replace("\\", "/")
                photoinfo = app.database_exists(rel_path)
            except IndexError:
                Logger.warning(f"⚠️ Could not parse relative path from: {fullpath}")
                return
        else:
            Logger.warning(f"⚠️ Path does not contain 'organized_folder': {fullpath}")
            return
        # photoinfo = app.database_exists(fullpath)
        file = os.path.join(photoinfo[2], photoinfo[0])
        orientation = photoinfo[13]
        angle_offset = {3: 180, 4: 180, 5: 270, 6: 270, 7: 90, 8: 90}.get(orientation, 0)
        mirror = orientation in [2, 4, 5, 7]

        image_holder = ScatterImage(
            owner=self,
            source=file,
            rotation=angle + angle_offset,
            mirror=mirror,
            image_angle=0,
            photoinfo=photoinfo,
            lowmem=lowmem,
            aspect=aspect
        )
        image_holder.scale = size
        image_holder.selected = True

        image_holder.size = widget.size
        image_holder.center = widget.center  # ✅ Ensures it is visible and centered

        widget.add_widget(image_holder)
        self.images.append(image_holder)
        # self.owner.update_album_json()
        
    def add_collage_image(self, widget, fullpath, size=1, angle=0, lowmem=False, aspect=1, position=None):
        Logger.debug("photomanager screencollege GridCollage.add_collage_image")
        Logger.debug(f" - adding: {fullpath}")
        Logger.debug(f" - position: {position}, size: {size}, angle: {angle}, aspect: {aspect}")

        widget.clear_widgets()
        self.images = [img for img in self.images if img.parent != widget]
        if not lowmem and len(self.images) > 8:
            lowmem = True

        self.deselect_images()
        app = App.get_running_app()
        photoinfo = app.database_exists(fullpath)
        file = os.path.join(photoinfo[2], photoinfo[0])
        orientation = photoinfo[13]
        angle_offset = {3: 180, 4: 180, 5: 270, 6: 270, 7: 90, 8: 90}.get(orientation, 0)
        mirror = orientation in [2, 4, 5, 7]

        image_holder = ScatterImage(
            owner=self,
            source=file,
            rotation=angle + angle_offset,
            mirror=mirror,
            image_angle=0,
            photoinfo=photoinfo,
            lowmem=lowmem,
            aspect=aspect
        )
        image_holder.scale = size
        image_holder.selected = True

        image_holder.size = widget.size
        image_holder.center = widget.center  # ✅ Ensures it is visible and centered

        widget.add_widget(image_holder)
        self.images.append(image_holder)
        # self.owner.update_album_json()

    def clear(self):
        Logger.debug("photomanager screencollege GridCollage.clear")
        for child in self.walk(restrict=True, loopback=True):
            if isinstance(child, GridImage):
                child.clear_widgets()
        self.images = []
        # self.owner.update_album_json()

    def reset_background(self):
        Logger.debug("photomanager screencollege GridCollage.reset_background")
        self.collage_background = [0, 0, 0, 1]

    def deselect_images(self):
        Logger.debug("photomanager screencollege GridCollage.deselect_images")
        for child in self.walk(restrict=True, loopback=True):
            if isinstance(child, GridImage):
                for image in child.children:
                    image.selected = False

    def delete_selected(self):
        Logger.debug("photomanager screencollege GridCollage.delete_selected")
        for child in self.walk(restrict=True, loopback=True):
            if isinstance(child, GridImage):
                for image in child.children:
                    if image.selected:
                        child.clear_widgets()
                        break
        # self.owner.update_album_json()

    def add_photos(self, photos):
        Logger.debug("photomanager screencollege GridCollage.add_photos")
        image_slots = []
        for child in self.walk(restrict=True, loopback=True):
            if isinstance(child, GridImage):
                image_slots.append(child)

        #forces lowmem mode if more than a certain number of photos
        if len(image_slots) > 8:
            lowmem = True
        else:
            lowmem = False

        random.shuffle(photos)
        for image_slot in image_slots:
            if photos:
                photo = photos.pop(0)
                self.add_collage_image(image_slot, photo[0], lowmem=lowmem)
        self.deselect_images()
        # self.owner.update_album_json()


class GridCollage3(GridCollage):
    Logger.debug("photomanager screencollege GridCollage3")
    pass
class GridCollage2(GridCollage):
    Logger.debug("photomanager screencollege GridCollage2")
    pass
class GridCollage1(GridCollage):
    Logger.debug("photomanager screencollege GridCollage1")
    pass
# class GridImageWithLayers(RelativeLayout):
#     Logger.debug("photomanager screencollege GridCollage3")
#     pass
class GridImageWithLayers(RelativeLayout):
    foreground_source = StringProperty("")
    background_source = StringProperty("")
    def on_kv_post(self, base_widget):
        self.apply_template()

    def apply_template(self):
        app = App.get_running_app()
        project_name = app.selected_project if hasattr(app, "selected_project") else "Default Project"
        album_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.json")
        template_name = getattr(app, "template", "Default Template 1")  # fallback
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        template_out_path = os.path.join(album_folder, f"{template_name}.json")
        with open(template_out_path, "r") as f:
            data = json.load(f)
            template_name = data.get("album", {}).get("template", "")
        self.load_template_config(template_name)

    def load_template_config(self, template_name):
        template_dir = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", "Templates")
        template_file = os.path.join(template_dir, f"{template_name}.json")

        if os.path.exists(template_file):
            with open(template_file, "r") as f:
                config = json.load(f)
                self.foreground_source = config.get("foreground_layer", "")
                self.background_source = config.get("background_layer", "")
        else:
            print(f"⚠️ Template file not found: {template_file}")

class GridCollage2x2(GridCollage):
    Logger.debug("photomanager screencollege GridCollage2x2")
    pass


class GridCollage2x3(GridCollage):
    Logger.debug("photomanager screencollege GridCollage2x3")
    pass


class GridCollage3x3(GridCollage):
    Logger.debug("photomanager screencollege GridCollage3x3")
    pass


class GridCollage3x2(GridCollage):
    Logger.debug("photomanager screencollege GridCollage3x2")
    pass


class GridCollage5(GridCollage):
    Logger.debug("photomanager screencollege GridCollage5")
    pass
class GridCollage7(GridCollage):
    Logger.debug("photomanager screencollege GridCollage7")
    pass


class CollageScreen(Screen):
    #Display variables
    selected = StringProperty('')  #The current folder/tag being displayed
    type = StringProperty('None')  #'Folder', 'Tag'
    target = StringProperty()  #The identifier of the folder/tag that is being viewed
    photos = []  #Photoinfo of all photos in the album
    collage_type = StringProperty('Pile')

    sort_reverse_button = StringProperty('normal')
    resolution = StringProperty('Medium')
    # template =  StringProperty('Default Template')
    aspect = NumericProperty(1.3333)
    aspect_text = StringProperty('4:3')
    filename = StringProperty('')
    export_scale = 1
    collage_background = ListProperty([0, 0, 0, 1])

    #Widget holder variables
    sort_dropdown = ObjectProperty()  #Holder for the sort method dropdown menu
    event_dropdown =  ObjectProperty()
    popup = None  #Holder for the screen's popup dialog
    resolution_select = ObjectProperty()
    color_select = ObjectProperty()
    aspect_select = ObjectProperty()
    collage_type_select = ObjectProperty()
    add_remove = ObjectProperty()
    collage = ObjectProperty()
    exportthread = ObjectProperty()
    current_page = NumericProperty(1)
    total_pages = NumericProperty(1)
    collage_pages = ListProperty([]) 
    collages = []       # New: list of all collage pages
    current_collage_index = 0  # Track which page is visible
    collage_types = ListProperty([])  
    page_status = StringProperty("Page 1 of 1")
    expanded_events = BooleanProperty(True)
    expanded_events_root = True
    expanded_individual_events = set()
    page_keys = ListProperty([])  # store page key order
    current_page_key = StringProperty("Create Album")
    autofilled_pages = set()

    




    #Variables relating to the photo list view on the left
    sort_method = StringProperty('Name')  #Current album sort method
    selected_event = StringProperty('All')
    sort_reverse = BooleanProperty(False)

    from_database = BooleanProperty(False)  #indicates if the database screen switched to this screen

    def back(self, *_):
        Logger.debug("photomanager screencollege CollageScreen.back")
        app = App.get_running_app()
        if self.from_database:
            app.show_menu() #COLLAGE
        else:
            app.show_menu()

    def rescale_screen(self):
        Logger.debug("photomanager screencollege CollageScreen.rescale_screen")
        app = App.get_running_app()
        self.ids['leftpanel'].width = app.left_panel_width()

    def on_collage_background(self, *_):
        Logger.debug("photomanager screencollege CollageScreen.on_collage_background")
        self.collage.collage_background = self.collage_background
        # self.update_album_json()

    def deselect_images(self):
        Logger.debug("photomanager screencollege CollageScreen.deselect_images")
        self.collage.deselect_images()

    def delete_selected(self):
        Logger.debug("photomanager screencollege CollageScreen.delete_selected")
        self.collage.delete_selected()
        # self.update_album_json()

    def clear_collage(self):
        Logger.debug("photomanager screencollege CollageScreen.clear_collage")
        self.collage.clear()

        # self.update_album_json()
        
    def autofill_current_page(self, index):
        Logger.debug(f"Autofilling page {index + 1} on demand")

        collage = self.collages[index]
        if not isinstance(collage, GridCollage):
            return

        grid_slots = [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]
        if not grid_slots:
            return

        # ✅ Build a photo list from all good photos sorted by event
        all_photos = []
        for event_name in self.get_event_names():
            raw_event = event_name
            if "(" in event_name and event_name.endswith(")"):
                raw_event = event_name.rsplit("(", 1)[-1].rstrip(")")
            event_photos = [p for p in self.photos if p[24] == raw_event and str(p[25]).lower() == 'good']
            all_photos.extend(event_photos)

        # ✅ Keep track of already used photo paths across all pages (in memory)
        if not hasattr(self, "_in_session_used_paths"):
            self._in_session_used_paths = set()

        photos_to_place = [p for p in all_photos if os.path.join(p[2], p[0]) not in self._in_session_used_paths]

        Logger.debug(f"Placing {len(photos_to_place)} available images on page {index + 1}")

        for slot in grid_slots:
            if not photos_to_place:
                break
            photo = photos_to_place.pop(0)
            photo_path = os.path.join(photo[2], photo[0])
            # collage.add_collage_image1(slot, photo_path, aspect=1)
            if hasattr(collage, 'add_collage_image1'):
                collage.add_collage_image1(slot, photo_path, aspect=1)
            else:
                collage.add_collage_image(slot, photo_path, aspect=1)
            self._in_session_used_paths.add(photo_path)

        self.deselect_images()
        # self.update_album_json()
        # self.used_photo_paths = self.get_used_photo_paths()


        
    # def autofill_album_pages_by_event(self):
    #     Logger.debug("photomanager screencollege autofill_album_pages_by_event")

    #     app = App.get_running_app()
    #     all_slots = []

    #     # Collect all grid slots across pages
    #     for collage in self.collages:
    #         if isinstance(collage, GridCollage):
    #             grid_slots = [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]
    #             all_slots.extend([(collage, slot) for slot in grid_slots])
    #         elif isinstance(collage, ScatterCollage):
    #             continue  # Optional: handle ScatterCollage if needed

    #     # Get photos grouped by event (preserve order)
    #     photos_to_place = []
    #     ordered_events = self.get_event_names()  # already sorted

    #     for event_name in ordered_events:
    #         # Un-rename to get the original event key from photos
    #         raw_event = event_name
    #         if "(" in event_name and event_name.endswith(")"):
    #             raw_event = event_name.rsplit("(", 1)[-1].rstrip(")")
            
    #         event_photos = [p for p in self.photos if p[24] == raw_event and str(p[25]).lower() == 'good']
    #         photos_to_place.extend(event_photos)

    #     Logger.debug(f"Total good photos to place: {len(photos_to_place)}")

    #     # Place into available slots
    #     photo_idx = 0
    #     lowmem = len(photos_to_place) > 8 
    #     for collage, slot in all_slots:
    #         if photo_idx >= len(photos_to_place):
    #             break
    #         photo = photos_to_place[photo_idx]
    #         collage.add_collage_image(slot, photo[0], lowmem=lowmem)
    #         photo_idx += 1

    #     Logger.info(f"✅ Autofilled {photo_idx} photos into collage slots.")

    def add_all(self):
        Logger.debug("photomanager screencollege CollageScreen.add_all")
        good_photos = [photo for photo in self.photos if str(photo[25]).lower() == 'good']
        # self.collage.add_photos(list(self.photos))
        self.collage.add_photos(good_photos)
        # retry_count = [0]
        # def wait_for_positions(_):
        #     retry_count[0] += 1
        #     all_valid = True
        #     for img in self.collage.images:
        #         if isinstance(self.collage, ScatterCollage):
        #             if list(img.pos) == [0.0, 0.0]:
        #                 all_valid = False
        #                 Logger.warning(f"[WAIT] Image still not positioned: {img.source}")
        #                 break

        #     if all_valid or retry_count[0] > 20:
        #         Logger.info(f"[SAVE] Proceeding to save album.json (after {retry_count[0]} retries)")
        #         self.update_album_json()
        #     else:
        #         Clock.schedule_once(wait_for_positions, 0.1)  # Retry after a frame

        # Clock.schedule_once(wait_for_positions, 0.1)
        # # self.update_album_json()

    def export(self):
        Logger.debug("photomanager screencollege CollageScreen.export")
        self.deselect_images()
        self.filechooser_popup()

    # def filechooser_popup(self): #OLD
    #     Logger.debug("photomanager screencollege CollageScreen.filechooser_popup")
    #     app = App.get_running_app()
    #     content = FileBrowser(ok_text='Export', path=app.last_browse_folder, file_editable=True, export_mode=True, file='collage.jpg')
    #     content.bind(on_cancel=self.dismiss_popup)
    #     content.bind(on_ok=self.export_check)
    #     self.popup = NormalPopup(title="Select File To Export To", content=content, size_hint=(0.9, 0.9))
    #     self.popup.open()
    
    def filechooser_popup(self): #NEW
        Logger.debug("photomanager screencollege CollageScreen.select_export_folder")
        app = App.get_running_app()
        content = FileBrowser(directory_select=True, file_editable=False, export_mode=False,ok_text="Export")
        content.bind(on_cancel=self.dismiss_popup)
        content.bind(on_ok=self.export_all_pages)
        self.popup = NormalPopup(title="Select Folder to Export Album", content=content, size_hint=(0.9, 0.9))
        self.popup.open()
        
    def export_all_pages(self, instance): #NEW
        Logger.debug("photomanager screencollege CollageScreen.export_all_pages")
        path = instance.path
        self.dismiss_popup()

        app = App.get_running_app()
        self.export_folder = path  # Store folder path for export
        self.popup = ScanningPopup(title='Exporting Album Pages...', auto_dismiss=False, size_hint=(None, None), size=(app.popup_x, app.button_scale * 4))
        self.popup.scanning_text = ''
        self.popup.button_text = 'Ok'
        self.popup.open()

        self.export_page_index = 0  # Start from first page
        Clock.schedule_once(self._export_next_page, 0.1)

        
        
    def _export_next_page(self, *_): #NEW
        if self.export_page_index >= len(self.collages):
            self.popup.dismiss()
            self.popup = None
            App.get_running_app().message("Exported all album pages successfully.")
            return

        self.collage = self.collages[self.export_page_index]
        self.collage.deselect_images()

        if self.resolution == 'High':
            self.export_scale = 4
        elif self.resolution == 'Low':
            self.export_scale = 1
        else:
            self.export_scale = 2

        self.filename = os.path.join(self.export_folder, f"page{self.export_page_index + 1}.jpg")

        self.export_process(callback=self._export_next_page)
        self.export_page_index += 1
        
    def export_process(self, callback=None, *_):#NEW
        Logger.debug("photomanager screencollege CollageScreen.export_process")
        scanning = 0
        check_images = []

        if self.export_scale > 1:
            for image in self.collage.images:
                scanning += 10
                self.popup.scanning_percentage = scanning % 100
                async_image = image.children[0].children[0]
                if not async_image.is_full_size:
                    async_image.loadfullsize = True
                    async_image._load_fullsize()
                    check_images.append(async_image)

        def wait_for_fullsize(dt):#NEW
            nonlocal check_images
            for img in check_images[:]:
                if img.is_full_size:
                    check_images.remove(img)

            if check_images:
                Clock.schedule_once(wait_for_fullsize, 0.1)
            else:
                self.collage.show_guides(False)
                Clock.schedule_once(lambda dt: self.export_collage_as_image(callback), 0.1)

        wait_for_fullsize(0)




    def export_check(self, *_): #COLLAGE #OLD
        Logger.debug("photomanager screencollege CollageScreen.export_check")
        popup = self.popup
        if popup:
            path = popup.content.path
            app = App.get_running_app()
            app.last_browse_folder = path
            file = popup.content.file
            self.dismiss_popup()
            if not file.lower().endswith('.jpg'):
                file = file+'.jpg'
            self.filename = os.path.join(path, file)
            if os.path.isfile(self.filename):
                content = ConfirmPopup(text='Overwrite the file "'+self.filename+'"?', yes_text='Overwrite', no_text="Cancel", warn_yes=True)
                content.bind(on_answer=self.export_overwrite_answer)
                self.popup = NormalPopup(title='Confirm Overwrite', content=content, size_hint=(None, None), size=(app.popup_x, app.button_scale * 4), auto_dismiss=False)
                self.popup.open()
            else:
                self.export_finish()

    def export_overwrite_answer(self, instance, answer): #OLD
        Logger.debug("photomanager screencollege CollageScreen.export_overwrite_answer")
        del instance
        if answer == 'yes':
            self.dismiss_popup()
            self.export_finish()

    def export_finish(self):  #OLD
        Logger.debug("photomanager screencollege CollageScreen.export_finish")
        app = App.get_running_app()
        if len(self.collage.images) > 8:
            message = 'Exporting Collage, This May Take Several Minutes, Please Wait...'
        else:
            message = 'Exporting Collage, Please Wait...'
        self.popup = ScanningPopup(title=message, auto_dismiss=False, size_hint=(None, None), size=(app.popup_x, app.button_scale * 4))
        self.popup.scanning_text = ''
        self.popup.button_text = 'Ok'
        self.popup.open()
        self.export_process()
        # It calls the export_process() within the main Thread Instead of creating another Thread 
        # self.exportthread = threading.Thread(target=self.export_process) #ORIGINAL
        # self.exportthread.start()

    # def export_process(self, *_):  #OLD
    #     Logger.debug("photomanager screencollege CollageScreen.export_process")
    #     scanning = 0
    #     if self.resolution == 'High':
    #         self.export_scale = 4
    #     elif self.resolution == 'Low':
    #         self.export_scale = 1
    #     else:
    #         self.export_scale = 2

    #     #wait for full sized images to load
    #     check_images = []
    #     if self.export_scale > 1:
    #         for image in self.collage.images:
    #             scanning = scanning + 10
    #             if scanning > 100:
    #                 scanning = 0
    #             self.popup.scanning_percentage = scanning
    #             async_image = image.children[0].children[0]
    #             if not async_image.is_full_size:
    #                 async_image.loadfullsize = True
    #                 async_image._load_fullsize()
    #                 check_images.append(async_image)
    #     while check_images:
    #         for image in check_images:
    #             scanning = scanning + 10
    #             if scanning > 100:
    #                 scanning = 0
    #             self.popup.scanning_percentage = scanning
    #             if image.is_full_size:
    #                 check_images.remove(image)

    #     self.collage.show_guides(False)

    #     #wait a cycle so kivy can finish displaying the textures
    #     Clock.schedule_once(self.export_collage_as_image,0.1)
    
    def export_collage_as_image(self, callback=None): #NEW
        Logger.debug("photomanager screencollege CollageScreen.export_collage_as_iamge")
        exported = self.export_scaled_jpg(self.collage, self.filename, image_scale=self.export_scale)

        app = App.get_running_app()
        if exported is True:
            app.message(f"Exported {self.filename}")
        else:
            app.message(f"Export error: {exported}")

        self.collage.show_guides(True)

        if callback:
            Clock.schedule_once(callback, 0.2)


    # def export_collage_as_image(self, *_): #OLD
    #     Logger.debug("photomanager screencollege CollageScreen.export_collage_as_iamge")
    #     collage = self.collage
    #     exported = self.export_scaled_jpg(collage, self.filename, image_scale=self.export_scale)
    #     app = App.get_running_app()
    #     self.popup.dismiss()
    #     self.popup = None
    #     if exported is True:
    #         app.message("Exported "+self.filename)
    #     else:
    #         app.message('Export error: '+exported)
    #     self.collage.show_guides(True)

    def export_scaled_jpg(self, widget, filename, image_scale=1):  #OLD
        Logger.debug("photomanager screencollege CollageScreen.export_scaled_jpg")
        from kivy.graphics import (Translate, Fbo, ClearColor, ClearBuffers, Scale)
        re_size = (widget.width * image_scale, widget.height * image_scale)

        if widget.parent is not None:
            canvas_parent_index = widget.parent.canvas.indexof(widget.canvas)
            if canvas_parent_index > -1:
                widget.parent.canvas.remove(widget.canvas)

        try:
            fbo = Fbo(size=re_size, with_stencilbuffer=True)
            with fbo:
                ClearColor(0, 0, 0, 0)
                ClearBuffers()
                Scale(image_scale, -image_scale, image_scale)
                Translate(-widget.x, -widget.y - widget.height, 0)

            fbo.add(widget.canvas)
            fbo.draw()
            from io import BytesIO
            image_bytes = BytesIO()
            fbo.texture.save(image_bytes, flipped=False, fmt='png')
            image_bytes.seek(0)
            from PIL import Image
            image = Image.open(image_bytes)
            image = image.convert('RGB')
            image.save(filename)
            exported = True
        except Exception as ex:
            exported = str(ex)
        try:
            fbo.remove(widget.canvas)
        except:
            pass

        if widget.parent is not None and canvas_parent_index > -1:
            widget.parent.canvas.insert(canvas_parent_index, widget.canvas)
        return exported

    def change_transform(self, transform_mode):
        Logger.debug("photomanager screencollege CollageScreen.change_transform")
        self.collage.transform_mode = transform_mode
        # self.update_album_json()

    def on_sort_reverse(self, *_):
        Logger.debug("photomanager screencollege CollageScreen.on_sort_reverse")
        """Updates the sort reverse button's state variable, since kivy doesnt just use True/False for button states."""

        app = App.get_running_app()
        self.sort_reverse_button = 'down' if to_bool(app.config.get('Sorting', 'album_sort_reverse')) else 'normal'

    def drop_widget(self, fullpath, position, dropped_type='file', aspect=1):
        Logger.debug("photomanager screencollege CollageScreen.drop_widget")
        """Called when a widget is dropped.  Determine photo dragged, and where it needs to go."""

        position = self.collage.to_widget(*position)
        self.collage.drop_image(fullpath, position, aspect=aspect)

    def show_selected(self):
        Logger.debug("photomanager screencollege CollageScreen.show_selected")
        """Scrolls the treeview to the currently selected folder"""

        database = self.ids['albumContainer']
        database_interior = self.ids['album']
        selected = self.selected
        data = database.data
        current_folder = None
        for i, node in enumerate(data):
            if node['target'] == selected and node['type'] == self.type:
                current_folder = node
                break
        if current_folder is not None:
            database_interior.selected = current_folder
            database.scroll_to_selected()

    def text_input_active(self):
        Logger.debug("photomanager screencollege CollageScreen.text_input_active")
        """Detects if any text input fields are currently active (being typed in).
        Returns: True or False
        """

        input_active = False
        for widget in self.walk(restrict=True):
            if widget.__class__.__name__ == 'NormalInput' or widget.__class__.__name__ == 'FloatInput' or widget.__class__.__name__ == 'IntegerInput':
                if widget.focus:
                    input_active = True
                    break
        return input_active

    def has_popup(self):
        Logger.debug("photomanager screencollege CollageScreen.haS_popup")
        """Detects if the current screen has a popup active.
        Returns: True or False
        """

        if self.popup:
            if self.popup.open:
                return True
        return False

    def dismiss_popup(self, *_):
        Logger.debug("photomanager screencollege CollageScreen.dismiss_popup")
        """Close a currently open popup for this screen."""

        if self.popup:
            if self.popup.title.startswith('Exporting Collage'):
                return False
            self.popup.dismiss()
            self.popup = None

    def dismiss_extra(self):
        Logger.debug("photomanager screencollege CollageScreen.dismiss_extra")
        """Deactivates running processes if applicable.
        Returns: True if something was deactivated, False if not.
        """

        return False

    def key(self, key):
        Logger.debug("photomanager screencollege CollageScreen.key")
        """Handles keyboard shortcuts, performs the actions needed.
        Argument:
            key: The name of the key command to perform.
        """

        if self.text_input_active():
            pass
        else:
            if not self.popup or (not self.popup.open):
                #normal keypresses
                pass
            elif self.popup and self.popup.open:
                if key == 'enter':
                    self.popup.content.dispatch('on_answer', 'yes')

    def scroll_photolist(self):
        Logger.debug("photomanager screencollege CollageScreen.scroll_photolist")
        """Scroll the right-side photo list to the current active photo."""

        photolist = self.ids['albumContainer']
        self.show_selected()
        photolist.scroll_to_selected()

    def refresh_all(self):
        Logger.debug("photomanager screencollege CollageScreen.refresh_all")
        self.refresh_photolist()
        self.refresh_photoview()

    def update_selected(self):
        Logger.debug("photomanager screencollege CollageScreen.update_selected")
        pass

    def refresh_photolist(self):
        Logger.debug("photomanager screencollege CollageScreen.refresh_photolist")
        """Reloads and sorts the photo list"""

        app = App.get_running_app()

        #Get photo list
        self.photos = []
        if self.type == 'Tag':
            self.photos = app.database_get_tag(self.target)
        else:
            self.photos = app.database_get_folder(self.target)
        

        #Remove video files
        temp_photos = []
        for photo in self.photos:
            source = os.path.join(photo[2], photo[0])
            isvideo = os.path.splitext(source)[1].lower() in app.movietypes
            if not isvideo:
                temp_photos.append(photo)
        self.photos = temp_photos

        #Sort photos
        if self.sort_method == 'Imported':
            sorted_photos = sorted(self.photos, key=lambda x: x[6], reverse=self.sort_reverse)
        elif self.sort_method == 'Modified':
            sorted_photos = sorted(self.photos, key=lambda x: x[7], reverse=self.sort_reverse)
        elif self.sort_method == 'Owner':
            sorted_photos = sorted(self.photos, key=lambda x: x[11], reverse=self.sort_reverse)
        elif self.sort_method == 'Name':
            sorted_photos = sorted(self.photos, key=lambda x: os.path.basename(x[0]), reverse=self.sort_reverse)
        else:
            sorted_photos = sorted(self.photos, key=lambda x: x[0], reverse=self.sort_reverse)
        self.photos = sorted_photos
        
    
    def show_prev_collage(self):
        if self.current_collage_index > 0:
            self.switch_collage(self.current_collage_index - 1)
            self.page_status = f"Page {self.current_collage_index + 1} of {len(self.collages)}"


    def show_next_collage(self):
        if self.current_collage_index < len(self.collages) - 1:
            self.switch_collage(self.current_collage_index + 1)
            self.page_status = f"Page {self.current_collage_index + 1} of {len(self.collages)}"


    # def update_album_ini(self):
        
    #     app = App.get_running_app()
    #     project_name = app.selected_project if hasattr(app, "selected_project") else "Default Project"
    #     album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.ini")
    #     # os.makedirs(album_folder, exist_ok=True)
    #     album_ini_path = os.path.join(album_folder)

    #     config = ConfigParser()
    #     config["Album"] = {
    #             "album_page_count": str(self.total_pages),
    #             "aspect": str(self.aspect),
    #             "aspect_text": self.aspect_text,
    #             "resolution": self.resolution
    #         }

    #         # Add each page's data
    #     for i, collage in enumerate(self.collages):
    #         section = f"Page{i + 1}"
    #         config[section] = {}

    #         # Collage type per page
    #         collage_type = self.collage_types[i]
    #         config[section]["collage_type"] = collage_type

    #         # Background per page (assuming it may differ across pages later)
    #         collage_background = getattr(collage, "collage_background", [0, 0, 0, 1])
    #         config[section]["collage_background"] = ",".join(map(str, collage_background))

    #         # Image paths
    #         for i, collage in enumerate(self.collages):
    #             section = f"Page{i + 1}"
    #             config[section] = {}

    #             # Collage type per page
    #             collage_type = self.collage_types[i]
    #             config[section]["collage_type"] = collage_type

    #             # Background per page
    #             collage_background = getattr(collage, "collage_background", [0, 0, 0, 1])
    #             config[section]["collage_background"] = ",".join(map(str, collage_background))

    #             # Images (only added if actually present)
    #             for idx, img in enumerate(collage.images):
    #                 config[section][f"image{idx + 1}"] = img.source


    #     # Write to file
    #     with open(album_ini_path, "w") as configfile:  
    #         config.write(configfile)

    #     print(f"album.ini updated at: {album_ini_path}")
    
    def normalize_angle(self, angle):
        return min([0, 90, 180, 270], key=lambda x: abs(x - angle % 360))

    
    def update_album_json(self):
        app = App.get_running_app()
        project_name = getattr(app, "selected_project", "Default Project")
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        os.makedirs(album_folder, exist_ok=True)
        json_path = os.path.join(album_folder, "album.json")
        template_name = getattr(app, "template", "Default Template 1")  # fallback
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        template_out_path = os.path.join(album_folder, f"{template_name}.json")

        # data = {
        #     "album": {
        #         "page_count": self.total_pages,
        #         "aspect": self.aspect,
        #         "aspect_text": self.aspect_text,
        #         "resolution": self.resolution
        #     }
        # }
        if os.path.exists(template_out_path):
            with open(template_out_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        if "album" not in data:
            data["album"] = {}

        album_meta = data["album"]
        album_meta["page_count"] = self.total_pages
        album_meta["aspect"] = self.aspect
        album_meta["aspect_text"] = self.aspect_text
        album_meta["resolution"] = self.resolution

        # Maintain existing special/title counts if already present
        for key in ["front_title_pages", "front_special_pages", "back_title_pages", "back_special_pages"]:
            if not key in album_meta:
                album_meta[key] = 0

        for i, collage in enumerate(self.collages):
            # page_key = f"page{i + 1}"
            page_key = self.page_keys[i] if i < len(self.page_keys) else f"page{i + 1}"

            collage_type = self.collage_types[i]
            background = getattr(collage, "collage_background", [0, 0, 0, 1])

            image_list = []
            for img in collage.images:
                angle = getattr(img, 'user_angle', 0.0)
                image_data = {
                    "path": img.source,
                    "size": img.scale,
                    "angle":  self.normalize_angle(angle),
                    "aspect": img.aspect
                }
                # if isinstance(collage, ScatterCollage):
                if hasattr(collage, "images") and all(hasattr(img, "pos") for img in collage.images):
                    pos = list(img.pos)
                    if img.pos == [0, 0] or None:
                        Logger.warning(f"Image {img.source} position still (0, 0) at save time!")
                        pos = list(img.center)
                    image_data["position"] = pos
                if isinstance(collage, GridCollage):
                    parent_slot = img.parent
                    grid_slots = [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]
                    try:
                        index = grid_slots.index(parent_slot)
                        image_data["slot"] = index
                    except ValueError:
                        continue  

                image_list.append(image_data)

            data[page_key] = [{
                "collage_type": collage_type,
                "background": background,
                "images": image_list
            }]

        with open(template_out_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"✅ album.json updated at: {json_path}")

    def switch_collage(self, index):
        Logger.debug(f"Switching collage page to {index + 1}")
        if index < 0 or index >= len(self.collages):
            return
        collage_holder = self.ids['collageHolder']
        collage_holder.clear_widgets()
        self.current_collage_index = index
        self.collage = self.collages[index]
        self.current_page_key = self.page_keys[index]  
        collage_holder.add_widget(self.collage)
        # self.collage_type = self.collage_types[self.current_collage_index]
        self.ids.collageTypeButton.text = '  Collage Type: ' + self.collage_types[self.current_collage_index]

    
        self.page_status = f"Page {self.current_collage_index + 1} of {len(self.collages)}"
        for child in self.collage.walk(restrict=True):
            if isinstance(child, GridImageWithLayers):
                child.apply_template()
        project_name = getattr(App.get_running_app(), "selected_project", "Default Project")
        json_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.json")
        app = App.get_running_app()
        template_name = getattr(app, "template", "Default Template 1")  
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        template_out_path = os.path.join(album_folder, f"{template_name}.json")
        with open(template_out_path, "r") as f:
            data = json.load(f)

        page_key = self.page_keys[index]
        page_data = data.get(page_key, [{}])[0]
        has_images = len(page_data.get("images", [])) > 0

        if has_images:
            Clock.schedule_once(lambda dt: self.restore_images_for_page(index, data), 0.2)
        else:
            Clock.schedule_once(lambda dt: self.autofill_current_page(index), 0.1)
            self.autofilled_pages.add(index)

        
    def get_event_names(self):
        app = App.get_running_app()
        project_name = app.selected_project if hasattr(app, "selected_project") else "Default Project"

        events_directory = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "Events")
        if not os.path.exists(events_directory):
            return []

        event_files = [f[:-6] for f in os.listdir(events_directory) if f.endswith('.event')]
        sorted_events = sorted(event_files)
        return sorted_events
    
    def populate_event_dropdown(self):
        app = App.get_running_app()
        self.event_dropdown.clear_widgets()
        event_names = self.get_event_names()
        event_names.insert(0, "All")
        current_selection = self.selected_event or "All"
        for event_name in event_names:
            event_name = app.database_get_renamed_events(event_name)
            if event_name == current_selection:
                continue
            btn = MenuButton(
                text=event_name,
                size_hint_y=None,
                height=40
            )
            btn.bind(on_release=lambda btn, en=event_name: self.on_event_selected(en))
            self.event_dropdown.add_widget(btn)
            
    def on_event_selected(self, event_name):
            Logger.info(f"Event selected: {event_name}")
            # self.ids.sortButton.text = event_name
            self.selected_event = event_name
            self.event_dropdown.dismiss()
            self.refresh_photoview()
            self.populate_event_dropdown()  
            
    # def get_used_photo_paths(self):
    #     used_paths = set()

    #     # Load album JSON from file
    #     app = App.get_running_app()
    #     project_name = app.selected_project if hasattr(app, "selected_project") else "Default Project"
    #     album_json_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.json")
    #     if not os.path.exists(album_json_path):
    #         return used_paths

    #     with open(album_json_path, 'r', encoding='utf-8') as f:
    #         data = json.load(f)

    #     for key, value in data.items():
    #         if key.startswith("page") and isinstance(value, list):
    #             for page in value:
    #                 if "images" in page:
    #                     for img in page["images"]:
    #                         used_paths.add(img["path"])

    #     return used_paths
    

    def get_used_photo_paths(self):
        app = App.get_running_app()
        project_name = getattr(App.get_running_app(), "selected_project", "Default Project")
        json_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.json")
        template_name = getattr(app, "template", "Default Template 1")  
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        template_out_path = os.path.join(album_folder, f"{template_name}.json")
        used_paths = {}  # Dictionary to hold {page_key: set(paths)}

        if not os.path.exists(template_out_path):
            return used_paths

        with open(template_out_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key, value in data.items():
            if key == "album":
                continue  # skip metadata section

            if isinstance(value, list):
                image_paths = set()
                for section in value:
                    images = section.get("images", [])
                    for img in images:
                        if "path" in img:
                            image_paths.add(img["path"])

                if image_paths:
                    used_paths[key] = image_paths

        return used_paths



    def refresh_photoview(self):
        Logger.debug("photomanager screencollege CollageScreen.refresh_photoview")
        #refresh recycleview
        photolist = self.ids['albumContainer']
        photodatas = []
        if hasattr(self, 'selected_event') and self.selected_event != 'All':
            if '(' in self.selected_event and self.selected_event.endswith(')'):
                selected = self.selected_event.rsplit('(', 1)[-1].rstrip(')')
                photos = [p for p in self.photos if p[24] == selected and p[25].lower() == "good"]
            else:
                photos = [p for p in self.photos if p[24] == self.selected_event and p[25].lower() == "good"]
        else:
            photos = [p for p in self.photos if p[25].lower() == "good"]
        if not photos:#TEMPLATE
            Logger.debug("No good photos found. Showing all photos.")
            photos = self.photos  
        for photo in photos:
            fullpath = os.path.join(photo[2], photo[0]).replace("/", "\\")

            # is_used = fullpath in self.used_photo_paths
            is_used = any(fullpath in page_set for page_set in self.used_photo_paths.values())
            source = os.path.join(photo[2], photo[0])
            filename = os.path.basename(photo[0])
            photodata = {
                'text': filename,
                'fullpath': photo[0],
                'temporary': True,
                'photoinfo': photo,
                'folder': self.selected,
                'database_folder': photo[2],
                'filename': filename,
                'target': self.selected,
                'type': self.type,
                'owner': self,
                'video': False,
                'photo_orientation': photo[13],
                'source': source,
                'title': photo[10],
                'selected': False,
                'selectable': not is_used,
                'dragable': not is_used,
                'disabled': is_used 
            }
            photodatas.append(photodata)
        photolist.data = photodatas

    def clear_photolist(self):
        Logger.debug("photomanager screencollege CollageScreen.clear_photolist")
        photolist = self.ids['albumContainer']
        photolist.data = []

    def resort_method(self, method):
        Logger.debug("photomanager screencollege CollageScreen.resort_method")
        """Sets the album sort method.
        Argument:
            method: String, the sort method to use
        """

        self.sort_method = method
        app = App.get_running_app()
        app.config.set('Sorting', 'album_sort', method)
        self.refresh_all()
        Clock.schedule_once(lambda *dt: self.scroll_photolist())

    def resort_reverse(self, reverse):
        Logger.debug("photomanager screencollege CollageScreen.resort_reverse")
        """Sets the album sort reverse.
        Argument:
            reverse: String, if 'down', reverse will be enabled, disabled on any other string.
        """

        app = App.get_running_app()
        sort_reverse = True if reverse == 'down' else False
        app.config.set('Sorting', 'album_sort_reverse', sort_reverse)
        self.sort_reverse = sort_reverse
        self.refresh_all()
        Clock.schedule_once(lambda *dt: self.scroll_photolist())
        Clock.schedule_once(lambda dt: self.update_album_json(), 0.3)


    # def on_collage_type(self, *_):
    #     Logger.debug("photomanager screencollege CollageScreen.on_collage_type")
    #     self.set_collage()

    # def set_collage(self):
    #     Logger.debug("photomanager screencollege CollageScreen.set_collage")
    #     if self.collage:
    #         self.collage.clear()
    #     collage_holder = self.ids['collageHolder']
    #     collage_holder.clear_widgets()
    #     if self.collage_type == 'Pile':
    #         self.collage = ScatterCollage()
    #     elif self.collage_type == '3':
    #         self.collage = GridCollage3()
    #     elif self.collage_type == '2x2':
    #         self.collage = GridCollage2x2()
    #     elif self.collage_type == '5':
    #         self.collage = GridCollage5()
    #     elif self.collage_type == '2x3':
    #         self.collage = GridCollage2x3()
    #     elif self.collage_type == '3x2':
    #         self.collage = GridCollage3x2()
    #     elif self.collage_type == '3x3':
    #         self.collage = GridCollage3x3()
    #     self.collage.collage_background = self.collage_background
    #     collage_holder.add_widget(self.collage)
    # def set_collage(self):
    # Logger.debug("photomanager screencollege CollageScreen.set_collage")

    # app = App.get_running_app()
    # collage_holder = self.ids['collageHolder']
    # collage_holder.clear_widgets()

    # self.collages = []
    # self.current_collage_index = 0

    # try:
    #     page_count = int(app.page_count)  # from AlbumCountScreen
    # except:
    #     page_count = 1

    # for _ in range(page_count):
    #     if self.collage_type == 'Pile':
    #         collage = ScatterCollage()
    #     elif self.collage_type == '3':
    #         collage = GridCollage3()
    #     elif self.collage_type == '2x2':
    #         collage = GridCollage2x2()
    #     elif self.collage_type == '5':
    #         collage = GridCollage5()
    #     elif self.collage_type == '2x3':
    #         collage = GridCollage2x3()
    #     elif self.collage_type == '3x2':
    #         collage = GridCollage3x2()
    #     elif self.collage_type == '3x3':
    #         collage = GridCollage3x3()
    #     else:
    #         collage = ScatterCollage()

    #     collage.collage_background = self.collage_background
    #     self.collages.append(collage)

    # if self.collages:
    #     self.collage = self.collages[0]
    #     collage_holder.add_widget(self.collage)

    # def set_collage(self):
    #     Logger.debug("photomanager screencollege CollageScreen.set_collage")

    #     app = App.get_running_app()
    #     collage_holder = self.ids['collageHolder']
    #     collage_holder.clear_widgets()

    #     self.collages = []
    #     self.current_collage_index = 0

    #     layout_sequence = ['2x2', '3x2', '3', '2x3', '3x3', '5']  # Define layouts you want to cycle through

    #     try:
    #         page_count = int(app.album_page_count)
    #     except:
    #         page_count = 1

    #     for i in range(page_count):
    #         layout_type = layout_sequence[i % len(layout_sequence)]  # cycle through layouts

    #         if layout_type == 'Pile':
    #             collage = ScatterCollage()
    #         elif layout_type == '3':
    #             collage = GridCollage3()
    #         elif layout_type == '2x2':
    #             collage = GridCollage2x2()
    #         elif layout_type == '5':
    #             collage = GridCollage5()
    #         elif layout_type == '2x3':
    #             collage = GridCollage2x3()
    #         elif layout_type == '3x2':
    #             collage = GridCollage3x2()
    #         elif layout_type == '3x3':
    #             collage = GridCollage3x3()
    #         else:
    #             collage = ScatterCollage()

    #         collage.collage_background = self.collage_background
    #         self.collages.append(collage)

    #     if self.collages:
    #         self.collage = self.collages[0]
    #         collage_holder.add_widget(self.collage)

    # def set_collage(self):
    #     Logger.debug("photomanager screencollege CollageScreen.set_collage")

    #     app = App.get_running_app()
    #     collage_holder = self.ids['collageHolder']
    #     collage_holder.clear_widgets()

    #     self.collages = []
    #     self.current_collage_index = 0

    #     try:
    #         page_count = int(app.album_page_count)
    #     except:
    #         page_count = 1

    #     # Initialize or reset collage_types per page
    #     self.collage_types = ['Pile'] * page_count

    #     for i in range(page_count):
    #         layout = self.collage_types[i]
    #         collage = self.build_collage_widget(layout)
    #         collage.collage_background = self.collage_background
    #         self.collages.append(collage)

    #     if self.collages:
    #         self.collage = self.collages[self.current_collage_index]
    #         collage_holder.add_widget(self.collage)
    #         # self.collage_type = self.collage_types[self.current_collage_index]
    #         self.ids.collageTypeButton.text = '  Collage Type: ' + self.collage_types[self.current_collage_index]


    #         self.page_status = f"Page {self.current_collage_index + 1} of {len(self.collages)}"
    
    
    
    # def set_collage(self):
    #     Logger.debug("photomanager screencollege CollageScreen.set_collage")

    #     app = App.get_running_app()
    #     collage_holder = self.ids['collageHolder']
    #     collage_holder.clear_widgets()

    #     self.collages = []
    #     self.collage_types = []
    #     self.current_collage_index = 0

    #     # Load album.ini
    #     project_name = app.selected_project if hasattr(app, "selected_project") else "Default Project"
    #     album_ini_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.ini")

    #     config = ConfigParser()
    #     if os.path.exists(album_ini_path):
    #         config.read(album_ini_path)

    #         self.total_pages = int(config.get("Album", "album_page_count", fallback="1"))
    #         self.aspect = float(config.get("Album", "aspect", fallback="1.3333"))
    #         self.aspect_text = config.get("Album", "aspect_text", fallback="4:3")
    #         self.resolution = config.get("Album", "resolution", fallback="Medium")

    #         for i in range(1, self.total_pages + 1):
    #             section = f"Page{i}"
    #             collage_type = config.get(section, "collage_type", fallback="Pile")
    #             collage_background = list(map(float, config.get(section, "collage_background", fallback="0,0,0,1").split(",")))

    #             collage = self.build_collage_widget(collage_type)
    #             collage.collage_background = collage_background
    #             collage.owner = self

    #             idx = 0
    #             while True:
    #                 path_key = f"image{idx}_path"
    #                 if path_key not in config[section]:
    #                     break

    #                 path = config[section][path_key]
    #                 try:
    #                     rel_path = path.split("organized_folder" + os.sep, 1)[1].replace("\\", "/")
    #                 except IndexError:
    #                     Logger.warning(f"[Album Load] Skipping invalid path: {path}")
    #                     idx += 1
    #                     continue

    #                 position = tuple(map(float, config[section].get(f"image{idx}_pos", "0,0").split(",")))
    #                 size = float(config[section].get(f"image{idx}_size", "0.5"))
    #                 angle = float(config[section].get(f"image{idx}_angle", "0"))
    #                 aspect = float(config[section].get(f"image{idx}_aspect", "1"))

    #                 photoinfo = app.database_exists(rel_path)
    #                 if photoinfo is None:
    #                     Logger.warning(f"[Album Load] Image not found in DB: {rel_path}, skipping.")
    #                     idx += 1
    #                     continue

    #                 if isinstance(collage, ScatterCollage):
    #                     collage.add_collage_image(rel_path, position=position, size=size, angle=angle, aspect=aspect)

    #                 elif isinstance(collage, GridCollage):
    #                     grid_slots = [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]
    #                     if idx < len(grid_slots):
    #                         collage.add_collage_image(grid_slots[idx], rel_path, size=size, angle=angle, aspect=aspect)

    #                 idx += 1

    #             self.collages.append(collage)
    #             self.collage_types.append(collage_type)
    #     else:
    #         # Fallback for new album
    #         self.total_pages = 1
    #         self.aspect = 1.3333
    #         self.aspect_text = "4:3"
    #         self.resolution = "Medium"

    #         collage = self.build_collage_widget("Pile")
    #         collage.collage_background = self.collage_background
    #         collage.owner = self

    #         self.collages.append(collage)
    #         self.collage_types.append("Pile")

    #     if self.collages:
    #         self.collage = self.collages[0]
    #         collage_holder.add_widget(self.collage)
    #         self.ids.collageTypeButton.text = '  Collage Type: ' + self.collage_types[0]
    #         self.page_status = f"Page 1 of {len(self.collages)}"

    def set_collage(self):
        Logger.debug("photomanager screencollege CollageScreen.set_collage")

        app = App.get_running_app()
        collage_holder = self.ids['collageHolder']
        collage_holder.clear_widgets()
        self.collages = []
        self.collage_types = []
        self.current_collage_index = 0

        project_name = getattr(app, "selected_project", "Default Project")
        json_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.json")
        template_name = getattr(app, "template", "Default Template 1")  
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        template_out_path = os.path.join(album_folder, f"{template_name}.json")


        with open(template_out_path, "r") as f:
            data = json.load(f)

        album_settings = data.get("album", {})
        self.total_pages = album_settings.get("page_count", 1)
        self.aspect = album_settings.get("aspect", 1.3333)
        self.aspect_text = album_settings.get("aspect_text", "4:3")
        self.resolution = album_settings.get("resolution", "Medium")
        
        page_keys = [k for k in data.keys() if k != "album"]
        self.total_pages = len(page_keys)
        
        # for i in range(1, self.total_pages + 1):
        for page_key in page_keys:
            # page_key = f"page{i}"
            page_data = data.get(page_key, [{}])[0]

            collage_type = page_data.get("collage_type", "Pile")
            background = page_data.get("background", [0, 0, 0, 1])
            # images = page_data.get("images", [])

            collage = self.build_collage_widget(collage_type)
            collage.collage_background = background
            collage.owner = self

            self.collages.append(collage)
            self.collage_types.append(collage_type)
        self.page_keys = page_keys

        if self.collages:
            self.collage = self.collages[0]
            collage_holder.add_widget(self.collage)
            self.ids.collageTypeButton.text = '  Collage Type: ' + self.collage_types[0]
            self.page_status = f"Page 1 of {len(self.collages)}"
            # with open(json_path, "r") as f:
            #     data = json.load(f)
            # self.restore_images_for_page(0, data)
            Clock.schedule_once(lambda dt: self.restore_images_for_page(0,data), 0.2)
        # self.page_keys = page_keys

                        
    def restore_images_for_page(self, index, data):
        Logger.debug(f"Restoring images for page {index + 1}")
        app = App.get_running_app()
        # page_key = f"page{index + 1}"
        page_key = self.page_keys[index]
        page_data = data.get(page_key, [{}])[0]
        images = page_data.get("images", [])
        collage = self.collages[index]
        # if isinstance(collage, ScatterCollage):
        #     for child in list(collage.images):
        #         collage.remove_widget(child)
        #     collage.images.clear()
        # elif isinstance(collage, GridCollage):
        #     for grid_image in [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]:
        #         # Assuming GridImage has an 'image' attribute or child
        #         if hasattr(grid_image, 'source'):
        #             grid_image.source = ''
        #         elif hasattr(grid_image, 'clear_widgets'):
        #             grid_image.clear_widgets()
                    
        for image_data in images:
            rel_path = image_data.get("path")
            position = tuple(image_data.get("position", [0, 0]))
            size = image_data.get("size", 0.5)
            angle = image_data.get("angle", 0)
            aspect = image_data.get("aspect", 1)
            slot_index = image_data.get("slot", None)

            rel_path = rel_path.split("organized_folder" + os.sep, 1)[1].replace("\\", "/")
            photoinfo = app.database_exists(rel_path)
            if photoinfo is None:
                Logger.warning(f"[Album Load] Image not found in DB: {rel_path}, skipping.")
                continue

            if isinstance(collage, ScatterCollage):
                collage.add_collage_image(rel_path, position=position, size=size, angle=angle, aspect=aspect)

            elif isinstance(collage, GridCollage):
                grid_slots = [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]
                if slot_index is not None and slot_index < len(grid_slots):
                    collage.add_collage_image(grid_slots[slot_index], rel_path, size=size, angle=angle, aspect=aspect)

        self.deselect_images()
        

                        
    # def reset_image_angles(album_data):
    #     for page_key in album_data:
    #         for item in album_data[page_key]:
    #             for image in item.get("images", []):
    #                 # Reset the angle to original value
    #                 image["angle"] = 90.0
    #     return album_data

            
    
    def build_collage_widget(self, collage_type):
        Logger.debug(f"photomanager collage screen build_collage_widget: {collage_type}")
        if collage_type == 'Pile':
            collage = ScatterCollage()
        elif collage_type == '3':
            collage = GridCollage3()
        elif collage_type == '2':
            collage = GridCollage2()
        elif collage_type == '1':
            collage = GridCollage1()
        elif collage_type == '2x2':
            collage = GridCollage2x2()
        elif collage_type == '5':
            collage = GridCollage5()
        elif collage_type == '2x3':
            collage = GridCollage2x3()
        elif collage_type == '3x2':
            collage = GridCollage3x2()
        elif collage_type == '7':
            collage = GridCollage7()
        elif collage_type == '3x3':
            collage = GridCollage3x3()
        else:
            collage = ScatterCollage()  # fallback

        collage.owner = self  # <--- this sets the owner to CollageScreen
        return collage
    
    def refill_collage_from_continuity(self, page_index):
        Logger.info(f"📌 Rebuilding layout continuity from page {page_index + 1}")

        all_photos = []
        for event_name in self.get_event_names():
            raw_event = event_name.rsplit("(", 1)[-1].rstrip(")") if "(" in event_name else event_name
            event_photos = [p for p in self.photos if p[24] == raw_event and str(p[25]).lower() == 'good']
            all_photos.extend(event_photos)

        used_paths = self.get_used_photo_paths()
        in_use = set()
        for v in used_paths.values():
            in_use |= v

        unused_photos = [p for p in all_photos if os.path.join(p[2], p[0]) not in in_use]

        # Extract and flatten future page photos (from next pages)
        future_paths = []
        for idx in range(page_index, len(self.collages)):
            page = self.collages[idx]
            for img in getattr(page, "images", []):
                future_paths.append(img.source)

        future_paths = list(dict.fromkeys(future_paths))  # unique order preserved
        photo_paths = future_paths + [os.path.join(p[2], p[0]) for p in unused_photos]

        Logger.info(f"Reallocating {len(photo_paths)} photos starting at page {page_index + 1}")

        # Clear current and next pages
        for idx in range(page_index, len(self.collages)):
            self.collages[idx].clear()

        # Refill forward using new template slots
        path_idx = 0
        for idx in range(page_index, len(self.collages)):
            collage = self.collages[idx]
            grid_slots = [w for w in collage.walk(restrict=True, loopback=True) if isinstance(w, GridImage)]
            for slot in grid_slots:
                if path_idx >= len(photo_paths):
                    break
                self.collage.add_collage_image(slot, photo_paths[path_idx])
                path_idx += 1

            if path_idx >= len(photo_paths):
                break

        self.deselect_images()
        Logger.info("✅ Continuity-based image refill completed.")


    def on_collage_type(self, *_):
        Logger.debug("photomanager screencollege CollageScreen.on_collage_type (per page)")
        app = App.get_running_app()

        # Update the collage type for current page only
        self.collage_types[self.current_collage_index] = self.collage_type

        # Rebuild collage widget for this page only
        collage_holder = self.ids['collageHolder']
        collage_holder.clear_widgets()

        collage = self.build_collage_widget(self.collage_type)
        collage.collage_background = self.collage_background

        self.collages[self.current_collage_index] = collage
        self.collage = collage
        collage_holder.add_widget(collage)
        # self.update_album_json()
        # self.refill_collage_from_continuity(self.current_collage_index)
        


    def save_album(self):
        Logger.debug("photomanager screencollege CollageScreen.save_album")
        self.deselect_images()
        self.update_album_json()
        self.used_photo_paths = self.get_used_photo_paths()
        # self.refresh_photoview()
        Clock.schedule_once(lambda dt: self.refresh_photoview(), 0)
        print("✅ Album work saved.")

    def on_leave(self):
        Logger.debug("photomanager screencollege CollageScreen.on_leave")
        """Called when the screen is left.  Clean up some things."""

        app = App.get_running_app()
        app.clear_drags()
        self.clear_collage()
        collage_holder = self.ids['collageHolder']
        collage_holder.clear_widgets()
        self.clear_photolist()

    def on_enter(self):
        Logger.debug("photomanager screencollege CollageScreen.on_enter")
        """Called when the screen is entered.  Set up variables and widgets, and prepare to view images."""

        app = App.get_running_app()
        self.set_collage()
        # good_photos = [photo for photo in self.photos if str(photo[25]).lower() == 'good']#TEMPLATE

        # if not good_photos:  # If there are no good photos
        #     Logger.debug("No good photos found. Creating a new page with GridCollage2x2 layout.")
        #     self.collages = [GridCollage2x2()]#TEMPLATE
        #     self.collage = self.collages[0]#TEMPLATE
        #     collage_holder = self.ids['collageHolder']#TEMPLATE
        #     collage_holder.add_widget(self.collage)#TEMPLATE
        #     self.page_keys = ["normal_page1"]  #TEMPLATE

        #     # Load all photos in the left panel (photo list)
        #     self.refresh_photoview()  # Make sure all photos are shown, not just "good" ones

        #     # Set collage type for the new page
        #     self.collage_types = ['2x2']
        #     self.page_status = "Page 1 of 1"
        # else:
        #     self.page_status = f"Page {self.current_collage_index + 1} of {len(self.collages)}"
        if self.collage:
            self.collage.reset_background()
        self.ids['leftpanel'].width = app.left_panel_width()
        self.ids['moveButton'].state = 'down'
        self.ids['rotateButton'].state = 'normal'
        self.color_select = ColorDropDown(owner=self)
        self.resolution_select = ResolutionDropDown(owner=self)
        self.aspect_select = ExportAspectRatioDropDown(owner=self)
        self.add_remove = AddRemoveDropDown(owner=self)
        self.collage_type_select = CollageTypeDropDown(owner=self)
        self.current_page_key = self.page_keys[self.current_collage_index]


        #import variables
        self.target = app.export_target
        self.type = app.export_type

        #set up sort buttons
        self.sort_dropdown = AlbumSortDropDown()
        self.event_dropdown = NormalDropDown()
        self.selected_event = 'All'
        self.populate_event_dropdown()

        self.sort_dropdown.bind(on_select=lambda instance, x: self.resort_method(x))
        self.sort_method = app.config.get('Sorting', 'album_sort')
        self.sort_reverse = to_bool(app.config.get('Sorting', 'album_sort_reverse'))
        self.current_page = 1
        # self.total_pages = app.album_page_count
        # self.aspect = app.aspect
        # self.aspect_text = app.aspect_text
        # self.resolution = app.resolution
        #refresh views
        self.refresh_photolist()
        # self.populate_event_list()
        self.used_photo_paths = self.get_used_photo_paths()
        self.refresh_photoview()
        # self.autofill_album_pages_by_event()
        # Clock.schedule_once(lambda dt: self.autofill_album_pages_by_event(), 0.5)
        self.autofilled_pages = set()  # Add this if not already present
        page_key = self.page_keys[self.current_collage_index]
        has_images = False
        app = App.get_running_app()
        project_name = app.selected_project if hasattr(app, "selected_project") else "Default Project"
        album_path = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name, "album.json")
        template_name = getattr(app, "template", "Default Template 1")  # fallback
        album_folder = os.path.join(os.getenv("APPDATA"), "Snu Photo Manager", project_name)
        template_out_path = os.path.join(album_folder, f"{template_name}.json")
        with open(template_out_path, "r") as f:
            data = json.load(f)
        if page_key in data and data[page_key] and "images" in data[page_key][0]:
            has_images = len(data[page_key][0]["images"]) > 0
        if not hasattr(self, "_in_session_used_paths"):
            self._in_session_used_paths = set()
        else:
            self._in_session_used_paths.clear()

        if not  has_images:
            Clock.schedule_once(lambda dt: self.autofill_current_page(self.current_collage_index), 0.1)
            self.autofilled_pages.add(self.current_collage_index)
        # self._in_session_used_paths = set()

        for child in self.collage.walk(restrict=True):
            if isinstance(child, GridImageWithLayers):
                child.apply_template()
                
