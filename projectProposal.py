from PIL import Image
import random
import Draw

def getPixList(path):
    img = Image.open(path)
    pix = img.load() # loads the pixel data, returns a PixelAccess Class
    width, height = img.size
    
    allPix = []
    for w in range(width):
        for h in range(height):
            cpix = pix[w,h]
            allPix.append(cpix)
    
    return allPix

def pixDist(r1,g1,b1,r2,g2,b2):
    # returns the euclidean distance btwn the 2 rgb values
    return int((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def getClustRow(clusters,centroid):
    
    for row in range(len(clusters)):
        print(clusters[row])
        print(centroid)
        if(centroid in clusters[row]):
            return row
            

def main():


    allPix = getPixList('sunflowerField.jpg')
    
    
    # selecting 8 unique random centroids (in form of indeces) to begin
    centroids = random.sample(allPix,8)
    
    print("old centroids:" + str(centroids))
    
    #clusters list
    clusters = [[c] for c in centroids]
    
    #remove centroids since they already clustered
    allPix = [i for i in allPix if i not in centroids]
    
    # we will start with the max distance and max pix values
    minDist = pixDist(255,255,255,0,0,0)
    
    
    print(len(allPix)//len(centroids))
    
    
    # we want each centroid to be allPix/8 length
    for j in range(len(allPix)//len(centroids)):
        
        print(j)
        
        # loop through all the pixels
        for p in allPix:
            
            # rgb values of the current pixel
            
            # appending the distance btwn current centroid and current pixel
            
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
                    closestC = centroids[c]
                    
            # add that pixel to the closest centroid
            clusters[c].append(p)
            
            
            r1,g1,b1 = centroids[c]
            r2,g2,b2 = p
            
            
            centroids[c] = (r1+r2)//2,(b1+b2)//2,(g1+g2)//2
            
        
        # resetting variables
        minDist = pixDist(255,255,255,0,0,0)

            
            
    print("new centroids:" + str(centroids))
    
    for i in range(len(centroids)):
        Draw.setColor(Draw.color(centroids[i][0],centroids[i][1],centroids[i][2]))
        Draw.filledRect(i*50,100,100,100)

main()

