from PIL import Image, ImageDraw

#Function to create bounding box for image
def boundingBox(img):
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
    return left, right, top, bottom

# Function to find the centroid
def findCentroid(img, left, right, top, bottom):
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
    h.write("%d, " % cx)
    h.write("%d\n" % cy)
    return cx, cy

#Function to find the transitions of image
def findTransitions(img, left, right, top, bottom, cx, cy):
    prev = img.getpixel((0,0))
    n = 0
    transitions = []
    #Calling function to calculate transitions for each segment around centroid
    for x in range(left, cx):
        for y in range(top, cy):
            curr = img.getpixel((x,y))
            if curr is 255 and prev is 0:
                n = n + 1
            prev = curr
    transitions.append(n)
    for x in range(cx, right):
        for y in range(cy, top):
            curr = img.getpixel((x,y))
            if curr is 255 and prev is 0:
                n = n + 1
            prev = curr
    transitions.append(n)
    for x in range(left, cx):
        for y in range(bottom, cy):
            curr = img.getpixel((x,y))
            if curr is 255 and prev is 0:
                n = n + 1
            prev = curr
    transitions.append(n)
    for x in range(cx, right):
        for y in range(bottom, cy):
            curr = img.getpixel((x,y))
            if curr is 255 and prev is 0:
                n = n + 1
            prev = curr
    transitions.append(n)
    #Writing output to file
    for i in transitions:
            g.write(" %d " % i)
    g.write("\n")
    return transitions

#Function to find the ratio
def findRatio(left, right, top, bottom): 
    ratio = (right - left)/(bottom - top)
    #Writing output to file
    f.write("%d\n" % ratio)
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
        t = findTransitions(img, left, right, top, bottom, cx, cy)
        r = findRatio(left, right, top, bottom)
       
if __name__=="__main__":
    f = open("ratio.txt", "a+")
    g = open("transitions.txt", "a+")
    h = open("centroid.txt", "a+")
    #Convert signature to a binary image
    img = Image.open('sign0.jpg')
    img = img.convert('L').point((lambda x : 255 if x > 150 else 0), mode = '1')
    #Function call to make bounding box and get coordinates
    left, right, top, bottom = boundingBox(img)
    draw = ImageDraw.Draw(img)
    #Function call to split image into 64 segments according to centroid
    split(img, left, right, top, bottom)
    f.close()
    g.close()
    h.close()
    #Show output image
    #img.show()
