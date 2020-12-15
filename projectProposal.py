from PIL import Image, ImageDraw
import pandas as pd
import random
import Draw
import math

# global variable
canvasW = 686
canvasH = 600


def pixDist(r1,g1,b1,r2,g2,b2):
    # returns the euclidean distance btwn the 2 rgb values
    return int((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def getClustRow(clusters,centroid):
    
    for row in range(len(clusters)):
        print(clusters[row])
        print(centroid)
        if(centroid in clusters[row]):
            return row

# function modifies centroids and clusters
def clusterize(allPix,centroids,clusters):
    
    # loop through all the pixels
    for p in allPix:
        # we will start with the max distance and max pix values
        minDist = pixDist(255,255,255,0,0,0)
            
        for c in range(len(centroids)):
            r1,g1,b1 = centroids[c]
            r2,g2,b2 = p
            
            # find the pixels distance to the current centroid
            dist = pixDist(r1,g1,b1,r2,g2,b2)
            
            # if the pix distance from the centroid < the min distance btwn
            # that pix and the other centroids then make that dist the minDist
            # and that centroid the closest centroid
            if(dist < minDist):
                minDist = dist
                index = c # represents index of cluster list OR index of which centroid closest to
                
        # add that pixel to the closest centroid
        clusters[index].append(p)
            
        # change the centroid to average together 
        r1,g1,b1 = centroids[index]
        r2,g2,b2 = p
        
        # taking avg of old centroid and new cluster addition to
        # get new centroid
        centroids[index] = (r1+r2)//2,(g1+g2)//2,(b1+b2)//2   
        
        
# returns a list of the closest color name to each centroid in same order
def getColorName(centroids):
    
    # dictionary with centroid as key and a tuple of the closest color name as 
    # the data
    centroidNames = []
    
    
    # creating an empty 2d list
    data = {}
    
    # load in the data
    fin = open("colorNames.csv")
    
    # reading the first row of headers
    fin.readline()
    
    for line in fin:
        
        # getting a line from the file
        dat = line.strip()
        dat = line.split(",")
        
        # the color name is the 0th element of the line
        name = dat[0]
        
        # rgb values are dat[1],dat[2],and dat[3] respectively
        rgb = (dat[1],dat[2],dat[3])
        
        # add to the data dictionary
        data[name] = rgb
    
    fin.close()
        
    for c in centroids:
        
        # set minDist to the maximum dist possible
        minDist = pixDist(0,0,0,255,255,255)
        # closest colorName
        closestName = ""
        
        # looping through the color name data
        for k in data:
            
            
            r,g,b = c # centroid rgb vals
            r1,g1,b1 = data[k] # corresponding rgb vals to the key
            
            
            dist = pixDist(r,g,b,int(r1),int(g1),int(b1))
            
            # if the distance is less than the minDist 
            # the values at that color become the values of the current pix
            if(dist < minDist):
                closestName = k
                minDist = dist
        
        centroidNames+=[closestName]
        
    return centroidNames

# returns list of hex value of a centroid
# note hex is base 16
def getHex(centroids):
    
    hexVals = []
    
    decToHex = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:"A",11:"B",
                12:"C",13:"D",14:"E",15:"F"}
    
    
    
    for c in centroids:
        
        # hex values start with a #
        hexStr = "#"
        
        for i in range(len(c)):
            
            
            # the first hex digit is the hex equivalent of the int division by 16
            
            hexDig1 = decToHex[c[i]//16]
            
            #print("dig1",hexDig1)
            
            # the second hex digit is the hex equivalent of the remainder from
            # the first hex dig times 16
            hexDig2 = decToHex[int(abs(c[i]//16 - c[i]/16)*16)]
            
            # add the first and second dig to the hexstring
            hexStr+=(str(hexDig1)+str(hexDig2))
    
        
        hexVals+=[hexStr]
        
    return hexVals  

def drawPic(path, picW, picH, rectX, rectY, rectW, rectH, centroids):
    
    # we want to draw the picture centered in our frame
    
    # initialize values as if the picture is as big as the rectange or frame
    picX = rectX
    picY = rectY
    
    # if the pic width is less than the rect width
    if(picW < rectW):
        # then add the error//2 to the pic's x coord
        picX += (rectW - picW)//2
    # if the pic height is less than the rect height
    if(picH < rectH):
        # then add the error//2 to the pic's y coord
        picY += (rectH - picH)//2
    
    
    # draw the picture
    Draw.picture(path,picX,picY)

def drawColors(centroids,centroidNames,centroidHex, rectH, rectW, rectX, rectY):
    
    colorsH = 60 
    colorsW = rectW//len(centroids)    
    colorsStartX = rectX
    colorsY = rectY + (rectH-colorsH)
    
    
    wordsH = 45
    
    # drawing a white space for the text
    
    Draw.setColor(Draw.WHITE)
    Draw.filledRect(rectX,colorsY-wordsH,rectW,wordsH)    
    
    
    
    for i in range(len(centroids)):
    
        # set color to values in current centroid
        Draw.setColor(Draw.color(centroids[i][0],centroids[i][1],centroids[i][2]))
        
        colorsX = colorsStartX + i*colorsW
        
        Draw.filledRect(colorsX,colorsY,colorsW,colorsH)     
        
        # draw black line separating white space above colors
        Draw.setColor(Draw.BLACK)
        
        Draw.line(colorsX,colorsY-wordsH,colorsX,colorsY+colorsH)
        
        # draw the words text: hex and color names
        
        Draw.setColor(Draw.BLACK)
        
        # drawing hex and color names
        # colorsX+1 so word isn't on line/ for aesthetic reasons
        
        Draw.setFontSize(8)
        Draw.string(centroidNames[i],colorsX+1,colorsY-wordsH)         
        
        Draw.setFontSize(8)
        Draw.string(centroidHex[i],colorsX+1,colorsY-2*(wordsH//3))  
        
        Draw.setFontSize(8)
        rgb = "(" + str(centroids[i][0]) + ", " + str(centroids[i][1]) + ", " + str(centroids[i][2]) + ")"
        Draw.string(rgb,colorsX+1,colorsY-(wordsH//3))  
        
                
    
    
    
    # draw black border
    Draw.setColor(Draw.BLACK)
    Draw.rect(rectX,rectY,rectW,rectH)  
    Draw.rect(rectX,colorsY-wordsH,rectW,wordsH)
    

def drawLogo(logoX,logoY):
    print(Draw.availableFonts())
    
    
    Draw.text("Font Test", logoX, logoY)

def drawPalette(path, centroids, picW, picH, centroidNames, centroidHex):
    
    # set values for our frame
    rectW = 664 # must be multiple of 8 since we have 8 centroids
    rectH = 460
    rectX = (canvasW - rectW)//2 # since we want equal margins we divide the difference by 2
    rectY = 80    
    
    # setting background of frame to color to the darkest color of centroids
    clen = len(centroids)
    Draw.setColor(Draw.color(centroids[0][0],centroids[0][1],centroids[0][2]))
    
    # draw the frame
    Draw.filledRect(rectX,rectY,rectW,rectH)    
    
    # draw the picture
    drawPic(path,picW, picH, rectX, rectY, rectW, rectH-50, centroids)
    
    # to cover the side where the image goes over the frame on the right
    if(picW > rectW):
        
        coverX = rectX + rectW
        coverY = rectY
        coverW = canvasW - rectX - rectW
        coverH = canvasH
        
        Draw.setColor(Draw.WHITE)
        Draw.filledRect(coverX,coverY, canvasW - rectX - rectW, canvasH)
    
    
    drawColors(centroids,centroidNames,centroidHex, rectH, rectW, rectX, rectY)
    
def colorSchemer(path):
    
    # we are using PIL to do this since once we use a Draw
    # function we cannot re-set the canvas size
    #width,height = Image.open(path).size
    
    # to make sure the 8 palettes we draw can be evenly arranged
    #if(width%8 !=0):
        #width = width - width%8
    
    #setting the canvas size to:
    Draw.setCanvasSize(canvasW,canvasH)
    
    width,height = Draw.getPictureSize(path)
    
    allPix = []
    for w in range(width):
        for h in range(height):
            cpix = Draw.getPixel(path,w,h)
            allPix.append(cpix)
    
    # selecting 8 unique random centroids (in form of indeces) to begin
    centroids = random.sample(allPix,8)
    
    print("old centroids:" + str(centroids))
    
    #clusters list
    clusters = [[c] for c in centroids]
    
    #remove centroids since they already clustered
    allPix = [i for i in allPix if i not in centroids]
    
    # print("original cluster len",[len(c) for c in clusters])
    
    # clusterize the pixels by centroid
    clusterize(allPix,centroids,clusters)
    
    # sort the centroids
    centroids.sort()
            
    print("new centroids:" + str(centroids))
    # print("new cluster len",[len(c) for c in clusters])
    
    # get lists of the hex values and the closest names
    centroidNames = getColorName(centroids)
    centroidHex = getHex(centroids)    
    
    drawPalette(path, centroids, width, height, centroidNames, centroidHex)
    

    #for i in range(len(centroids)):
    #Draw.string(
    
    #print(centroids,"\n",centroidNames,"\n",centroidHex)
    
    
    
    
def main():
    
    #colorSchemer("sunflowerField.jpg")
    #colorSchemer("pinkFlower.JPG")
    #colorSchemer("pics/rainbow.gif")
    #colorSchemer("pics/galaxy.gif")
    #colorSchemer("pics/aaronJudge.gif")
    
    
    drawLogo(10,20)
    
    # load in the data
    #data = open("colorNames.csv")
    
    
    # reading the first row of headers
    #print(data.readline())
        

    
    #print(getColorName([(50,100,40),(2,36,200)]))
    
    #print(getHex([(2,30,40),(2,36,200)]))
    

main()