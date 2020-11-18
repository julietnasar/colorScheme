from PIL import Image, ImageDraw
import random
import Draw


def pixDist(r1,g1,b1,r2,g2,b2):
    # returns the euclidean distance btwn the 2 rgb values
    return int((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def getClustRow(clusters,centroid):
    
    for row in range(len(clusters)):
        print(clusters[row])
        print(centroid)
        if(centroid in clusters[row]):
            return row

def colorSchemer(path):
    
    img = Image.open(path)
    pix = img.load() # loads the pixel data, returns a PixelAccess Class
    width, height = img.size
    
    allPix = []
    for w in range(width):
        for h in range(height):
            cpix = pix[w,h]
            allPix.append(cpix)

    
    
    # selecting 8 unique random centroids (in form of indeces) to begin
    centroids = random.sample(allPix,8)
    
    print("old centroids:" + str(centroids))
    
    #clusters list
    clusters = [[c] for c in centroids]
    
    #remove centroids since they already clustered
    allPix = [i for i in allPix if i not in centroids]
    
    # we will start with the max distance and max pix values
    #minDist = pixDist(255,255,255,0,0,0)
    
    
    # print("original cluster len",[len(c) for c in clusters])
    
        
        # loop through all the pixels
    for p in allPix:
        # we will start with the max distance and max pix values
        minDist = pixDist(255,255,255,0,0,0)
            
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
                index = c # represents index of cluster list OR index of which centroid closest to
                
        # add that pixel to the closest centroid
        clusters[index].append(p)
            
        # change the centroid to average together 
        r1,g1,b1 = centroids[index]
        r2,g2,b2 = p
        
        # taking avg of old centroid and new cluster addition to
        # get new centroid
        centroids[index] = (r1+r2)//2,(g1+g2)//2,(b1+b2)//2
                   
            
    print("new centroids:" + str(centroids))
    # print("new cluster len",[len(c) for c in clusters])
    
    #Draw.picture(path,0,0)
    
    for i in range(len(centroids)):
        Draw.setColor(Draw.color(centroids[i][0],centroids[i][1],centroids[i][2]))
        Draw.filledRect(i*50,100,100,100)    
    
    
    
    
def main():
    
    #colorSchemer("sunflowerField.jpg")
    colorSchemer("pinkFlower.JPG")
    


    # Questions:
    # Q1. pinkFlower doesn't capture essense of pink flower
    # Q2. will show many similar colors that are prominent (like shades
        # of grey and black) but that don't make for a pretty palette
    # Q3. Takes a little over a minute to run - ideas to make more efficient
    
    # possible solutions:
    
    # use a diff measurement for clusters:eg density
           # could group by color bracket and then return avg from each
           # with > ____ obs
    # find more than 8 clusters and return only contrasting colors
    # or colors that aren't too similar
    
    

main()

