import PIL
from PIL import Image, ImageDraw

# Convert signature to a binary image
img = Image.open('sign0.jpg')
img = img.convert('L').point((lambda x : 255 if x > 150 else 0), mode = '1')

# Drawing bounding box
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

# Locate Centroid
cx = 0
cy = 0 
n = 0
for x in range(0, width):
    for y in range(0, height):
        if (img.getpixel((x,y))) == 0:
            cx = cx + x
            cy = cy + y
            n = n + 1
cx = cx / n
cy = cy / n

# Divide the image at centroid to create four segments
draw.rectangle(((left, top), (cx, cy)))
draw.rectangle(((cx, top), (right, cy)))
draw.rectangle(((left, cy), (cx, bottom)))
draw.rectangle(((cx, cy), (right, bottom)))

# Find black to white transitions for each segment
prev = img.getpixel((0,0))
n = 0
transitions = []
for x in range(left, cx):
    for y in range(top, cy):
        curr = img.getpixel((x,y))
        if curr is 255 and prev is 0:
            n = n + 1
        prev = curr
transitions.append(n)

for x in range(cx, right):
    for y in range(cy,top):
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

# Output transition final image
print transitions
img.show()
