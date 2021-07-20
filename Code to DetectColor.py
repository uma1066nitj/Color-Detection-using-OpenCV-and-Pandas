#import numpy, Pandas and OpenCV
import numpy as np
import pandas as pd
import cv2


#Read the Image for which we are going to detect color
img = cv2.imread("ColoeDetect.jpg")

#convert the BGR image to RGB image because imread command by default convert the image into BGR Scale.
newImg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

#global variables
clicked = False
r = g = b = xpos = ypos = 0

#Read the CSV file and giving names to each column
index = ["color","color_name","hex","R","G","B"]
data = pd.read_csv("colors.csv",names=index,header=None)


#define draw function to get the coordinate(x,y) of mouse double click
def draw_function(events,x,y,flags,param):
    if events == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = newImg[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#create a window with "Image" name
cv2.namedWindow("Image")
cv2.setMouseCallback("Image",draw_function)

#define function for calculating the minimum distance from all colors to get the most matching color name
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(data)):
        d = abs(R - int(data.loc[i,"R"])) + abs(B - int(data.loc[i,"B"])) + abs(G - int(data.loc[i,"G"])) 
        
        if(d <= minimum):
            minimum = d
            cname = data.loc[i,"color_name"]
    
    return cname


while(1):
    cv2.imshow("Image",newImg)
    
    if(clicked):
        #cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(newImg,(20,20),(750,60),(b,g,r),-1)
        
        #Creating text string to display ( Color name and RGB values )
        text = getColorName(r,g,b) + "R = " + str(r) + "G = " + str(g) + "G = " + str(b)
        
        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )
        cv2.putText(newImg,text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        
        if(r+g+b >= 600):
            cv2.putText(newImg,text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked = False
        
        
     #Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF ==27:
        break
cv2.destroyAllWindows()
