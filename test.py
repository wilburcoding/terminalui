from tui import App, Box, Text

app = App()

main_box = Box()

heading = Text("Hello World lorem ipsum dolor sit amet, consectetuar aoeihgagehiwaoughioc heoiuh ei heoiuheoieioheiuoeoiheoi heoi iuoe")
main_box.add_child(heading)

box2 = Box()
main_box.add_child(box2)
box2.set_style("layout", "horizontal")
box2.set_style("width", 100)

text2 = Text("Testing horizontal layout 2 soemoaeg e EIU IOE Eoi hOEIF EOIH iouef hoiUE OIE foieU HOIeh ")
text2.set_style("width", 40)
box2.add_child(text2)

text3 = Text("Testing horizontal layout 3 ei uHIO oi heoIU Heoiu hEIOU HFoiuhe oiuFHOIEHOFIheoifuHEOIUHOIEHFOIue")
text3.set_style("width", 40)
box2.add_child(text3)

text4 = Text("Testing horizontal layout 4eafo  oiea ofhae oiae hfoi hioaf oiuawfe fiuwef iouaiuo eaiue ")
text4.set_style("width", 50)
box2.add_child(text4)

app.set_main_container(main_box)
# res = app._render_container(main_box, None)
# print(res)
app.render()
