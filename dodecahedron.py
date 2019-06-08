import pickle
from numpy import array, sum, allclose

p = .5*(5**.5)+.5
basis = [[1,1,1],[0,p,1/p],[1/p,0,p],[p,1/p,0]]
vertices = []

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
    
    for i in range(-200,600,400):
        for j in range(-200,600,400):
            for k in range(-200,600,400):
                for l in range(4):
                    vertex = array([i*basis[l][0],j*basis[l][1],k*basis[l][2]])
                    if not contains(vertices)(vertex):
                        vertices.append(vertex)
                    
    edges = []
    l = (-1+5**.5)*200
    for i in range(20):
        for j in range(i):
            edge = [vertices[i],vertices[j]]
            if dist(edge[0],edge[1]) < l+2 and not(contains(edges)([edge[1], edge[0]]) or contains(edges)(edge)):
                edges.append(edge)

    file = open("dodec.wb", "wb")
    pickle.dump(edges, file)
    file.close()

if __name__ == "__main__":
    main()
