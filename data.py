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

# Return images from image directory
def image_indir():
    return images

#Returns Person name
def image_name():
    return personName
