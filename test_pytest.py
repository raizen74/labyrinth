import pytest

from labyrinth_OOP import Solution

class TestSolution(object):

    def test_one(self):
        test1 = [
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", ".", ".", ".", "#", ".", ".", ".", "."],
        [".", ".", ".", ".", "#", ".", ".", ".", "."],
        [".", "#", ".", ".", ".", ".", ".", "#", "."],
        [".", "#", ".", ".", ".", ".", ".", "#", "."],
        ]
        assert Solution(test1).bfs() == 11

    def test_two(self):
        test2 = [
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["#", ".", ".", ".", "#", ".", ".", "#", "."],
            [".", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", "#", "."],
            [".", "#", ".", ".", ".", ".", ".", "#", "."],
        ]
        assert Solution(test2).bfs() == -1

    def test_three(self):
        test3 = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
        assert Solution(test3).bfs() == 2


    def test_four(self):
        test4 = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", "#", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", "#", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ]
        assert Solution(test4).bfs() == 16
