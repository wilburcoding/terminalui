# TerminalUI

Easy to use Python library for displaying UI in the terminal

Objectives:
 - Easy to use, container based UI layout with actually good layout engine?
 - CSS like properties
 - HTML like elements: text, uh...
 - ANSI based colors -> allow any color
 - Easy to update?

# TODO

 - [ ] Layout engine
   - [ ] Initiailization
   - [ ] Elements
     - [x] Text
     - [x] Container
       - [x] Container layouts -> just row and column for now probably
     - [ ] More TBD
   - [ ] Elements properties
   - [ ] Rendering
     - [ ] Initial rendering
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
 - How to fix styles resetting in the middle bcs of new text?
   - Don't immediate add filling spaces for text?
     - This would really mess up how the current formatting works though
   - I guess always use parent function styling -> mostly a background issue
 - Text styling uses extra characters. What to do?
   - Add formatting stripping function? Can use regular expressions for the special color ones

# Notes

I think we worry about stuff like margin and padding later

This sounded a lot easier in my head

Google says i should have helper methods instead of letting people access my variables directly so i guess im doing that

Normal Python shell ignores reset tokens. Command prompt seems to work. Also providing an extra new line at the end helps with the issue. VSCode commnad prompt also doesn't seem to work. Looks like splitting lines individually also helps with this issue. 