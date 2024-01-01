class HalfEdge:
    def __init__(self,v,face) -> None:
        self.vertex = v
        self.twin = None
        self.face = face
        self.next = None
        self.prev = None
        

class Vertex:
    def __init__(self,cords,i) -> None:
        self.cords = cords
        self.index = i
        self.halfEdge = None

class Face:
    def __init__(self,points) -> None:
        self.points = points
        self.halfEdge = None

def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def sort_points(points):
    base_point = min(points, key=lambda p: (p[0][1], p[0][0]))[0]
    return sorted(points, key=lambda p: ccw(base_point, p[0], (p[0][0], p[0][1] + 1)),reverse=True) 

def create_half_edge_structure(points,triangles):
    p = [Vertex(cords,i) for i,cords in enumerate(points)]
    t = [Face(inds) for inds in triangles]
    half_edge = []
    for i,(p1,p2,p3) in enumerate(triangles):
        temp = [(points[p1],p1),(points[p2],p2),(points[p3],p3)]
        temp = sort_points(temp)
        h1 = HalfEdge(p[p1],t[i])
        h2 = HalfEdge(p[p2],t[i])
        h3 = HalfEdge(p[p3],t[i])
        t[i].halfEdge = h1
        p[p1].halfEdge = h1
        p[p2].halfEdge = h2
        p[p3].halfEdge = h3
        h1.next = h2
        h2.next = h3
        h3.next = h1
        h1.prev = h3
        h2.prev = h1
        h3.prev = h2
        half_edge.extend([h1,h2,h3])
    
    for i in range(len(half_edge)):
        for j in range(len(half_edge)):
            if i == j:
                continue
            if half_edge[i].next.vertex == half_edge[j].vertex and half_edge[j].next.vertex == half_edge[i].vertex:
                half_edge[i].twin = half_edge[j]
                half_edge[j].twin = half_edge[i]
                
    return sorted(half_edge,key=lambda v: v.vertex.index)

        
    