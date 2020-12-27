#"I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus and the academic integrity policy of the CS department.”




from PIL import Image, ImageDraw
import pandas as pd
import random
import Draw
import math

# global variable
# the canvas width and height
canvasW = 686
canvasH = 600


# function purpose: finds the Euclidean distance between two color points by their
#                   rgb values
# function returns: the Euclidean distance between the two color points
def pixDist(r1,g1,b1,r2,g2,b2):
    # returns the euclidean distance btwn the 2 rgb values
    return int((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)


# function purpose: uses a clustering algorithm to create groups of the "closest"
#                   pixels and modifies the centroid, or average pixel value,
#                   with each new addition to each cluster
# function returns: None
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


# function purpose: sorts the clusters from darkest (closest to (255,255,255))
#                   to lightest (closest to (0,0,0)
# function returns: a new list with the sorted centroids
def sortedDL(centroids):
    
    # getting a list of tuples with each centroid's index
    # and each centroid's Euclidean distance from Black (255,255,255)
    distFromBlack = [(i,pixDist(centroids[i][0],centroids[i][1],centroids[i][2],255,255,255)) for i in range(len(centroids))]
    
    # sorting the list created above by the second element which is the distance
    # from black (255,255,255)
    distFromBlack = sorted(distFromBlack, key = lambda x: x[1])

    # return a list of the centroids ordered by their distance from black
    # the order is stored in the above list distFromBlack
    return [centroids[i[0]] for i in distFromBlack]
        
    
        
# function purpose: reads in a color names dataset and matches each rgb value
#                   in the centroids list to their closest color names
# function returns: a new list of color names that corresponds to the inputted 
#                   centroids list
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


# function purpose: finds the hex values of a pixel based off its rgb values
# function returns: a list of hex values corresponding to the inputted list
#                   of centroids
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

# function purpose: Draws the picture in a centered and aesthetically pleasing manner
# function returns: None
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
    
    # draw white border around picture
    
    Draw.setColor(Draw.WHITE)
    Draw.rect(picX,picY,picW,picH)


# function purpose: Draws the color boxes with their names, hex values, and rgb values
# function returns: None
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
    
# function purpose: Draws the color schemer logo
# function returns: None
def drawLogo(logoX,logoY):
    #print(Draw.availableFonts())
    
    Draw.setFontFamily("Broadway")
    Draw.setFontSize(30)
    
    Draw.setColor(Draw.BLACK)
    Draw.filledRect(logoX,logoY,425,50)
    
    Draw.setColor(Draw.WHITE)
    Draw.string("The Color Schemer", logoX+10, logoY)

# function purpose: Draws the final picture
# function returns: None
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
    
    # draw the colored boxes from the centroids
    drawColors(centroids,centroidNames,centroidHex, rectH, rectW, rectX, rectY)
    
    # draw the color schemer logo
    drawLogo(rectX, rectY)

# function purpose: Function that puts everything together, finding
#                   the centroids and then drawing the final picture
# function returns: None
def colorSchemer(path):
    
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
    
    print("new centroids:" + str(centroids))
    
    # sort the centroids from  darkets Black = (0,0,0) to lightest White = (255,255,255)
    centroids = sortedDL(centroids)
            
    # get lists of the hex values and the closest names
    centroidNames = getColorName(centroids)
    centroidHex = getHex(centroids)    
    
    # draw the final picture
    drawPalette(path, centroids, width, height, centroidNames, centroidHex)
    
    
def main():
    
    
    colorSchemer("pics/itWorked.gif")
    #colorSchemer("pics/rainbow.gif")
    #colorSchemer("pics/galaxy.gif")
    #colorSchemer("pics/pinkClouds.gif")
    #colorSchemer("pics/ocean.gif")
    #colorSchemer("pics/flower.gif")
    #colorSchemer("pics/aaronJudge.gif")
    #colorSchemer("pics/stickFigures.gif")
    


main()

# Qs

# 1) global variables ok?