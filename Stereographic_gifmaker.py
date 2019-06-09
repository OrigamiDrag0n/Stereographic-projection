##A stereographic projection gifmaker using ImageDraw and Imageio
##OrigamiDragon 08-09/06/19

from numpy import sum, array, full, uint8
from math import sin, cos, pi, inf, floor

def mat(a1,b1,c1):                                       #Rotation matrix
    a = a1*pi/180; b = b1*pi/180; c = c1*pi/180
    amat = array([[1,0,0],[0,cos(-a),sin(-a)],[0,-sin(-a),cos(-a)]])
    bmat = array([[cos(-b),0,-sin(-b)],[0,1,0],[sin(-b),0,cos(-b)]])
    cmat = array([[cos(-c),sin(-c),0],[-sin(-c),cos(-c),0],[0,0,1]])
    return cmat@amat@bmat

def vect(a,b,c,v):                                 #Rotates a vector
    matrix = mat(a,b,c)
    return matrix@array(v)

def rotate(a, b, c, edges):
    return [[vect(a, b, c, e[0]), vect(a, b, c, e[1])] for e in edges]

def norm(vector):                 #Length of a vectorector
    return sum(vector**2)**0.5

def rescale(vector, r):           #Rescales a vectorector to length r
    return vector*r/norm(vector)

def project(vector, r):           #Stereographic projection
    relative_vector = vector - array([0, 0, r])
    if relative_vector[-1] == 0:
        return array([inf, inf])
    else:
        projection_vector = (-2*relative_vector*r/relative_vector[-1])[:-1]
    return projection_vector

from PIL import ImageDraw, Image

def blank(h, w, filename):          #Makes a blank canvas for the drawing with ImageDraw later
    data = full((h, w, 3), 255, dtype=uint8)
    img = Image.fromarray(data, "RGB")
    img.save(f"{filename}.png")
    #img.show()
    
def draw(edges, r, n, h, w, filename):    #Splts each edge into n parts, and makes an image. Note that n should be *odd*. This screws up when an edge reaches infinity; avoid this.
    blank(h, w, "basis")
    canvas = Image.open("basis.png").convert("RGB")
    
    draw = ImageDraw.Draw(canvas)           #Dra
    for e in edges:
        v1 = array(e[0]); v2 = array(e[1]); line = []    #Takes the vertices of the edge; and creates a line object.
        for i in range(n + 1):
            v = (i*v1 + (n - i)*v2)/n                      #A partial point on the line
            line.append(tuple(array([h/2, w/2]) + project(rescale(v, r), r)))        #The point, which is now centred with the canvas, is added to the line.
        draw.line(line, fill = "Black", width = 5)

    canvas.save(f"{filename}.jpeg", "JPEG")           #Saves the image

def main(filename, outfilename, angle_function, minimum = 0, maximum = 360, step = 1): #Makes gif of rotating object with the angle_function a tuple from minimum to maximum with step 
    import pickle
    import imageio
    import os
    file = open(f"{filename}.wb", "rb")    #Opens the edge item from pickle
    edges = pickle.load(file)
    if os.path.exists(f"{outfilename}.gif"):
        os.remove(f"{outfilename}.gif")
    with imageio.get_writer(f'{outfilename}.gif', mode='I') as writer:
        theta = minimum
        while theta <= maximum:
            draw(rotate(*angle_function(theta), edges), 40, 39, 1000, 1000, f"{outfilename}")
            image = imageio.imread(f'{outfilename}.jpeg')
            writer.append_data(image)
            os.remove(f'{outfilename}.jpeg')
            theta += step
            print(str(int((theta - minimum)*100/(step*floor((maximum - minimum)/step))))+"% complete", end = "\r")    #Open in terminal for this to work; a progress indicator
    print(f"Loading complete. Open {outfilename}.gif")

if __name__ == "__main__":      #Fix the little glitches that happen every so often
    main("icosidodec", "icosidodeca_3", lambda x: (x, 0, 0))
    
