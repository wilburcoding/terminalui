# imports - minimal
from miniui import App, Box, Text, Button, Input, ProgressBar

# init app
app = App()

# main container
main_box = Box()

main_box.set_style("border", True) # add border

sample_text = Text("Hello, World!")
sample_text.set_style("font_weight", "bold") # bold
sample_text.set_style("color", (200, 200, 200)) # gray

main_box.add_child(sample_text) # add text to main container

sample_button = Button("Click me", "button1")
sample_button.set_style("width", 20) # set button width

def on_button_click(button):
    print("Button clicked!")

sample_button.set_button_action(on_button_click) # set button action
main_box.add_child(sample_button) # add button to main container

sample_input = Input('input1')
sample_input.set_style("width", 20) # set input width
sample_input.set_placeholder("Enter text...") # set placeholder text

def on_submit(input_field):
    print("Input submitted with value: " + input_field.get_text())
    
sample_input.set_on_submit_action(on_submit) # set input submit action

main_box.add_child(sample_input) # add input to main container

sample_progress = ProgressBar("progress1")
sample_progress.set_style("width", 30) # set progress bar width
sample_progress.set_value(60) # set progress bar value - should be 60%
sample_progress.set_style("fill_color", (0, 255, 0))

main_box.add_child(sample_progress) # add progress bar to main container

app.set_main_container(main_box) # set main container to app

app.start_listener() # start live app listener