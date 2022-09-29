from math import sin, cos, radians
import numpy as np

def rotate(angle, rotationPoint, polygonPoints):

    pointsMatrix = [(polygonPoint[0] - rotationPoint[0], polygonPoint[1] - rotationPoint[1]) for polygonPoint in polygonPoints]

    rotationMatrix = [[cos(radians(angle)),  sin(radians(angle))],
                      [-sin(radians(angle)), cos(radians(angle))]]

    result = [[0, 0] for i in range(len(pointsMatrix))]

    for i in range(len(pointsMatrix)):
        for j in range(len(rotationMatrix[0])):
            for k in range(len(rotationMatrix)):
                result[i][j] += pointsMatrix[i][k] * rotationMatrix[k][j]

    for row in result:
        row[0] += rotationPoint[0]
        row[1] += rotationPoint[1]

    return result
