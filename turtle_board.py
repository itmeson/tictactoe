# coding: utf-8
"""Defines helper functions to draw a tic-tac-toe board using python turtle.

"""


from turtle import penup, goto, right, forward, left, pendown, circle


def x(pos, size):
    """Draws an X"""
    penup()
    goto(pos)
    right(90)
    forward(size / 2)
    right(90)
    forward(size / 2)
    right(135)

    pendown()
    forward(size * 1.4)
    penup()
    left(135)
    forward(size)
    pendown()
    left(135)
    forward(size * 1.4)
    penup()
    right(135)
    forward(size / 2)
    right(90)
    forward(size / 2)
    right(90)


def o(pos, size):
    """Draws an O"""
    penup()
    goto(pos)
    right(90)
    forward(size)
    left(90)
    pendown()
    circle(size)
    penup()
    left(90)
    forward(size)
    right(180)


def board(pos=[0, 0], size=100):
    """Draws the board"""
    penup()
    goto(pos)
    right(90)
    forward(size / 2)
    right(90)
    forward(1.5 * size)
    left(180)
    pendown()
    forward(3 * size)
    penup()
    left(90)
    forward(size)
    pendown()
    left(90)
    forward(3 * size)
    penup()
    right(90)
    forward(size)
    right(90)
    forward(size)
    right(90)
    pendown()
    forward(3 * size)
    penup()
    left(90)
    forward(size)
    left(90)
    pendown()
    forward(3 * size)
    penup()

