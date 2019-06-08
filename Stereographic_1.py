from numpy import sum, array, full, uint8
from math import sin, cos, pi, inf

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

def blank(h, w, filename):
    data = full((h, w, 3), 255, dtype=uint8)
    img = Image.fromarray(data, "RGB")
    img.save(f"{filename}.png")
    #img.show()
    
def draw(edges, r, n, h, w, filename):    #Splts each edge into n parts, and makes an image. Note that n should be *odd*
    blank(h, w, "basis")
    canvas = Image.open("basis.png").convert("RGB")
    
    draw = ImageDraw.Draw(canvas)
    for e in edges:
        v1 = array(e[0]); v2 = array(e[1]); lis = []
        for i in range(n + 1):
            v = (i*v1 + (n - i)*v2)/n
            lis.append(tuple(array([h/2, w/2]) + project(rescale(v, r), r)))
        draw.line(lis, fill = "Black", width = 5)

    canvas.save(f"{filename}.jpeg", "JPEG")

def main(filename, outfilename): #Makes gif of rotating object.
    import pickle
    import imageio
    import os
    file = open(f"{filename}.wb", "rb")
    edges = pickle.load(file)
    if os.path.exists(f"{outfilename}.gif"):
        os.remove(f"{outfilename}.gif")
    with imageio.get_writer(f'{outfilename}.gif', mode='I') as writer:
        for theta in range(360):
            draw(rotate(theta + 0.25, theta + 0.25, theta + 0.25, edges), 40, 39, 1000, 1000, f"{outfilename}")
            image = imageio.imread(f'{outfilename}.jpeg')
            writer.append_data(image)
            os.remove(f'{outfilename}.jpeg')
            print(theta)
    print("Done!")

if __name__ == "__main__":      #Fix the little glitches that happen every so often
    main("icosidodec", "icosidodeca_2")#"dodec")
    
