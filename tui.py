# main handler for the ui
from colors import printc
class App:
    def __init__(self):
        self.main_container = None
        
    def set_main_container(self, container):
        self.main_container = container
    
    def get_main_container(self):
        return self.main_container
        
    def render(self):
        # TODO: implement rendering logic
        txt = self._render_container(self.main_container, None)
        print(printc(txt, fg=(0, 0, 0), bg=(255, 255, 255), val_ret=True) + "\n")
        pass
    
    def _render_container(self, container, parent):  
        if (type(container) == Box):
            txt = ""
            children = []
            for child in container.get_children():
                children.append(self._render_container(child, container))
            # check layout
            # print(children)
            if (container.get_style("layout") == "vertical"):
                # TODO: check for other styles
                txt += "\n".join(children)
            elif (container.get_style("layout") == "horizontal"):
                # check widths 
                max_width = container.get_style("width")
                y_offset = 0 # keep track for every row
                row = []
                lines = []
                
                for child in children:
                    if (len(lines) == 0):
                        spl = child.split("\n")
                        for i in range(len(spl)):
                            lines.append(spl[i])
                        continue
                    if (len(lines[-1]) + len(child) > max_width):
                        # new row -> clean up existing lines and add new row with child
                        y_offset += len(lines)
                    else:
                        # add on to current row
                        spl = child.split("\n")
                        if (len(spl) > len(lines)):
                            for i in range(len(lines), len(spl)):
                                lines.append(" " * len(lines[0]))
                        for i in range(len(spl)):
                            lines[i + y_offset] += spl[i]
                            
                # clean up lines

                        
                    
            print(txt)
            return txt
        elif (type(container) == Text):
            width = container.get_style("width")
            if (width == "parent"):
                width = parent.get_style("width") 
            width = int(width)
            text = container.get_text()
            # TODO: implement different word wrap styling logics
            if (container.get_style("word_wrap") == "break-word"):
                lines = []
                # TODO: implement different text styling
                for i in range(0, int(len(text) / width + 1)):
                    lines.append(text[i * width:(i+1)*width])
                if (len(lines[-1]) < width):
                    lines[-1] += " " * (width - len(lines[-1]))
            return "\n".join(lines)

            
                
            
            

class Box:
    def __init__(self):
        self.children = []
        self.styles = { # default styles
            "width": 100, 
            "border": False,
            "height": 10,
            "layout": "vertical"
        }
        self.parent = None
    
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
        

class Text: 
    def __init__(self, text):
        self.text = text
        self.styles = { # default styles
            "color": "white",
            "background": "black",
            "word_wrap": "break-word",
            "font_weight": "normal",
            "width": "parent"
        }
        self.parent = None
        
    
    
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
    

    
    