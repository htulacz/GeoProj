import matplotlib.pyplot as plt
def draw_halfedge_structure(halfedge, mesh):
    plt.figure(figsize=(8, 8))
    i = 0
    j = 0
    c = ['red', 'magenta', 'green', 'orange', 'purple', 'black']

    # Obliczenie średniej długości krawędzi
    lengths = []
    for section in mesh:
        dx = section[1][0] - section[0][0]
        dy = section[1][1] - section[0][1]
        length = (dx ** 2 + dy ** 2) ** 0.5
        lengths.append(length)
    average_length = sum(lengths) / len(lengths)

    # Dostosowanie offset i shortening
    scale_factor = average_length / 7.5  # Można dostosować według potrzeb
    offset = 0.1 * scale_factor
    shortening = 0.1 * scale_factor

    for section in mesh:
        plt.plot([section[0][0], section[1][0]], [section[0][1], section[1][1]], color='blue')
    
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

        plt.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1], head_width=offset, head_length=offset, fc=c[j], ec=c[j])

        i += 1
        j = (i // 3) % 6

    plt.axis('equal')
    plt.show()
