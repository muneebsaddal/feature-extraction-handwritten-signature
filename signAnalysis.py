from PIL import Image, ImageDraw

#Function to create bounding box for image
def drawBoundingBox(img):
    width, height = img.size
    left = width
    right = 0
    top = height
    bottom = 0
    for x in range(0, width):
        for y in range(0, height):
            color = img.getpixel((x, y))
            if color == 0:
                if x > right:
                    right = x
                if x < left:
                    left = x
                if y > bottom:
                    bottom = y
                if y < top:
                    top = y
    draw = ImageDraw.Draw(img)
    draw.rectangle(((left, top), (right, bottom)))

    return img, left, right, top, bottom

# Function to find the centroid
def findCentroid(img, left, right, top, bottom):
        f = open("centroid.txt", "a+")
        cx = 0
        cy = 0
        n = 0
        for x in range(left, right):
            for y in range(top, bottom):
                if (img.getpixel((x,y))) == 0:
                    cx = cx + x
                    cy = cy + y
                    n = n + 1
        cx = cx / n
        cy = cy / n
        draw.rectangle(((left, top), (cx, cy)))
        draw.rectangle(((cx, top), (right, cy)))
        draw.rectangle(((left, cy), (cx, bottom)))
        draw.rectangle(((cx, cy), (right, bottom)))
        #Writing output to file
        f.write("%d\t" % cx)
        f.write("%d\n" % cy)
        f.close()

        return cx, cy

#Function for transition algorithm
def transitionAlgo(img, left, right, top, bottom, prev, n):
    for x in range(left, right):
        for y in range(top, bottom):
            curr = img.getpixel((x,y))
            if curr is 255 and prev is 0:
                n = n + 1
            prev = curr
    return n

#Function to find the transitions of image
def findTransitions(img, left, right, top, bottom,cx,cy):

    f = open("transitions.txt", "a+")
    prev = img.getpixel((0,0))
    n = 0
    transitions = []
    #Calling function to calculate transitions for each segment around centroid
    transitions.append(transitionAlgo(img, left, cx, top, cy, prev, n))
    transitions.append(transitionAlgo(img, cx, right, cy, top, prev, n))
    transitions.append(transitionAlgo(img, left, cx, bottom, cy, prev, n))
    transitions.append(transitionAlgo(img, cx, right, bottom, cy, prev, n))
    #Writing output to file
    for i in transitions:
            f.write("%d\t" % i)
    f.write("\n")
    f.close()

    return transitions

#Function to find the ratio
def findRatio(left, right, top, bottom):
    f = open("ratio.txt", "a+")
    ratio = (right - left)/(bottom - top)
    #Writing output to file
    f.write("%d\n" % ratio)
    f.close()

    return ratio

# Function to split the image recursively
def split(img, left, right, top, bottom, depth=0):
    cx, cy = findCentroid(img, left, right, top, bottom)
    if depth < 2:
        split(img, left, cx, top, cy, depth + 1)
        split(img, cx, right, top, cy, depth + 1)
        split(img, left, cx, cy, bottom, depth + 1)
        split(img, cx, right, cy, bottom, depth + 1)
    else:
        t = findTransitions(img, left, right, top, bottom,cx,cy)
        r = findRatio(left, right, top, bottom)
       
if __name__=="__main__":
    # Convert signature to a binary image
    img = Image.open('sign0.jpg')
    img = img.convert('L').point((lambda x : 255 if x > 150 else 0), mode = '1')
    #Function call to make bounding box and get coordinates
    img, left, right, top, bottom = drawBoundingBox(img)
    draw = ImageDraw.Draw(img)
    #Function call to split image into 64 segments according to centroid
    split(img, left, right, top, bottom)
    #Show output image
    img.show()
