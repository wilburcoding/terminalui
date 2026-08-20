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
     - [ ] Text
     - [ ] Container
       - [ ] Container layouts -> just row and column for now probably
     - [ ] More TBD
   - [ ] Elements properties
   - [ ] Rendering
     - [ ] Initial rendering
     - [ ] Figure out how to update things? 
 - [x] Color rendering engine
 - [ ] 

# IDEA DUMP

 - Layout engine
   - 
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

# Notes

I think we worry about stuff like margin and padding later

This sounded a lot easier in my head

