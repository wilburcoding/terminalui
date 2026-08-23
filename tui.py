# main handler for the ui
from colors import printc, printp, fstrip, borders
import pynput
import os

class App:
    def __init__(self):
        self.main_container = None
        self.listener_active = False
        self.custom_key_actions = {
            "on_key_press": None,
            "on_key_release": None
        }
        self.input_elements = []
        self.selected_element_id = None
        
    def set_main_container(self, container):
        self.main_container = container
    
    def get_main_container(self):
        return self.main_container
        
    def render(self, debug=False):
        # TODO: implement rendering logic
        txt = self._render_container(self.main_container, None)
        lengths = [len(fstrip(line)) for line in txt.split("\n")]
        for line in txt.split("\n"):
            printc(line, bg=(0, 0, 0), fg=(255, 255, 255))
        
        if (debug is True):
            printc(f"Debug: {len(txt.split("\n"))} lines rendered", fg=(255, 255, 0), dec=["bold"])
            if (len(set(lengths)) > 1):
                printc("Warning: Certain lines are not the same length. Make sure you are accounting for borders. ", fg=(255, 0, 0), dec=["bold"])
    
    def start_listener(self):
        self.listener_active = True
        
        self.input_elements = []
        self._find_input_elements(self.main_container)
        self.selected_element_id = None
        # for element in self.input_elements:
        #     print(element.get_id())
        
            
            
        with pynput.keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join() # blocking function btw
            

        
        
            
    def on_key_press(self, key):
        # print(key)
        if (key == pynput.keyboard.Key.esc):
            return False    
        if (self.listener_active is False):
            return False
    
        # arrow keys
        if (key == pynput.keyboard.Key.up):
            pass
        elif (key == pynput.keyboard.Key.down):
            pass
        elif (key == pynput.keyboard.Key.left):
            pass
        elif (key == pynput.keyboard.Key.right):
            pass
        
        if (self.custom_key_actions["on_key_press"] is not None):
            self.custom_key_actions["on_key_press"](key)
    def on_key_release(self, key):
        if (key == pynput.keyboard.Key.esc):
            return False
        if (self.listener_active is False):
            return False
        
        if (self.custom_key_actions["on_key_release"] is not None):
            self.custom_key_actions["on_key_release"](key)
        
    def stop_listener(self):
        self.listener_active = False
       
    

    def _find_input_elements(self, container):
        if (type(container) == Box):
            for child in container.get_children():
                self._find_input_elements(child)
        elif (type(container) == Button):
            self.input_elements.append(container)
        
        
    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
        
    def set_custom_key_action(self, action_type, action):
        if (action_type not in self.custom_key_actions):
            raise ValueError(f"Invalid action type: {action_type}")
        self.custom_key_actions[action_type] = action
    
    def get_custom_key_action(self, action_type):
        if (action_type not in self.custom_key_actions):
            raise ValueError(f"Invalid action type: {action_type}")
        return self.custom_key_actions[action_type]

    def clear_custom_key_action(self, action_type):
        if (action_type not in self.custom_key_actions):
            raise ValueError(f"Invalid action type: {action_type}")
        self.custom_key_actions[action_type] = None
        
    def _render_container(self, container, parent):  
        if (type(container) == Box):
            print(container.get_styles())
            txt = ""
            children = []
            for child in container.get_children():
                children.append(self._render_container(child, container))
            # check layout
            # print(children)
            max_width = container.get_style("width")
            if (parent is not None):
                if (max_width > parent.get_real_width()):
                    max_width = parent.get_real_width()
            max_height = container.get_style("height")
            if (container.get_style("border") is True):
                max_width -=2
                max_height -= 2
            
            

            if (container.get_style("layout") == "vertical"):
                lines = []
                for child in children:
                    spl = child.split("\n")
                    for i in range(len(spl)):
                        lines.append(spl[i])
                for i in range(len(lines)):
                    if (len(fstrip(lines[i])) < max_width):
                        presets = {
                            "bg": container.get_style("background"),
                            "fg": None,
                            "dec": [],
                            "val_ret": True
                        }
                        lines[i] += printp(" " * (max_width - len(fstrip(lines[i]))), presets)
                txt += "\n".join(lines)
                
            elif (container.get_style("layout") == "horizontal"):
                # check widths 
                y_offset = 0 # keep track for every row
                row = []
                lines = []
                # print(children)
                for child in children:
                    spl = child.split("\n")

                    if (len(lines) == 0):
                        for i in range(len(spl)):
                            lines.append(spl[i])
                        continue
                    # print(len(lines[-1]))
                    if (len(fstrip(lines[-1])) + len(fstrip(spl[0])) > max_width):
                        # new row -> clean up existing lines and add new row with child
                        y_offset += len(lines)
                        presets = {
                            "bg": container.get_style("background"),
                            "fg": None,
                            "dec": [],
                            "val_ret": True
                        }
                        for i in range(len(lines)):
                            if (len(fstrip(lines[i])) < max_width):
                                # print(lines[i])
                                lines[i] += printp(" " * (max_width - len(fstrip(lines[i]))), presets)
                            # needs to clean up with the styles of the last element in this row
                        for i in range(len(spl)):
                            lines.append(spl[i])
                    else:
                        # add on to current row
                        if (len(spl) > len(lines)):
                            for i in range(len(lines), len(spl)):
                                lines.append(" " * len(fstrip(lines[0])))
                        for i in range(len(spl)):
                            lines[i + y_offset] += spl[i]
                        
                        

                            
                # clean up lines
                presets = {
                    "bg": container.get_style("background"),
                    "fg": None,
                    "dec": [],
                    "val_ret": True
                }
                for i in range(len(lines)):
                    if (len(fstrip(lines[i])) < max_width):
                        lines[i] += printp(" " * (max_width - len(fstrip(lines[i]))), presets)
                txt += "\n".join(lines)
              
                        

            # add border if needed
            if (container.get_style("border") is True):
                border_style = borders(container.get_style("border_style"))
                presets = {
                    "fg": container.get_style("border_color"),
                    "bg": container.get_style("border_background"),
                    "dec": [],
                    "val_ret": True
                }
                first_line = printp(border_style["tl"] + (border_style["t"] * max_width) + border_style["tr"], presets)
                spl = txt.split("\n")
                for i in range(len(spl)):
                    spl[i] = printp(border_style["l"], presets) + spl[i] + printp(border_style["r"], presets)
                last_line = printp(border_style["bl"] + (border_style["b"] * max_width) + border_style["br"], presets)
                txt = first_line + "\n" + "\n".join(spl) + "\n" + last_line 
                    
            return txt
        elif (type(container) == Text):
            width = container.get_style("width")
            if (width == "parent"):
                width = parent.get_style("width") 
                
            if (width > parent.get_real_width()):
                width = parent.get_real_width()
            
            
            width = int(width)
            text = container.get_text()

            text_presets = {
                "bg": container.get_style("background"),
                "fg": container.get_style("color"),
                "dec": [container.get_style("font_weight")],
                "val_ret":True
            }
            # TODO: implement different word wrap styling logics
            if (container.get_style("word_wrap") == "break-word"):
                lines = []
                # TODO: implement different text styling
                for i in range(0, int(len(text) / width + 1)):
                    t = text[i * width:(i+1)*width]
                    lines.append(t)
                if (len(lines[-1]) < width):
                    lines[-1] += " " * (width - len(lines[-1]))
                for i in range(len(lines)):
                    lines[i] = printp(lines[i], text_presets)
                    
            return "\n".join(lines)

        elif (type(container) == Button):
            width = container.get_style("width")
            if (width == "parent"):
                width = parent.get_style("width")
            print(type(width))
            if (width > parent.get_real_width()):
                width = parent.get_real_width()
            
            height = container.get_style("height")
            if (height > parent.get_real_height()):
                height = parent.get_real_height()
                
            if (container.get_style("border") is True):
                width -= 2
                height -=2
            
            text = container.get_text()
            spl = []
            presets = {
                "bg": container.get_style("background"),
                "fg": container.get_style("color"),
                "dec": [container.get_style("font_weight")],
                "val_ret": True
            }
            for i in range(0, int(len(text) / width + 1)):
                t = text[i * width:(i+1)*width]
                spl.append(printp(t, presets))
                
        
            for i in range(len(spl)):
                if (len(fstrip(spl[i])) < width):
                    spl[i] += printp(" " * (width - len(fstrip(spl[i]))), presets)
            if (len(spl) < height):
                for i in range(len(spl), height):
                    spl.append(printp(" " * width, presets))  
                    
            # check border
            if (container.get_style("border") is True):
                border_style = borders(container.get_style("border_style"))
                border_presets = {
                    "fg": container.get_style("border_color"),
                    "bg": container.get_style("border_background"),
                    "dec": [],
                    "val_ret": True
                }
                first_line = printp(border_style["tl"] + (border_style["t"] * width) + border_style["tr"], border_presets)
                for i in range(len(spl)):
                    spl[i] = printp(border_style["l"], border_presets) + spl[i] + printp(border_style["r"], border_presets)
                last_line = printp(border_style["bl"] + (border_style["b"] * width) + border_style["br"], border_presets)
                txt = first_line + "\n" + "\n".join(spl) + "\n" + last_line
            return txt
                
    
            
            
                
            
            

class Box:
    def __init__(self):
        self.children = []
        self.styles = { # default styles
            "width": 100, 
            "border": False,
            "height": 10,
            "layout": "vertical",
            "border_style": 4,
            "border_background": None,
            "border_color": (255, 255, 255),
            "background": (230, 230, 230),
            "hover": {
                "border_style": 3
            }
        }
        self.id = None
        self.parent = None
        # self.real_width = 100
    
    # helper methods for managing styles and children
    
    def set_style(self, key, value):
        self.styles[key] = value
        
        
        
    def set_styles(self, styles):
        self.styles.update(styles)
        
    def set_parent(self, parent):
        self.parent = parent 
    
    def get_styles(self):
        return self.styles

    def get_style(self, key):
        return self.styles.get(key, None)
    
    def get_parent(self):
        return self.parent
        
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        
    def remove_child(self, child):
        self.children.remove(child)
        
    def get_children(self):
        return self.children
    
    def get_real_width(self):
        width = self.get_style("width")
        if (self.get_style("border") is True):
            width -= 2
        return width
        
    
    def get_real_height(self):
        height = self.get_style("height")
        if (self.get_style("border") is True):
            height -=2
        return height
    
    def set_id(self, id):
        self.id = id
        
    def get_id(self):
        return self.id
        

class Text: 
    def __init__(self, text):
        self.text = text
        self.styles = { # default styles
            "color": (255, 255, 255),
            "background": (0, 0, 0),
            "word_wrap": "break-word",
            "font_weight": "normal",
            "width": "parent"
        }
        self.parent = None
        self.id = None
    
    
    # helper methods
    
    def set_style(self, key, value):
        self.styles[key] = value
    
    def set_styles(self, styles):
        self.styles.update(styles)
        
    def set_text(self, text):
        self.text = text
        
    def get_styles(self):
        return self.styles
    
    def get_style(self, key):
        return self.styles.get(key, None)
    
    def set_parent(self, parent):
        self.parent = parent
    
    def get_parent(self):
        return self.parent
    
    def get_text(self):
        return self.text
    
    def set_id(self, id):
        self.id = id
        
    def get_id(self):
        return self.id
    
class Button:
    def __init__(self, text, id):
        self.text = text
        self.styles = { # default styles
            "color": (255, 255, 255),
            "background": (0, 0, 0),
            "font_weight": "normal",
            "width": 30,
            "height": 3,
            "border": True,
            "border_style": 4,
            "border_background": None,
            "border_color": (255, 255, 255),
            "button_action": None,
            "hover": {
                "border_style": 3
            }
        }
        self.id = id
        self.parent = None
        self.children = []
        
    # the usual helper functions
    
    def set_style(self, key, value):
        self.styles[key] = value
    
    def set_styles(self, styles):
        self.styles.update(styles)
        
    def set_text(self, text):
        self.text = text
        
    def get_styles(self):
        return self.styles
    
    def get_style(self, key):
        return self.styles.get(key, None)

    def get_text(self):
        return self.text
    
    def set_parent(self, parent):
        self.parent = parent
        
    def get_parent(self):
        return self.parent
    
    def set_id(self, id):
        self.id = id
        
    def get_id(self):
        return self.id
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        
    def remove_child(self, child):
        self.children.remove(child)
    
    def get_children(self):
        return self.children
    
    

    
    