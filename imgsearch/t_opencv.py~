from cv2 import cv

haarpath = '/home/whille/Downloads/OpenCV-2.4.0/data/haarcascades/'
img=cv.LoadImage('face.png')
hc=cv.Load(haarpath + 'haarcascade_frontalface_alt.xml')
faces = cv.HaarDetectObjects(img, hc, cv.CreateMemStorage(),1.2, 2, 0)
for (x,y,w,h),n in faces:
    print x,y,w,h,n
    cv.Rectangle(img, (x,y), (x+w,y+h), 255)
cv.SaveImage("faces_detected.jpg", img)
        
