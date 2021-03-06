import pyglet
from pyglet.app import exit
from pyglet.text import Label
from pyglet.window import mouse
from game.gameobject import GameObject
from game.resources import Resources

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

class UIObject(GameObject):
    def __init__(self,name,world,curr_state,*args,**kwargs):
        super(UIObject, self).__init__(name = name,*args, **kwargs)
        self.world = world
        self.curr_state = curr_state

class Button(UIObject):
    def __init__(self,name,curr_state,target_state,world,*args,**kwargs):
        super(Button, self).__init__(name = name, curr_state = curr_state, world = world,*args,**kwargs)
        self.name = name
        self.hand_cursor = world.window.get_system_mouse_cursor('hand')
        self.target_game_state = target_state
        self.fx = Resources.audio['button']

    def hit_test(self,x,y):
        if x > (self.x - (self.width*0.5)) and x < (self.x + (self.width*0.5)):
            if y > (self.y - self.height*0.5) and y < (self.y + (self.height*0.5)):
                return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.active and self.world.state == Resources.states[self.curr_state]:
            if button == mouse.LEFT or button == 0:
                if self.hit_test(x,y):
                    #print "Button: Proceeding to",self.target_game_state,"STATE."
                    self.fx.play()
                    if self.target_game_state == 'SETUP':
                        self.world.switch_to_setup(self.batch)
                    elif self.target_game_state == 'HOST':
                        self.world.switch_to_host(self.batch)
                    elif self.target_game_state == 'JOIN':
                        self.world.switch_to_join(self.batch)
                    elif self.target_game_state == 'GAME':
                        self.world.switch_to_game(self.batch)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.active and self.world.state == Resources.states[self.curr_state]:
            if self.hit_test(x,y):
                #print "Entering Button:",self.name
                self.color = (150,150,150)
                self.world.window.set_mouse_cursor(self.hand_cursor)
            else:
                self.color = (255,255,255)

class QuitButton(UIObject):
    def __init__(self,name,curr_state,world,*args,**kwargs):
        super(QuitButton, self).__init__(name = name, curr_state = curr_state, world = world,*args,**kwargs)
        self.name = name
        self.hand_cursor = world.window.get_system_mouse_cursor('hand')
        self.fx = Resources.audio['button']

    def hit_test(self,x,y):
        if x > (self.x - (self.width*0.5)) and x < (self.x + (self.width*0.5)):
            if y > (self.y - self.height*0.5) and y < (self.y + (self.height*0.5)):
                return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.active and self.world.state == Resources.states[self.curr_state]:
            if button == mouse.LEFT or button == 0:
                if self.hit_test(x,y):
                    self.fx.play()
                    exit()
                    
    def on_mouse_motion(self, x, y, dx, dy):
        if self.active and self.world.state == Resources.states[self.curr_state]:
            if self.hit_test(x,y):
                self.color = (150,150,150)
                self.world.window.set_mouse_cursor(self.hand_cursor)
            else:
                self.color = (255,255,255)

class UILabel(Label):
    def __init__(self,name,*args,**kwargs):
        super(UILabel, self).__init__(*args,**kwargs)
        self.name = name
        self.font_name = "Nexa Bold"
        self.color = (24,24,24,245)
        self.bold = True

class MyRectangle(UIObject):
     def __init__(self,name,curr_state,*args,**kwargs):
        super(MyRectangle, self).__init__(name = name, curr_state = curr_state, world = None,*args,**kwargs)
        self.opacity = 180

class Rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [236, 240, 241, 255] * 4)
        )

class TextWidget(UIObject):
    def __init__(self, text, x, y, width, batch, cursor, curr_state, world, name, *args,**kwargs):
        super(TextWidget,self).__init__(
                                        name = name,
                                        img = Resources.sprites['no_sprite'],
                                        x = x,
                                        y = y,
                                        batch = batch,
                                        curr_state = curr_state,
                                        world = world,
                                        *args,
                                        **kwargs
                                        )
        self.batch = batch
        self.text_cursor = cursor
        self.world = world

        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.font_name = "Nexa Bold"
        self.document.set_style(0,
                            len(self.document.text), 
                            dict(color=(0, 0, 0, 255)))
        font = self.document.get_font()
        height = font.ascent - font.descent
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
                                                                width,
                                                                height,
                                                                multiline=False,
                                                                batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad,
                                   y + height + pad, 
                                   batch)

    def hit_test(self, x, y):
        if self.active and self.world.state == Resources.states[self.curr_state]:
            return (0 < x - self.layout.x < self.layout.width and
                    0 < y - self.layout.y < self.layout.height)
        return False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.hit_test(x, y):
            #print 'Hovering TextWidget:',self.name
            self.world.window.set_mouse_cursor(self.text_cursor)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT or button == 0:
            if self.hit_test(x, y):
                #print 'Focusing TextWidget:',self.name
                self.world.set_focus(self)

        if self.world.focus is self:
            self.world.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.world.focus:
            self.world.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.world.focus is self:
            self.world.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.world.focus is self:
            self.world.focus.caret.on_text_motion(motion)
      
    def on_text_motion_select(self, motion):
        if self.world.focus is self:
            self.world.focus.caret.on_text_motion_select(motion)

class Background(GameObject):
    def __init__(self,name,*args, **kwargs):
        super(Background, self).__init__(name = name,*args, **kwargs)
        self.x = Resources.window_width * 0.5
        self.y = Resources.window_height * 0.5

    def set_image(self,img):
        self.image = img