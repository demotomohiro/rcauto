import pathlib

p1 = pathlib.Path("test001.png")
p2 = pathlib.Path("test002.bmp")
p1.write_text("test001.png")
p2.write_text("test002.png")

a = input("start testrender")
print(a)
print("End of testrender")
