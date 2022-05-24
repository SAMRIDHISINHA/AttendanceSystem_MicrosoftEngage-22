import os
import cv2

path = 'images'
images = []
personName = []
myList = os.listdir(path)
try:
    myList.remove('.DS_Store')
except:
    pass
for cur_img in myList:
    current_img = cv2.imread(f'{path}/{cur_img}')
    images.append(current_img)
    personName.append(os.path.splitext(cur_img)[0])
print(personName)
def image_indir():
    return images
def image_name():
    return personName




