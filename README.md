# TerminalUI

Easy to use Python library for displaying UI in the terminal

Objectives:
 - Easy to use, container based UI layout with actually good layout engine?
 - CSS like properties
 - HTML like elements: text, uh...
 - ANSI based colors -> allow any color
 - Button inputs -> allow users to select buttons using arrow keys?
   - Also maybe different frames? -> can select different frames
 - Easy to update?
 - HTML/CSS based importing? would be a lot cleaner than the normal

# TODO

 - [ ] Layout engine
   - [ ] Initiailization
   - [ ] Elements
     - [x] Text
     - [x] Container
       - [x] Container layouts -> just row and column for now probably
     - [x] Button
     - [ ] Links
   - [ ] Elements properties
   - [x] Rendering
     - [x] Initial rendering
       - [x] Text
       - [x] Different container layouts
       - [x] Borders
     - [ ] Figure out how to update things? 
 - [x] Color rendering engine
 - [ ] 

# IDEA DUMP

 - Layout engine  
   - Elements
     - Boxes
       - Width is x amount of char spaces. Height is in lines.
         - Percentage amounts in the future? 
         - Required field. For now. 
       - Border - always 1 grid space width
         - Later feature probably
       - Layout orientation
         - Vertical is easy -> just place on top and use size calculations
         - Horizontal -> Check if container fits. For text, since width is by default the width of parent container, it would break into 2 lines. 
           - Keep track of lines. Add additional if necesary before moving onto new row
     - Text
       - By default, width is parent container width
         - "parent" = parent width. Otherwise it should be a number
           - Theoretically there should always be a parent. 
             - WHat if parent also has "parent" as width..... Require containers to have a set width
       - Wrap is by default break word
         - Can figure out other options later
   - Generating output
     - Recursively generate the actual appearences of containers starting from main container
       - Main container should automatically be the size of the window
       - once generated, calculate size and figure out placement 
       - Once placement is figured out, generate full output
       - this is def a lot harder than it sounds
 - Color rendering
   - I guess we should just make an alt print function that just has alternate options for colors
   - Keep it simple. Want to focus on actual rendering and layout engine
 - Overall usage structure for users
   - Import module
   - Require a base container for the main layout -> created wiht user setup
   - User can add elements (text, container to start) to this main container and to other containers
     - Can pass parameters to style these elements
     - Can tag elements with ID to find them later
   - Call function to render or update UI 
     - Rendering just clears and pastes new UI. 
     - Start listener allows users to interact
       - same rendering function but allow users to select items
         - How to highlight selected items?
           - All items have by default a "hover" style -> maybe like a different border style (double line border)
 - How to fix styles resetting in the middle bcs of new text?
   - Don't immediate add filling spaces for text?
     - This would really mess up how the current formatting works though
   - I guess always use parent function styling -> mostly a background issue
 - Text styling uses extra characters. What to do?
   - Add formatting stripping function? Can use regular expressions for the special color ones
 - What to do if there is extra space at the end of a row for horizontal or vertical layouts??
   - Use parent styling (just background for the filling)
 - Borders
   - Separate outer and inner heights and width dimensions?
     - All children should be based on inner width
     - The actual outer size is read by the parent of the container
   - Borders not stacking? Why
     - Boxes use set height, not real height. Same with width. 
     - Want to make sure that outer box is the correct width
       - Forcing parent width as maximum
     - What about extra width from the prev?
       - can't forcibly remove?
       - Let's just put a warning since all dimensions are hard set
         - How to detect anyways?
 - Elements expansion
   - Lists? Should be easy
   - Buttons
     - Based on location 
       - Ex. if you press left arrow, it searches for any buttons left at a certain range (starting with the height of the original button)
       - If it doesn't find any buttons on this first path, it continually expands search radius in the direction 
       - Should allow functions to attach to buttons
     - Should essentially be the combination of box and text into a single element
   - Lists
     - Automatically fills and adds new line when necesary
     - Shoudl probably split this up into ordered and unordered lsits
   - Links?
     - Same way users are allowed to select elements?
     - Styles on hover - this would likely be a lot easier to do if we used a css like format
   - Can't really do different sized text
     - Or images
   - Text input?
     - If an input is selected all keyboard input is set into the text input
 - Actively looking for input?
   - keyboard module or pynput
   - Think im gonna use pynput. Looks a little easier to use.

# Notes

I think we worry about stuff like margin and padding later

This sounded a lot easier in my head

Google says i should have helper methods instead of letting people access my variables directly so i guess im doing that

Normal Python shell ignores reset tokens. Command prompt seems to work. Also providing an extra new line at the end helps with the issue. VSCode commnad prompt also doesn't seem to work. Looks like splitting lines individually also helps with this issue. 