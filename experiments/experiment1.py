"""
Code by Adk2001tech, Github: https://github.com/Adk2001tech/OpenCV-YOLO-Python
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise

cap=cv2.VideoCapture(0)
i=0
_,frame=cap.read()
handPic = cv2.imread("picture_2021-11-14_18-05-26.jpg")
back=None
roi=cv2.selectROI(handPic)
(x,y,w,h)=tuple(map(int,roi))
while True:
    _,frame=cap.read()
    frame = cv2.flip(frame, 1)
    if i<60:
        i+=1
        if back is None:
            back=frame[y:y+h,x:x+w].copy()
            back=np.float32(back)
        else:
            
            cv2.accumulateWeighted(frame[y:y+h,x:x+w].copy(),back,0.2)
    else:
        #print(back.shape,frame.shape)
        back=cv2.convertScaleAbs(back)
        back_gray=cv2.cvtColor(back,cv2.COLOR_BGR2GRAY)
        frame_gray=cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY)
        
        img=cv2.absdiff(back_gray,frame_gray)

        _,img=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        con,hie=cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img2=img.copy()
        
        con=max(con,key=cv2.contourArea)
        conv_hull=cv2.convexHull(con)
        cv2.drawContours(img,[conv_hull],-1,225,3)
        
        top=tuple(conv_hull[conv_hull[:,:,1].argmin()][0])
        bottom=tuple(conv_hull[conv_hull[:,:,1].argmax()][0])
        left=tuple(conv_hull[conv_hull[:,:,0].argmin()][0])
        right=tuple(conv_hull[conv_hull[:,:,0].argmax()][0])
        cx=(left[0]+right[0])//2
        cy=(top[1]+bottom[1])//2

        dist=pairwise.euclidean_distances([left,right,bottom,top],[[cx,cy]])[0]
        radi=int(0.80*dist)
        
        circular_roi=np.zeros_like(img,dtype='uint8')
        cv2.circle(circular_roi,(cx,cy),radi,255,8)
        wighted=cv2.addWeighted(img.copy(),0.6,circular_roi,0.4,2)

        mask=cv2.bitwise_and(img2,img2,mask=circular_roi)
        #mask
        con,hie=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        count=0
        circumfrence=2*np.pi*radi
        for cnt in con:
            (m_x,m_y,m_w,m_h)=cv2.boundingRect(cnt)
            out_wrist_range=(cy+(cy*0.25))>(m_y+m_h)
            limit_pts=(circumfrence*0.25)>cnt.shape[0]
            if limit_pts and out_wrist_range:
                #print(limit_pts,out_wrist_range)
                count+=1



        cv2.putText(frame,'count: '+str(count),(460,70),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,250,0),thickness=4)
        cv2.rectangle(frame,(x,y),(x+w,y+h),255,3)
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)
        cv2.imshow('weight',wighted)
        
    k=cv2.waitKey(5)
    if k==27:
        break
    
cap.release()
cv2.destroyAllWindows()