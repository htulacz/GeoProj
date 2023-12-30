import matplotlib.pyplot as plt

def draw_halfedge_structure(halfedge,mesh):
    plt.figure(figsize=(8, 8))
    i = 0
    j = 0
    c = ['red','magenta','green','orange','purple','black']

    offset = 0.015  
    shortening = 0.1  
    for section in mesh:
        plt.plot([section[0][0],section[1][0]],[section[0][1],section[1][1]],color='blue')
    for h in halfedge:
        start = h.vertex.cords  
        end = h.next.vertex.cords  

        dx = start[0] - end[0]  
        dy = start[1] - end[1]  

        length = (dx ** 2 + dy ** 2) ** 0.5
        dx /= length
        dy /= length

        end = (end[0] + offset * dy, end[1] - offset * dx)
        start = (start[0] + offset * dy, start[1] - offset * dx)

        end = (start[0] + (end[0] - start[0]) * (1 - shortening), start[1] + (end[1] - start[1]) * (1 - shortening))
        start = (start[0] + (end[0] - start[0]) * (1 - shortening), start[1] + (end[1] - start[1]) * (1 - shortening))

        plt.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1], head_width=0.01, head_length=0.1, fc=c[j], ec=c[j])

        i += 1
        j = (i // 3) % 6

    plt.axis('equal')
    plt.show()