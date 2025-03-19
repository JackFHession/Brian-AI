import numpy as np
import time
import sys
import shutil
import os

vertices = 1.5 * np.array([
    [-1, -1, -1, -1], [1, -1, -1, -1], [-1, 1, -1, -1], [1, 1, -1, -1],
    [-1, -1, 1, -1],  [1, -1, 1, -1],  [-1, 1, 1, -1],  [1, 1, 1, -1],
    [-1, -1, -1, 1],  [1, -1, -1, 1],  [-1, 1, -1, 1],  [1, 1, -1, 1],
    [-1, -1, 1, 1],   [1, -1, 1, 1],   [-1, 1, 1, 1],   [1, 1, 1, 1]
])

edges = [(i, j) for i in range(16) for j in range(i) if bin(i ^ j).count('1') == 1]

def rotate_4d(points, angle, a, b):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    rot_matrix = np.eye(4)
    rot_matrix[a, a] = cos_a
    rot_matrix[a, b] = -sin_a
    rot_matrix[b, a] = sin_a
    rot_matrix[b, b] = cos_a
    return np.dot(points, rot_matrix.T)

def project_3d(points, w_dist=4):
    w = 1 / (w_dist - points[:, 3])
    return points[:, :3] * w[:, np.newaxis]

def project_2d(points, width, height):
    scale = min(width, height) // 3
    center_x, center_y = width // 2, height // 2
    projected = points[:, :2] * scale + np.array([center_x, center_y])
    return projected.astype(int), points[:, 2]

def draw_line(canvas, x0, y0, x1, y1, char="█"):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    while True:
        if 0 <= y0 < len(canvas) and 0 <= x0 < len(canvas[0]):
            canvas[y0][x0] = char
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def get_shading(depth):
    shades = " ░▒▓█"
    return shades[min(int((depth + 1) * (len(shades) / 2)), len(shades) - 1)]

def draw_tesseract():
    angle = 0
    while True:
        width, height = shutil.get_terminal_size((80, 24))
        width = max(width, 20)
        height = max(height, 10)

        canvas = [[" " for _ in range(width)] for _ in range(height)]

        rotated = rotate_4d(vertices, angle, 0, 3)
        rotated = rotate_4d(rotated, angle * 0.8, 1, 2)
        rotated = rotate_4d(rotated, angle * 0.5, 2, 3)
        rotated = rotate_4d(rotated, angle * 0.3, 0, 1)

        projected_3d = project_3d(rotated)
        projected_2d, depths = project_2d(projected_3d, width, height)

        for i, j in edges:
            p1, p2 = projected_2d[i], projected_2d[j]
            depth_avg = (depths[i] + depths[j]) / 2
            char = get_shading(depth_avg)
            draw_line(canvas, p1[0], p1[1], p2[0], p2[1], char)

        os.system("clear")

        sys.stdout.write("\033[H\033[J")
        for row in canvas:
            print("".join(row))
        sys.stdout.flush()

        time.sleep(0.05)
        angle += 0.1

if __name__ == "__main__":
    draw_tesseract()
