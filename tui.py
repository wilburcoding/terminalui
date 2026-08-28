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
        
        rendered_layout = self._render_container(self.main_container, None)
        self._find_input_elements(self.main_container, rendered_layout)
        self.selected_element_id = None
        # for element in self.input_elements:
        #     print(element["corner"])
        #     print(element)
        
        self._clear()
        self.render()
        with pynput.keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release, suppress=True) as listener:
            listener.join() # blocking function btw
            

        
        
            
    def _on_key_press(self, key):
        # print(key)
        if (key == pynput.keyboard.Key.esc):
            return False    
        if (self.listener_active is False):
            return False
    
        # arrow keys
        if (self.selected_element_id is not None):
            # if (key == pynput.keyboard.Key.up):
            #     pass
            # elif (key == pynput.keyboard.Key.down):
            #     pass
            id_index = None
            for i in range(len(self.input_elements)):
                if (self.input_elements[i]["id"] == self.selected_element_id):
                    id_index = i
                    break
            
            if (id_index is None):
                return
            if (key == pynput.keyboard.Key.left):

                id_index -=1
                if (id_index < 0):
                    id_index = len(self.input_elements) - 1
            elif (key == pynput.keyboard.Key.right):
                id_index +=1 
                if (id_index >= len(self.input_elements)):
                    id_index = 0
            self.selected_element_id = self.input_elements[id_index]["id"]
            if (key == pynput.keyboard.Key.enter and type(self.input_elements[id_index]["element"]) == Button):
                button_action = self.input_elements[id_index]["element"].get_button_action()
                if (button_action is not None):
                    button_action(self.input_elements[id_index]["element"])
            if (type(self.input_elements[id_index]["element"]) == Input):
                if (key == pynput.keyboard.Key.backspace):
                    text = self.input_elements[id_index]["element"].get_text()
                    text = text[:-1]
                    self.input_elements[id_index]["element"].set_text(text)
                    change_action = self.input_elements[id_index]["element"].get_on_change_action()
                    if (change_action is not None):
                        change_action(self.input_elements[id_index]["element"])
                elif (key == pynput.keyboard.Key.enter):
                    on_submit_action = self.input_elements[id_index]["element"].get_on_submit_action()
                    if (on_submit_action is not None):
                        on_submit_action(self.input_elements[id_index]["element"])
                elif (hasattr(key, "char") and key.char is not None):
                    text = self.input_elements[id_index]["element"].get_text()
                    text += key.char
                    self.input_elements[id_index]["element"].set_text(text)
                    change_action = self.input_elements[id_index]["element"].get_on_change_action()
                    if (change_action is not None):
                        change_action(self.input_elements[id_index]["element"])
                    
        else:
            if (key in [pynput.keyboard.Key.left, pynput.keyboard.Key.right]):
                if (len(self.input_elements) > 0):
                    self.selected_element_id = self.input_elements[0]["id"] 

        if (self.custom_key_actions["on_key_press"] is not None):
            res = self.custom_key_actions["on_key_press"](key)
            if (res is False):
                return False # allow users to exit their own functions

        
    def _on_key_release(self, key):
        if (key == pynput.keyboard.Key.esc):
            return False
        if (self.listener_active is False):
            return False
        
        if (self.custom_key_actions["on_key_release"] is not None):
            res = self.custom_key_actions["on_key_release"](key)
            if (res is False):
                return False # exit listener
        self._clear()
        self.render()

        
    def stop_listener(self):
        self.listener_active = False
       
    

    def _find_input_elements(self, container, full_render):
        if (type(container) == Box):
            for child in container.get_children():
                self._find_input_elements(child, full_render)
        elif (type(container) == Button or type(container) == Input):
            # self.input_elements.append(container)
            
            # find position of button in full_render
            # r_split = fstrip(full_render).split("\n")
            # c_split = fstrip(container.get_cached_render()).split("\n")
            # lines_found = []
            # for i in range(len(r_split)):
            #     for j in range(len(c_split)):
            #         if (c_split[j] in r_split[i]):
            #             index = r_split[i].find(c_split[j])
            #             # print("Match found on line " + str(i) + " at index " + str(r_split[i].index(c_split[j])))
            #             # print(r_split[i][index:index+len(c_split[j])])
            #             lines_found.append([i, index, index + len(c_split[j])])
            # corner = [lines_found[0][0], lines_found[0][1]]
            # width = lines_found[0][2] - lines_found[0][1]
            # height = len(lines_found)
            if (container.get_disabled() is True):
                return
            
            self.input_elements.append({
                # "corner": corner,
                # "width": width,
                # "height": height,
                "element": container,
                "id": container.get_id()
            })
            
            
        
        
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
                
            spl = txt.split("\n")
            presets = {
                "bg": None,
                "fg": None,
                "dec": [],
                "val_ret": True
            }
            if (parent is not None):
                presets = {
                    "bg": parent.get_style("background"),
                    "fg": None,
                    "dec": [],
                    "val_ret":True
                }
            for i in range(container.get_style("marginTop")):
                spl.insert(0, printp(" " * max_width, presets))
            for i in range(container.get_style("marginBottom")):
                spl.append(printp(" " * max_width, presets))
            for i in range(len(spl)):
                spl[i] = printp(" " * container.get_style("marginLeft"), presets) + spl[i] + printp(" " * container.get_style("marginRight"), presets)
                
            txt = "\n".join(spl)

            container.set_cached_render(txt)
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
                for i in range(0, len(text), width):
                    t = text[i: i+width]
                    lines.append(t)
                if (len(lines[-1]) < width):
                    lines[-1] += " " * (width - len(lines[-1]))
                for i in range(len(lines)):
                    lines[i] = printp(lines[i], text_presets)
            presets = {
                "bg": parent.get_style("background"),
                "fg": None,
                "dec": [],
                "val_ret": True
            }
            for i in range(container.get_style("marginTop")):
                lines.insert(0, printp(" " * width, presets))
            for i in range(container.get_style("marginBottom")):
                lines.append(printp(" " * width, presets))
            for i in range(len(lines)):
                lines[i] = printp(" " * container.get_style("marginLeft"), presets) + lines[i] + printp(" " * container.get_style("marginRight"), presets)
            txt = "\n".join(lines)
                    
            container.set_cached_render(txt)
            return txt

        elif (type(container) == Button or type(container) == Input):
            width = container.get_style("width")
            if (width == "parent"):
                width = parent.get_style("width")
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
            if (self.selected_element_id == container.get_id()):
                # apply hover styles to text
                if ('background' in container.get_style("hover")):
                    presets["bg"] = container.get_style("hover")["background"]
                if ("color" in container.get_style("hover")):
                    presets["fg"] = container.get_style("hover")["color"]
                if ("font_weight" in container.get_style("hover")):
                    presets["dec"] = [container.get_style("hover")["font_weight"]]
            elif (container.get_disabled() is True):
                if ("background" in container.get_style("disabled")):
                    presets["bg"] = container.get_style("disabled")["background"]
                if ("color" in container.get_style("disabled")):
                    presets["fg"] = container.get_style("disabled")["color"]
                if ("font_weight" in container.get_style("disabled")):
                    presets["dec"] = [container.get_style("disabled")["font_weight"]]
            if (type(container) == Input and text == ""):
                text = container.get_placeholder()
                if ("color" in container.get_style("placeholder")):
                    presets["fg"] = container.get_style('placeholder')["color"]
                if ("background" in container.get_style("placeholder")):
                    presets["bg"] = container.get_style("placeholder")["background"]
                if ("font_weight" in container.get_style("placeholder")):
                    presets["dec"] = [container.get_style("placeholder")["font_weight"]]
            for i in range(0, len(text), width):
                t = text[i:i+width]
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
                if (self.selected_element_id == container.get_id()):
                    if ("border_style" in container.get_style("hover")):
                        border_style = borders(container.get_style("hover")["border_style"])
                    if ("border_color" in container.get_style("hover")):
                        border_presets["fg"] = container.get_style("hover")["border_color"]
                    if ("border_background" in container.get_style("hover")):
                        border_presets["bg"] = container.get_style("hover")["border_background"]
                elif (container.get_disabled() is True):
                    if ("border_color" in container.get_style("disabled")):
                        border_presets["fg"] = container.get_style("disabled")["border_color"]
                    if ("border_background" in container.get_style("disabled")):
                        border_presets["bg"] = container.get_style("disabled")["border_background"]
                    if ("border_style" in container.get_style("disabled")):
                        border_style = borders(container.get_style("disabled")["border_style"])
                
                first_line = printp(border_style["tl"] + (border_style["t"] * width) + border_style["tr"], border_presets)
                for i in range(len(spl)):
                    spl[i] = printp(border_style["l"], border_presets) + spl[i] + printp(border_style["r"], border_presets)
                last_line = printp(border_style["bl"] + (border_style["b"] * width) + border_style["br"], border_presets)
                txt = first_line + "\n" + "\n".join(spl) + "\n" + last_line
            # render margins
            presets = {
                "bg": None,
                "fg": None,
                "dec": [],
                "val_ret": True
            }
            if (parent is not None):
                presets = {
                    "bg": parent.get_style("background"),
                    "fg": None,
                    "dec": [],
                    "val_ret": True
                }
            spl = txt.split("\n")
            for i in range(container.get_style("marginTop")):
                spl.insert(0, printp(" " * width, presets))
            for i in range(container.get_style("marginBottom")):
                spl.append(printp(" " * width, presets))
            for i in range(len(spl)):
                spl[i] = printp(" " * container.get_style("marginLeft"), presets) + spl[i] + printp(" " * container.get_style("marginRight"), presets)
            txt = "\n".join(spl)
                    
            

            container.set_cached_render(txt)
            return txt
        elif (type(container) == ProgressBar):
            width = container.get_style("width")
            if (width == "parent"):
                width = parent.get_style("width")
            if (width > parent.get_real_width()):
                width = parent.get_real_width()
            
            height = container.get_style("height")
            if (height > parent.get_real_height()):
                height = parent.get_real_height()
            if (container.get_style("border") is True):
                width -= 2
                height -= 2

            fill_char = container.get_fill_char()
            percent = container.get_value() / container.get_max_value() 
            if (percent > 1):
                percent = 1
            if (percent < 0):
                percent = 0
            fill_width = int(width * percent)
            
            # gen fill text
            presets = {
                "bg": container.get_style("background"),
                "fg": container.get_style("fill_color"),
                "dec": [],
                "val_ret": True
            }
            fill_text = printp(fill_char * fill_width, presets)
            if (fill_width < width):
                fill_text += printp(" " * (width - fill_width), presets)
            
            # theoretically its not possible for the fill text to be taller than the height
            if (container.get_style("border") is True):
                border_style = borders(container.get_style("border_style"))
                border_presets = {
                    "fg": container.get_style("border_color"),
                    "bg": container.get_style("border_background"),
                    "dec": [],
                    "val_ret": True
                }
                first_line = printp(border_style["tl"] + (border_style["t"] * width) + border_style["tr"], border_presets)
                fill_text = printp(border_style["l"], border_presets) + fill_text + printp(border_style["r"], border_presets)
                last_line = printp(border_style["bl"] + (border_style["b"] * width) + border_style["br"], border_presets)
                txt = "\n".join([first_line, fill_text, last_line])

            # render margins
            presets = {
                "bg": None,
                "fg": None,
                "dec": [],
                "val_ret": True
            }
            if (parent is not None):
                presets = {
                    "bg": parent.get_style("background"),
                    "fg": None,
                    "dec": [],
                    "val_ret": True
                }
            spl = txt.split("\n")
            for i in range(container.get_style("marginTop")):
                spl.insert(0, printp(" " * width, presets))
            for i in range(container.get_style("marginBottom")):
                spl.append(printp(" " * width, presets))
            for i in range(len(spl)):
                spl[i] = printp(" " * container.get_style("marginLeft"), presets) + spl[i] + printp(" " * container.get_style("marginRight"), presets)
            txt = "\n".join(spl)

            container.set_cached_render(txt)
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
            "background": None,
            "hover": {
                "border_style": 3
            },
            "marginLeft": 0,
            "marginRight": 0,
            "marginTop": 0,
            "marginBottom": 0
        }
        self.id = None
        self.parent = None
        self.cached_render = None
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
        
    def set_cached_render(self, render):
        self.cached_render = render
    
    def get_cached_render(self):
        return self.cached_render

class Text: 
    def __init__(self, text):
        self.text = text
        self.styles = { # default styles
            "color": (255, 255, 255),
            "background": (0, 0, 0),
            "word_wrap": "break-word",
            "font_weight": "normal",
            "width": "parent",
            "height": 1,
            "marginLeft": 0,
            "marginRight": 0,
            "marginTop": 0,
            "marginBottom": 0
        }
        self.parent = None
        self.id = None
        self.cached_render = None
    
    
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
    
    def set_cached_render(self, render):
        self.cached_render = render
        
    def get_cached_render(self):
        return self.cached_render
    
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
            "hover": {
                "border_style": 3
            },
            "disabled": {
                "color": (150, 150, 150),
                "border_color": (150, 150, 150)
            },
            "marginLeft": 0,
            "marginRight": 0,
            "marginTop": 0,
            "marginBottom": 0
        }
        self.disabled = False
        self.id = id
        self.parent = None
        self.cached_render = None
        self.button_action = None
        
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
    
    def set_button_action(self, action):
        self.button_action = action
        
    def get_button_action(self):
        return self.button_action

    def set_cached_render(self, render):
        self.cached_render = render
    
    def get_cached_render(self):
        return self.cached_render
    
    def set_disabled(self, disabled):
        self.disabled = disabled
    
    def get_disabled(self):
        return self.disabled

class Input:
    def __init__(self, id):
        self.styles = { # default styles
            "color": (255, 255, 255),
            "background": None,
            "font_weight": "normal",
            "width": 30,
            "height": 1,
            "border": True,
            "border_style": 4,
            "border_background": None,
            "border_color": (255, 255, 255),
            "hover": {
                "border_style": 3,
            },
            "disabled": {
                "color": (150, 150, 150),
                "border_color": (150, 150, 150)
            },
            "placeholder": {
                "color": (200, 200, 200)
            },
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0
        }
        self.disabled = False
        self.parent = None
        self.id = id
        self.text = ""
        self.cached_render = None
        self.on_change_action = None
        self.on_submit_action = None # like pressing enter
        self.placeholder = "Enter text here..."
    
    def set_style(self, key, value):
        self.styles[key] = value

    def set_styles(self, styles):
        self.styles.update(styles)
        
    def get_styles(self):
        return self.styles

    def get_style(self, key):
        return self.styles.get(key, None)
    
    def set_parent(self, parent):
        self.parent = parent
        
    def get_parent(self):
        return self.parent
    
    def set_id(self, id):
        self.id = id
        
    def get_id(self):
        return self.id
    
    def set_text(self, text):
        self.text = text
    
    def get_text(self):
        return self.text
    
    def set_cached_render(self, render):
        self.cached_render = render
    
    def get_cached(self):
        return self.cached_render
    
    def set_disabled(self, disabled):
        self.disabled = disabled
        
    def get_disabled(self):
        return self.disabled
    
    def set_on_change_action(self, action):
        self.on_change_action = action
        
    def get_on_change_action(self):
        return self.on_change_action
    
    def set_on_submit_action(self, action):
        self.on_submit_action = action
        
    def get_on_submit_action(self):
        return self.on_submit_action
    
    def set_placeholder(self, placeholder):
        self.placeholder = placeholder
        
    def get_placeholder(self):
        return self.placeholder

class ProgressBar:
    def __init__(self, id):
        self.id = id
        self.max_value = 100
        self.value = 100
        self.children = []
        self.parent = None
        self.cached_render = None
        self.styles = {
            "width": 30,
            "height": 1,
            "border": True,
            "border_style": 4,
            "border_background": None,
            "border_color": (255, 255, 255),
            "background": None,
            "fill_color": (255, 255, 255),
            "marginTop": 0,
            "marginBottom": 0,
            "marginLeft": 0,
            "marginRight": 0
        }
        self.fill_char = "#"
    
    def set_style(self, key, value):
        self.styles[key] = value
    
    def set_styles(self, styles):
        self.styles.update(styles)
        
    def get_styles(self):
        return self.styles
    
    def get_style(self, key):
        return self.styles.get(key, None)
    
    def set_parent(self, parent):
        self.parent = parent
        
    def get_parent(self):
        return self.parent
    
    def set_id(self, id):
        self.id = id
        
    def get_id(self):
        return self.id

    def set_max_value(self, max_value):
        self.max_value = max_value
        
    def get_max_value(self):
        return self.max_value
    
    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        
    def remove_child(self, child):
        self.children.remove(child)
        
    def get_children(self):
        return self.children
    
    def set_cached_render(self, render):
        self.cached_render = render
        
    def get_cached_render(self):
        return self.cached_render
    
    def set_fill_char(self, char):
        self.fill_char = char
        
    def get_fill_char(self):
        return self.fill_char
    