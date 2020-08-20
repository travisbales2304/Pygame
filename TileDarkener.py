from PIL import Image, ImageEnhance 
im = Image.open("GameAssets\\Kings and Pigs\\Sprites\\08-Box\\Idle.png")
enhancer = ImageEnhance.Brightness(im)
enhanced_im = enhancer.enhance(.8)
enhanced_im.save("GameAssets\\BoxDark3.png")