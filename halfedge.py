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

    p = [(0.0, 0.0),
         (1.0, 0.0),
         (2.0, 0.0),
         (0.0, 1.0),
         (1.0, 1.0),
         (2.0, 1.0),
         (0.0, 2.0),
         (1.0, 2.0),
         (2.0, 2.0)]
    t = [(0, 1, 3),
         (1, 4, 3),
         (1, 2, 4),
         (2, 5, 4),
         (3, 4, 6),
         (4, 7, 6),
         (4, 5, 7),
         (5, 8, 7)]
    mesh = triangles_to_segments(p,t)
    he = create_half_edge_structure(p, t)
    draw_halfedge_structure(he,mesh)

Przykładowa wizualizacja
########################

.. image:: triangles.png
    :align: center
"""

Point = tuple[float, float]

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
    Reprezentacja wierzchołka
    """
    def __init__(self,cords: Point, index: int) -> None:
        self.cords = cords
        self.index = index
        self.halfEdge = None

class Face:
    """
    Reprezentacja trójkąta
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

        
    
