import pickle
from numpy import array, sum, allclose

file = open("icos.wb", "rb")
icos = pickle.load(file)

def contains(lis):
    
    def check(item):
        c = False
        for l in lis:
            if allclose(array(l) ,array(item)):
                c = True; break
        return c
    
    return check
                
def dist(x,y):
    
    return sum((x - y)**2)**0.5

def main():
    
    vertices = []
    for i in icos:
        vertices.append(i[0] + i[1])
    l = 400
    edges = []
    for i in range(30):
        for j in range(i):
            edge = [vertices[i],vertices[j]]
            if dist(edge[0], edge[1])< l + 2 and not contains(edges)(edge):
                edges.append(edge)
    print(edges)
    file = open("icosidodec.wb", "wb")
    pickle.dump(edges, file)
    file.close()

if __name__ == "__main__":
    main()


