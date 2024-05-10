from PIL import Image
import os

for i in range(128,263):
    print(i)
    filename = '{}.jpeg'.format(i)
    # img = Image.open(filename)
    os.remove(filename)
    print("File Removed!",i)
    # rgb_img = img.convert('RGB')
    # filenamea = '{}.jpg'.format(i)
    # rgb_img.save(filenamea)