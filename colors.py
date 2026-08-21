
import re

RESET = "\x1b[0m"
BOLD = "\x1b[1m"

def printc(msg, bg=None, fg=(255,255,255), dec=[], val_ret=False): # dec = text decorations, val_ret is whether to return the value or not
    fstr = ""
    if (not bg is None):
        fstr+=f"\x1b[48;2;{bg[0]};{bg[1]};{bg[2]}m"
    
    if (not fg is None):
        fstr+=f"\x1b[38;2;{fg[0]};{fg[1]};{fg[2]}m";
    
    for d in dec:
        d = d.lower()
        if (d == "bold"):
            fstr+=BOLD
            
    fstr+=str(msg)
    fstr+=RESET
    
    if (val_ret):
        return fstr
    print(fstr) 
    
def printp(msg, presets):
    fstr = ""
    if (not presets["bg"] is None):
        fstr+=f"\x1b[48;2;{presets['bg'][0]};{presets['bg'][1]};{presets['bg'][2]}m"
    
    if (not presets["fg"] is None):
        fstr+=f"\x1b[38;2;{presets['fg'][0]};{presets['fg'][1]};{presets['fg'][2]}m"
    
    for d in presets["dec"]:
        d = d.lower()
        if (d == "bold"):
            fstr+=BOLD
        
    fstr+=str(msg)
    fstr+=RESET
    
    if (presets["val_ret"]):
        return fstr
    
    print(fstr)

def strip_formatting(msg):
    msg = msg.replace(RESET, "")
    msg = msg.replace(BOLD, "")
    msg = re.sub(r"\x1b\[38;2;\d{1,3};\d{1,3};\d{1,3}m", "", msg)
    msg = re.sub(r"\x1b\[48;2;\d{1,3};\d{1,3};\d{1,3}m", "", msg)
    return msg