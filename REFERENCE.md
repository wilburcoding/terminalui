# Reference Guide

Just a quick guide to helping you make use of the `TerminalUI` python ilbrary

## Installation

~~Not available on PYPI, but its super lightweight and thus easy to install. Just download the `tui.py` file and import anything you need. Example below.~~
Soon to be available on PYPI!

```python
from tui import App, Box
```

## Initialization

The main handler is part of the `App` class you can import from `tui`. This class takes in `0` initial parameters but there are a few methods that will come useful:
 - `set_main_container` - Set the main container for your layout. It should be of the `Box` class
   - Takes in one parameter, the box you are trying to set as the main one
 - `get_main_container` - In case you need to
 - `render` - Display a single, standalone render of your layout
   - Has on optional parameter: `debug`. Set `True` to get debug information (minimal info for now)
 - `start_listener` - Start live UI updates with key listener, this allows users to select and interact with UI elements
 - `stop_listener` - Ends live UI updates
 - `set_custom_key_action` - Add custom listener for a key action
   - Takes in 2 parameters: `action_type`, the type of action you want to set, and `action`, the actual function you want to attach to this action
   - Currently the only action types available are `on_key_press` and `on_key_release`
 - `get_custom_key_action` - Get a custom key action
   - Takes in 1 parameter: `action_type`
 - `clear_custom_key_action` - Clears saved custom key action
   - Takes in 1 parameter: `action_type`

## User Usage

For live updating mode, use left and right arrow keys to move around selectable elements. Press enter to submit or click on buttons/input elements. Type directly to add text to input elements when selected. 

Use ESC to exit out of live mode. 


## Element Classes
There are currently **5** available elements you can add to your UI layout. You can import the classes for these elements straight from `tui`

```python
from tui import App, Box, Text, Button, Input, ProgressBar
```

Methods that all element classes have:
 - `set_style(key, value)` where key is the parameter name and value is the new styling value
 - `set_styles(styles)` - set styling in bulk (updates styling info, does not replace)
 - `set_parent(parent)` - Set new parent. This only changes the listed parent, not what the actual parent may be
 - `get_styles()` - get all styling
 - `get_style(key)` - get styling for a specific key (style name)
 - `get_parent()` - get parent
 - `set_id(id)` - set ID for element
 - `get_id()` - get the current ID for element 
 - `get_cached_render()` - mostly for internal use but this is the cached rendering of the specific element
  
### Box
Quite literally just a box. Its the only element you can add children to.
 - Initialization (`Box()`) - no parameters required
 - `add_child(child)` - add element (child) into list of children
 - `remove_child(child)` - remove element (child) from list of children
 - `get_children()` - get full list of children

Available styling:
 - Sizing (int number): `width`, `height`
 - Layout: `layout` (horizontal or vertical)
 - Border: `border` (boolean), `border_style` (int 1-4), `border_background` (tuple rgb), `border_color` (tuple rgb)
 - Background: `background` (tuple rgb)
 - All margin styling (int): `marginLeft`, `marginRight`, `marginTop`, `marginBottom`

### Text
Text element! The simplest of elements
 - Initialization (`Text(text)`) - text is the value of the text
 - `set_text(text)` - set the value of the text element
 - `get_text()` - get the value of the element
  
Available styling:
 - Sizing (int number): `width`, `height`
 - Text: `color` (tuple rgb), `font_weight` (normal or bold), `word_wrap`: (just break-word for now)
 - Background: `background` (tuple rgb)
 - All margin styling (int): `marginLeft`, `marginRight`, `marginTop`, `marginBottom`

### Button
A button that can be triggered by user (or selected during live updating mode)
 - Initiailization (`Button(text, id)`) - text is the text inside the button and id is the element id
 - `set_text(text)` - Set the text within the button
 - `get_text()` - Get the text within the button
 - `set_button_action(action)` - Set the primary button action function
 - `get_button_action()` - Get the primary button action function
 - `set_disabled(disabled)`- Set disabled value (True or False)
 - `get_disabled()` - Get disabled value

Available styling:
 - Sizing (int number): `width`, `height`
 - Text: `color` (tuple rgb), `font_weight` (normal or bold)
 - Border: `border` (boolean), `border_style` (int 1-4), `border_background` (tuple rgb), `border_color` (tuple rgb)
 - Background: `background` (tuple rgb)
 - Hover styling: Set any style within `hover` to have it apply on hover
 - Disabled styling: Set any style within `hover` to have it apply when element disabled
 - All margin styling (int): `marginLeft`, `marginRight`, `marginTop`, `marginBottom`

### Input
An input element where users can (in live updating mode) input text. 
 - Initialization (`Input(id)`) - id is the element id
 - `set_text(text)` - set value of the input element 
 - `get_text()` - get value of the input element
 - `set_disabled(disabled)` - set disabled status of input element
 - `get_disabled()` - check disabled status of input element
 - `set_on_change_action(action)` - set input value change action function
 - `get_on_change_action()` - get input value change action function
 - `set_on_submit_action(action)` - set input submission action function
 - `get_on_submit_action()` - get input submission action function
 - `set_placeholder(placeholder)` - set placeholder value for element
 - `get_placeholder()` - get placeholder value for element

Available styling:
 - Sizing (int number): `width`, `height`
 - Text: `color` (tuple rgb), `font_weight` (normal or bold)
 - Border: `border` (boolean), `border_style` (int 1-4), `border_background` (tuple rgb), `border_color` (tuple rgb)
 - Background: `background` (tuple rgb)
 - Hover styling: Set any style within `hover` to have it apply on hover
 - Disabled styling: Set any style within `hover` to have it apply when element disabled
 - Placeholder text styling: Set styles for placeholder text for input element - only Text styling available
 - All margin styling (int): `marginLeft`, `marginRight`, `marginTop`, `marginBottom`

### ProgressBar
A nice, simple and customizable progress bar. 
 - Initialization (`ProgressBar(id)`) - id is the element id
 - `set_max_value(max_value)` - set the max value of the progress bar elemnt to max_value. Default max value is 100
 - `get_max_value()` - get max value of the progress bar element
 - `set_value(value)` - set the value of the progress bar to value
 - `get_value()` - get the value of the progress bar
 - `set_fill_char(char)` - set character filling progress bar to char. Defaults to #
 - `get_fill_char()` - get character filling progress abr

Available styling:
 - Sizing (int number): `width`, `height`
 - Border: `border` (boolean), `border_style` (int 1-4), `border_background` (tuple rgb), `border_color` (tuple rgb)
 - Fill text: `fill_color` (tuple rgb), `background` (background)
 - All margin styling (int): `marginLeft`, `marginRight`, `marginTop`, `marginBottom`