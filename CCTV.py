import cv2
import datetime

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
showTime = True
faceDetection = False
autoSave = False
delayTime = 0      

def draw_boundary(img, classifier, scale, minNeighbors, color,text):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray,scale,minNeighbors)
    coords = []
    for (x,y,w,h) in features:
        cv2.rectangle(img,(x,y), (x+w,y+h),color,2)
        coords= [x,y,w,h]
    return img, coords

def detect(img,faceCascade, cam_id):
    img, coords = draw_boundary(img,faceCascade,1.1,10,(255,0,0), "Face")    
    global delayTime

    if (len(coords) == 4 and autoSave and delayTime == 0):    #ถ้า autoSave เป็น on
        cv2.imwrite("data/"+ cam_id + "_"  + datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S") + ".jpg", img)  #save รูปแบบ original ไม่วาดกรอบ
        delayTime = 30   # 7.5 ต่อการหน่วงประมาณ 1 วินาที
    return img


cap1 = cv2.VideoCapture(0)
if cap1.isOpened():         #กรณีมีการเชื่อมต่อกล้องตัวที่ 1 
    print("webCamera 1 connected.")
else:
    print("Don't have any webCamera connected!")

ret,frame1 = cap1.read()
cv2.imshow('Camera 01',frame1)
cv2.moveWindow('frame1',10,10)

cap2 = cv2.VideoCapture(1)
if cap2.isOpened():         #กรณีมีการเชื่อมต่อกล้องตัวที่ 2 
    print("webCamera 2 connected.")
    ret,frame2 = cap2.read()
    cv2.imshow('Camera 02',frame2)
    cv2.moveWindow('frame2',300,300)

print("Successed..")
print("press: 'a' to on/off autoSave snapshot to file from face detection.") 
print("       'd' to on/off face detection.") 
print("       't' to show/hide camera detial and date/time.")
print("       '1' or '2' to snapshot picture from webCamera 1 or 2")
print("       'Esc' to exit.")

while(True):
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
    ret,frame1 = cap1.read()
    if showTime:
        cv2.putText(frame1,"Camera 01",(10,20),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),2)
        cv2.putText(frame1,time,(10,40),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.5,(255,0,0),2)
    if faceDetection:
        frame1 = detect(frame1,faceCascade, "cam01")    

    cv2.imshow('Camera 01',frame1)

    if cap2.isOpened():     #ถ้าเชื่อมต่อกล้องที่ 2
        ret,frame2 = cap2.read()
        if faceDetection:
            frame2 = detect(frame2,faceCascade, "cam02")

        if showTime:
            cv2.putText(frame2,"Camera 02",(10,20),cv2.FONT_HERSHEY_PLAIN,1.5,(255,0,0),2)
            cv2.putText(frame2,time,(10,40),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.5,(255,0,0),2)

        cv2.imshow('Camera 02',frame2)

    k = cv2.waitKey(33)
    if k == 27 :        # Esc key to stop
        print("program terminate..")
        break                
    elif k == 116:      # press 't'
        showTime = not showTime
    elif k == 100:      # press 'd'
        faceDetection = not faceDetection
        if(faceDetection):
            print("faceDetection : on")
        else:
            print("faceDetection : off")
    elif k == 49:       # press '1'
        cv2.imwrite("data/cam01_sav_" + datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S") + ".jpg", frame1)
        print("cam01 save snapshot.") 
    elif k == 50:       # press '2'
        if cap2.isOpened():     #ถ้าเชื่อมต่อกล้องที่ 2
            cv2.imwrite("data/cam02_sav_" + datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S") + ".jpg", frame2)
            print("cam02 save snapshot.")
        else:
            print("webcamera02 not connect.")
    elif k == 97:       # press 'a'
        autoSave = not autoSave
        if(autoSave):
            print("autoSave : on")
        else:
            print("autoSave : off")
    #else:
        #print(k)
    
    if delayTime > 0:
        delayTime -= 1

cap1.release()
cap2.release()
cv2.destroyAllWindows()
