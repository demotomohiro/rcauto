import pathlib

p1 = pathlib.Path("test001.png")
p2 = pathlib.Path("test002.bmp")
p3 = pathlib.Path("test003.hdr")
p4 = pathlib.Path("test004.jpg")
p1.write_text("test001.png")
p2.write_text("test002.png")
p3.write_text("HDR image")
p4.write_text("jpg image")

a = input("start testrender")
print(a)
print("End of testrender")
