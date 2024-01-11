"""
Wprowadzenie
############

Do realizacji projektu została zaimplementowana struktura HalfEdge, w celu łatwego przechodzenia po wierzchołkach/trójkątach.

Podstawowe informacje techniczne
################################

* Język Python w wersji 3.10,
* Precyzja operacji zmiennoprzecinkowych — domyślna w python - zazwyczaj odpowiada double w języku C
* Narzędzie do wizualizacji - bibiloteka mathplotlib
* Reprezentacja punktu — krotka współrzędnych punku (liczb zmiennoprzecinkowych)

Przykłady użycia
################

::

    from halfedge import *
    from visualizer import *

    p = [(1.0, 1.0),
         (2.0, 6.5),
         (9.0, 1.0),
         (17.5, 5.0),
         (19.0, 13.5),
         (12.0, 16.0),
         (11.5, 12.0),
         (6.0, 12.0)]
    t = [(0, 2, 1),
         (1, 2, 7),
         (6, 7, 2),
         (2, 3, 6),
         (6, 3, 4),
         (6, 4, 5)]
    mesh = triangles_to_segments(p,t)
    he = create_half_edge_structure(p, t)
    draw_halfedge_structure(he,mesh)

Przykładowa wizualizacja
########################

.. image:: triangles.png
    :align: center
"""

Point = tuple[float, float]
Triangle = tuple[int, int, int]
Segment = tuple[Point, Point]
Connection = tuple[int, int]

class HalfEdge:
    """
    Reprezentacja półkrawędzi.
    """
    def __init__(self,v: 'Vertex', face: 'Face') -> None:
        self.vertex = v
        self.twin = None
        self.face = face
        self.next = None
        self.prev = None
        

class Vertex:
    """
    Reprezentacja wierzchołka.
    """
    def __init__(self,cords: Point, index: int) -> None:
        self.cords = cords
        self.index = index
        self.halfEdge = None

class Face:
    """
    Reprezentacja trójkąta.
    """
    def __init__(self,points: list[Point],index: int) -> None:
        self.points = points
        self.index = index
        self.halfEdge = None

def ccw(a: Point, b: Point, c: Point) -> float:
    """
    Pole równoległoboku rozpiętego na wektorach (ab) i (ac). Będzie ujemne, gdy podane punkty będą ułożone zgodnie z ruchem wskazówek zegara.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def sort_points(points: list[tuple[Point, int]]) -> list[tuple[Point, int]]:
    """
    Funkcja sortująca punkty.
    """
    base_point = min(points, key=lambda p: (p[0][1], p[0][0]))[0]
    return sorted(points, key=lambda p: ccw(base_point, p[0], (p[0][0], p[0][1] + 1)),reverse=True) 

def create_half_edge_structure(points: list[Point],triangles: list[int]) -> list[HalfEdge]:
    """
    Funkcja tworzy strukturę HalfEdge.
    """
    p = [Vertex(cords,i) for i,cords in enumerate(points)]
    t = [Face(inds,i) for i,inds in enumerate(triangles)]
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
        for j in range(i+1,len(half_edge)):
            if half_edge[i].next.vertex == half_edge[j].vertex and half_edge[j].next.vertex == half_edge[i].vertex:
                half_edge[i].twin = half_edge[j]
                half_edge[j].twin = half_edge[i]
                
    return half_edge

def triangulation_reader(number: int) -> tuple[list[Point], list[Triangle]]:
    """
    Funkcja czyta triangulację o zadanym numerze z katalogu *tests/*.
    """
    points, triangles = [], []
    with open('tests/test' + number + 'points', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split(' ')
            x = float(line[0])
            y = float(line[1])
            points.append((x,y))
    with open('tests/test' + number + 'triangles', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split(' ')
            id1 = int(line[0])
            id2 = int(line[1])
            id3 = int(line[2])
            triangles.append((id1,id2,id3))
    return points,triangles

def triangles_to_segments(points: list[Point], triangles: list[Triangle]) -> list[Segment]:
    """
    Funkcja tworzy i zwraca listę odcinków łączących punkty.
    """
    segments = []
    for ind1,ind2,ind3 in triangles:
        if (points[ind1],points[ind2]) not in segments and (points[ind2],points[ind1]) not in segments:
            segments.append((points[ind1],points[ind2]))
        if (points[ind1],points[ind3]) not in segments and (points[ind3],points[ind1]) not in segments:
            segments.append((points[ind1],points[ind3]))
        if (points[ind2],points[ind3]) not in segments and (points[ind3],points[ind2]) not in segments:
            segments.append((points[ind2],points[ind3]))
    return segments

def triangles_to_connections(triangles: list[Triangle]) -> list[Connection]:
    """
    Funkcja tworzy i zwraca listę odcinków łączących punkty w postaci listy par indeksów.
    """
    connections = []
    for i,ii,iii in triangles:
        if (i,ii) not in connections and (ii,i) not in connections:
            connections.append((i,ii))
        if (i,iii) not in connections and (iii,i) not in connections:
            connections.append((i,iii))
        if (ii,iii) not in connections and (iii,ii) not in connections:
            connections.append((ii,iii))
    return connections

def point_in(triangle: Triangle, point: Point) -> bool:
    """
    Funkcja sprawdza czy punkt zawiera się w podanym trójkącie.
    """
    x, y = point
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]

    alpha = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
    beta = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
    gamma = 1 - alpha - beta

    return alpha >= 0 and beta >= 0 and gamma >= 0 and alpha + beta + gamma == 1

def apex_surroundings_basic(point: int, points: list[Point], connections: list[Connection]) -> list[int]:
    """
    Funkcja wyznacza otoczenie punktu (2 warstwy incydentnych wierzchołków), mając do dyspozycji triangulację w postaci listy punktów i listy odcinków.
    """
    surrounding = []
    for i,j in connections:
        if i == point:
            if j not in surrounding:
                surrounding.append(j)
            for a,b in connections:
                if a == j and b != point and b not in surrounding:
                    surrounding.append(b)
                elif b == j and a != point and a not in surrounding:
                    surrounding.append(a)
        elif j == point:
            if i not in surrounding:
                surrounding.append(i)
            for a,b in connections:
                if a == i and b != point and b not in surrounding:
                    surrounding.append(b)
                elif b == i and a != point and a not in surrounding:
                    surrounding.append(a)
    return surrounding

def triangle_surroundings_basic(tri_id: int, triangles: list[Triangle]) -> tuple[list[int], list[int]]:
    """
    Funkcja wyznacza otoczenie trójkąta (2 warstwy incydentnych trójkątów), mając do dyspozycji listę trójkątów.
    """
    triangle = triangles[tri_id]
    surrounding = []
    for i,(t1,t2,t3) in enumerate(triangles):
        if i != tri_id and (t1 in triangle or t2 in triangle or t3 in triangle):
            if i not in surrounding:
                surrounding.append(i)
    res = copy.copy(surrounding)
    for j in surrounding:
        temp_triangle = triangles[j]
        for k,(t1,t2,t3) in enumerate(triangles):
            if k != tri_id and (t1 in temp_triangle or t2 in temp_triangle or t3 in temp_triangle):
                if k not in res:
                    res.append(k)
    return surrounding, res

def find_triangle_basic(triangles: list[Triangle], points: list[Point], point: Point, start_triangle: Triangle) -> int:
    """
    Funkcja szuka trójkąta, w którym znajduje się dany punkt.
    """
    triangle = [points[triangles[start_triangle][0]],points[triangles[start_triangle][1]],points[triangles[start_triangle][2]]]
    stack = [(triangle,start_triangle)]
    visited = [start_triangle]
    while stack:
        t, t_id = stack.pop(-1)
        if point_in(t,point):
            return t_id
        surrounding = triangle_surroundings_basic(t_id,triangles)[0]
        visited += [t_id]
        for s in surrounding:
            if s not in visited:
                stack.append(([points[triangles[s][0]],points[triangles[s][1]],points[triangles[s][2]]],s))

def apex_surroundings_halfedges(p: int, halfedges: list[HalfEdge]) -> list[int]:
    """
    Funkcja wyznacza otoczenie punktu (2 warstwy incydentnych wierzchołków), mając do dyspozycji triangulację w postaci stuktury HalfEdge.
    """
    def surr(p,halfedges):
        nonlocal p1
        surrounding = set()
        p_halfedges = []
        for halfedge in halfedges:
            if halfedge.vertex.index == p:
                p_halfedges.append(halfedge)
        while p_halfedges:
            he = p_halfedges.pop()
            if he.next.vertex.index != p1:
                surrounding.add(he.next.vertex.index)
            if he.prev.vertex.index != p1:
                surrounding.add(he.prev.vertex.index)
        return surrounding
    p1 = p
    s = list(surr(p,halfedges))
    s1 = copy.copy(s)
    for s_point in s1:
        s += surr(s_point,halfedges)
    return list(set(s))

def triangle_surroundings_halfedge(tri_id: int, halfedges: list[HalfEdge]) -> list[int]:
    """
    Funkcja wyznacza otoczenie trójkąta (2 warstwy incydentnych trójkątów), mając do dyspozycji triangulację w postaci stuktury HalfEdge.
    """
    def surr(tri_id,halfedges):
        nonlocal tri_id1
        he = None
        for h in halfedges:
            if h.face.index == tri_id:
                he = h
                break
        surrounding = []
        if he.twin != None and he.twin.face.index != tri_id1:
            surrounding.append(he.twin.face.index)
        he = he.next
        if he.twin != None and he.twin.face.index != tri_id1:
            surrounding.append(he.twin.face.index)
        he = he.next
        if he.twin != None and he.twin.face.index != tri_id1:
            surrounding.append(he.twin.face.index)
        he = he.next
        return surrounding 
    tri_id1 = tri_id
    surrounding = surr(tri_id,halfedges)
    s1 = copy.copy(surrounding)
    for face in s1:
        surrounding += surr(face,halfedges)
    return list(set(surrounding))

def find_triangle_halfedge(halfedges: list[HalfEdge], point: Point, start_triangle: int) -> int:
    """
    Funkcja szuka trójkąta, w którym znajduje się dany punkt, mając do dyspozycji triangulację w postaci stuktury HalfEdge..
    """
    def surr(he):
        surrounding = []
        if he.twin != None:
            surrounding.append(he.twin)
        he = he.next
        if he.twin != None:
            surrounding.append(he.twin)
        he = he.next
        if he.twin != None:
            surrounding.append(he.twin)
        return surrounding
    he = None
    for h in halfedges:
        if h.face.index == start_triangle:
            he = h
            break
    triangle = [he.vertex.cords,he.next.vertex.cords,he.prev.vertex.cords]
    tri_ind = he.face.index
    stack = [(triangle,tri_ind,he)]
    visited = [tri_ind]
    while stack:
        t,t_ind,halfedge = stack.pop(-1)
        if point_in(t,point):
            return t_ind
        surrounding = surr(halfedge)
        for h in surrounding:
            new_tri = [h.vertex.cords,h.next.vertex.cords,h.prev.vertex.cords]
            new_tri_ind = h.face.index
            if new_tri_ind not in visited:
                stack.append((new_tri,new_tri_ind,h))
                visited.append(new_tri_ind)
