from tui import App, Box, Text
from colors import fstrip, printc
app = App()

main_box = Box()

heading = Text("Hello World lorem ipsum dolor sit amet, consectetuar aoeihgagehiwaoughioc heoiuh ei heoiuheoieioheiuoeoiheoi heoi iuoe")
heading.set_style("width", 100)
main_box.add_child(heading)
main_box.set_style("border", True)

box2 = Box()
main_box.add_child(box2)
box2.set_style("layout", "horizontal")
box2.set_style("width", 100)
box2.set_style("border", True)
box2.set_style("border_style", 2)
box2.set_style("border_color", (255, 0, 0))
box2.set_style("border_background", (200, 200, 200))

text2 = Text("Testing horizontal layout 2 soemoaeg e EIU IOE Eoi hOEIF EOIH iouef hoiUE O ")
text2.set_style("width", 48)
box2.add_child(text2)

text3 = Text("Testing horizontal layout 3 ei uHIO oi heoIU Heoiu hEIOU HFoiuhe oiuFHOIEHOFIheoifuHEOIUHOIEHFOIueaehoiu eah oiaeu heaoi")
text3.set_style("width", 48)
text3.set_style("color", (255, 0, 0))
text3.set_style("background", (255, 255, 255))

box2.add_child(text3)

text4 = Text("Testing horizontal layout 4eafo  oiea ofhae oiae hfoi hioaf oiuawfe fiuwef iouaiuo eaiue ")
text4.set_style("width", 50)
text4.set_style("font_weight", "bold")
box2.add_child(text4)

box3 = Box()
box3.set_style("width", 98)
box3.set_style("border", True)
box3.set_style("border_style", 4)


text5 = Text("Testing border overflow 3")
text5.set_style("background", (200, 200, 200))
box3.add_child(text5)
main_box.add_child(box3)
app.set_main_container(main_box)
# res = app._render_container(main_box, None)
# print(res)
app.render(debug=True)

# testing strip_formatting
t = printc("Hello World", bg=(255, 0, 0), fg=(255, 255, 255), dec=["bold"], val_ret=True)
