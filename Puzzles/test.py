import unittest
from AbstractSudoku import AbstractSudoku
from Sudoku import Sudoku
from Kropki import Kropki
from KenKen import KenKen
import numpy as np
import pandas as pd
import os

# Test methods in LogicPuzzle
class AbstractSudokuTest(unittest.TestCase):
    
    def test_solve_cell(self):
        dim = 9
        values = set([ i+1 for i in range(dim) ])
        puzzle = AbstractSudoku(dimension=dim)

        for i in range(dim):
            for j in range(dim):
                assert( not puzzle.solved[j,i] )
                assert( puzzle.possible[j,i] == values )
                assert( puzzle.grid[j,i] == 0 )
        
        puzzle.solve_cell( (4,6), 2 )
        lower_values = set(values)
        lower_values.remove(2)
        for i in range(dim):
            for j in range(dim):
                if (i,j) == (4,6):
                    assert( puzzle.solved[j,i] )
                    assert( puzzle.possible[j,i] == set() )
                    assert( puzzle.grid[j,i] == 2 )
                elif i == 4 or j == 6:
                    assert( not puzzle.solved[j,i] )
                    assert( puzzle.possible[j,i] == lower_values )
                    assert( puzzle.grid[j,i] == 0 )
                else:
                    assert( not puzzle.solved[j,i] )
                    assert( puzzle.possible[j,i] == values )
                    assert( puzzle.grid[j,i] == 0 )

    def test_remove_possibility(self):
        dim = 9
        values = set([ i+1 for i in range(dim) ])
        puzzle = AbstractSudoku(dimension=dim)

        for i in range(dim):
            for j in range(dim):
                assert( not puzzle.solved[j,i] )
                assert( puzzle.possible[j,i] == values )
                assert( puzzle.grid[j,i] == 0 )
        
        x,y = 4,6
        lower_values = set(values)
        for val in range(dim-1):
            for i in range(dim):
                for j in range(dim):
                    if (i,j) == (4,6):
                        assert( not puzzle.solved[j,i] )
                        assert( puzzle.possible[j,i] == lower_values )
                        assert( puzzle.grid[j,i] == 0 )
                    else:
                        assert( not puzzle.solved[j,i] )
                        assert( puzzle.possible[j,i] == values )
                        assert( puzzle.grid[j,i] == 0 )

            puzzle.remove_possibility( (x,y), val+1 )
            lower_values.remove(val+1)

        lower_values = set(values)
        lower_values.remove(9)

        # Now the value should be set to 9
        for i in range(dim):
            for j in range(dim):
                if (i,j) == (4,6):
                    assert( puzzle.solved[j,i] )
                    assert( puzzle.possible[j,i] == set() )
                    assert( puzzle.grid[j,i] == 9 )
                elif i == 4 or j == 6:
                    assert( not puzzle.solved[j,i] )
                    assert( puzzle.possible[j,i] == lower_values )
                    assert( puzzle.grid[j,i] == 0 )
                else:
                    assert( not puzzle.solved[j,i] )
                    assert( puzzle.possible[j,i] == values )
                    assert( puzzle.grid[j,i] == 0 )

    def test_N_of_N_counts(self):
        dim = 9
        values = set([ i+1 for i in range(dim) ])
        test_coords = set( [ (i,0) for i in range(dim) ] )
        puzzle = AbstractSudoku(dimension=dim)
        group = puzzle.groups["row"][0]

        for i in range(dim)[2:]:
            puzzle.remove_possibility( (i,0), 1 )
            puzzle.remove_possibility( (i,0), 2 )
        
        puzzle.N_of_N_counts(group)

        for i in range(dim):
            if i == 0 or i == 1:
                assert( puzzle.possible[0,i] == set( [ 1,2 ] ) )
            else:
                assert( puzzle.possible[0,i] == set( [ 3,4,5,6,7,8,9 ] ) )

    def test_N_of_N_possibilities(self):
        dim = 9
        puzzle = AbstractSudoku(dimension=dim)
        group = puzzle.groups["row"][0]

        puzzle.possible[0,0] = set([1,2])
        puzzle.possible[0,4] = set([1,2])
        puzzle.N_of_N_possibilities(group)

        for coord in group["coords"]:
            x,y = coord
            if coord == (0,0) or coord == (4,0):
                assert( puzzle.possible[y,x] == set([1,2]) )
            else:
                assert( len( puzzle.possible[y,x] ) == 7 )
                assert( not 1 in puzzle.possible[y,x] )
                assert( not 2 in puzzle.possible[y,x] )

    def test_force_group(self):
        puzzle = AbstractSudoku(9)
        group1 = puzzle.groups["row"][2]
        group2 = puzzle.groups["column"][3]
        values = set([i+1 for i in range(puzzle.dim)])
        for x,y in group1["coords"]:
            if x != 3:
                puzzle.remove_possibility((x,y), 3)

        # Normally, N_of_N counts would take care of this specific case, but this should have the same effect and should generalize to
        # when subgrids become relevant (Test again there)
        puzzle.force_group(group1, "row")

        for row in range(puzzle.dim):
            for col in range(puzzle.dim):
                if (col, row) == (3,2):
                    assert( puzzle.possible[row,col] == values )
                elif (col, row) in group1["coords"] or (col, row) in group2["coords"]:
                    assert( puzzle.possible[row,col] == set([1,2,4,5,6,7,8,9]) )
                else:
                    assert( puzzle.possible[row,col] == values )

    def test_get_possibility_coords(self):
        dim = 9
        test_coords = set( [ (i,0) for i in range(dim) ] )
        puzzle = AbstractSudoku(dimension=dim)
        group = puzzle.groups["row"][0]

        for i in range(dim):
            coords = puzzle.get_possibility_coords( group, i+1 )
            assert( len(coords) == 9 )
            assert( coords == test_coords )
        
        puzzle.remove_possibility( (3,0), 1 )
        puzzle.remove_possibility( (3,0), 8 )
        puzzle.remove_possibility( (6,0), 1 )
        puzzle.remove_possibility( (7,0), 2 )

        for i in range(dim):
            coords = puzzle.get_possibility_coords( group, i+1 )
            if i+1 == 1:
                assert( len(coords) == 7 )
                assert( (3,0) not in coords )
                assert( (6,0) not in coords )
            elif i+1 == 2:
                assert( len(coords) == 8 )
                assert( (7,0) not in coords )
            elif i+1 == 8:
                assert( len(coords) == 8 )
                assert( (3,0) not in coords )
            else:
                assert( len(coords) == 9 )
                assert( coords == test_coords )

    def test_solved_in_group(self):
        dim = 9
        puzzle = AbstractSudoku(dimension=dim)
        group = puzzle.groups["row"][0]

        assert( puzzle.solved_in_group(group) == 0 )

        puzzle.solve_cell( (0,0), 1 )

        assert( puzzle.solved_in_group(group) == 1 )        

    def test_get_frequencies(self):
        dim = 9
        puzzle = AbstractSudoku(dimension=dim)
        group = puzzle.groups["row"][0]

        puzzle.remove_possibility( (0,0), 1 )
        puzzle.remove_possibility( (1,0), 1 )
        puzzle.remove_possibility( (2,0), 1 )
        puzzle.remove_possibility( (0,0), 2 )
        puzzle.remove_possibility( (5,0), 5 )

        coord_sets, frequencies = puzzle.get_frequencies(group)

        assert( len( frequencies[9] ) == 6 )
        assert( len( frequencies[8] ) == 2 )
        assert( len( frequencies[6] ) == 1 )

        for i in range(dim):
            val = i+1

            if val == 1:
                assert( len( coord_sets[val] ) == 6 )
                assert( not (0,0) in coord_sets[val] )
                assert( not (1,0) in coord_sets[val] )
                assert( not (2,0) in coord_sets[val] )
            elif val == 2:
                assert( len( coord_sets[val] ) == 8 )
                assert( not (0,0) in coord_sets[val] )
            elif val == 5:
                assert( len( coord_sets[val] ) == 8 )
                assert( not (5,0) in coord_sets[val] )
            else:
                assert( len( coord_sets[val] ) == 9 )

    def test_remove_from_complement(self):
        dim = 9
        values = set([ i+1 for i in range(dim) ])
        puzzle = AbstractSudoku(dimension=dim)
        group = puzzle.groups["row"][0]

        puzzle.remove_from_complement( group, [(0,0),(4,0)], [1,2] )

        for coord in group["coords"]:
            x,y = coord
            if coord == (0,0) or coord == (4,0):
                assert( puzzle.possible[y,x] == values )
            else:
                assert( len( puzzle.possible[y,x] ) == 7 )
                assert( not 1 in puzzle.possible[y,x] )
                assert( not 2 in puzzle.possible[y,x] )

class RelationalSudokuTest(unittest.TestCase):
    pass

class KropkiTest(unittest.TestCase):

    def test_factor_two(self):
        puzzle = Kropki(5)

        assert( puzzle.factor_two(1) == set([2]) )
        assert( puzzle.factor_two(2) == set([1,4]) )
        assert( puzzle.factor_two(3) == set() )
        assert( puzzle.factor_two(4) == set([2]) )
        assert( puzzle.factor_two(5) == set() )
    
    def test_difference_one(self):
        puzzle = Kropki(5)

        assert( puzzle.difference_one(1) == set([2]) )
        assert( puzzle.difference_one(2) == set([1,3]) )
        assert( puzzle.difference_one(3) == set([2,4]) )
        assert( puzzle.difference_one(4) == set([3,5]) )
        assert( puzzle.difference_one(5) == set([4]) )

    def test_black_dot(self):
        dim = 5
        puzzle = Kropki(dim)
        values = set([i+1 for i in range(dim)])

        assert( puzzle.possible[0,0] == values )
        assert( puzzle.possible[0,1] == values )

        result = puzzle.black_dot((0,0),(1,0))

        assert( result == set( [1,2,4] ) )

    def test_white_dot(self):
        puzzle = Kropki(5)

        dim = 5
        puzzle = Kropki(dim)
        values = set([i+1 for i in range(dim)])

        assert( puzzle.possible[0,0] == values )
        assert( puzzle.possible[0,1] == values )

        result = puzzle.white_dot((0,0),(1,0))

        assert( result == values )

        puzzle.remove_possibility((1,0), 4)
        result = puzzle.white_dot((0,0),(1,0))

        assert( result == set([1,2,3,4]) )

        puzzle.remove_possibility((1,0), 2)
        result = puzzle.white_dot((0,0),(1,0))

        assert( result == set([2,4]) )

        puzzle.remove_possibility((1,0), 1)
        result = puzzle.white_dot((0,0),(1,0))

        assert( result == set([2,4]) )      # Still have 3 adjacent to 2

    def test_blank_relation(self):
        dim = 5
        puzzle = Kropki(dim)

        puzzle.possible[0,1] = set([2,3])
        result = puzzle.blank_relation( (0,0), (1,0) )

        assert( result == set([1,5]) )

        puzzle.solve_cell((1,0),3)
        result = puzzle.blank_relation( (0,0), (1,0) )

        assert( result == set([1,5]) )

        puzzle = Kropki(dim)

        puzzle.solve_cell((1,0),2)
        result = puzzle.blank_relation( (0,0), (1,0) )

        assert( result == set([5]) )

    def test_solve(self):
        puzzle = Kropki(6)
        relations = puzzle.read_relations_from_csv("Puzzles\\Book2.csv")
        puzzle.load_relations(relations)
        puzzle.solve()
        assert( puzzle.is_solved() )

class SudokuTest(unittest.TestCase):
    def test_setup(self):
        puzzle = Sudoku()

        assert( len( puzzle.groups ) == 3 )
        assert( puzzle.groups["subgrid"].shape == (3,3) )

        assert( puzzle.groups["subgrid"][0,0]["coords"] == set( [ (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2) ] ) )
        assert( puzzle.groups["subgrid"][0,1]["coords"] == set( [ (3,0), (4,0), (5,0), (3,1), (4,1), (5,1), (3,2), (4,2), (5,2) ] ) )
        assert( puzzle.groups["subgrid"][0,2]["coords"] == set( [ (6,0), (7,0), (8,0), (6,1), (7,1), (8,1), (6,2), (7,2), (8,2) ] ) )

        assert( puzzle.groups["subgrid"][1,0]["coords"] == set( [ (0,3), (1,3), (2,3), (0,4), (1,4), (2,4), (0,5), (1,5), (2,5) ] ) )
        assert( puzzle.groups["subgrid"][1,1]["coords"] == set( [ (3,3), (4,3), (5,3), (3,4), (4,4), (5,4), (3,5), (4,5), (5,5) ] ) )
        assert( puzzle.groups["subgrid"][1,2]["coords"] == set( [ (6,3), (7,3), (8,3), (6,4), (7,4), (8,4), (6,5), (7,5), (8,5) ] ))

        assert( puzzle.groups["subgrid"][2,0]["coords"] == set( [ (0,6), (1,6), (2,6), (0,7), (1,7), (2,7), (0,8), (1,8), (2,8) ] ) )
        assert( puzzle.groups["subgrid"][2,1]["coords"] == set( [ (3,6), (4,6), (5,6), (3,7), (4,7), (5,7), (3,8), (4,8), (5,8) ] ) )
        assert( puzzle.groups["subgrid"][2,2]["coords"] == set( [ (6,6), (7,6), (8,6), (6,7), (7,7), (8,7), (6,8), (7,8), (8,8) ] ) )

    def test_solve(self):
        puzzle = Sudoku(9)
        grid = puzzle.read_grid_from_csv("Puzzles\\Book1.csv")
        puzzle.load_grid(grid)
        puzzle.solve()

class KenKenTest(unittest.TestCase):
    def test_get_permutations(self):
        puzzle = KenKen(4)
        group = puzzle.groups["row"][0]
        i = 0
        for x,y in group["coords"]:
            puzzle.possible[y,x] = set( [ (i+1)%5, (i+2)%5 ] )
            if 0 in puzzle.possible[y,x]:
                puzzle.possible[y,x].remove(0)
                puzzle.possible[y,x].add(1)
            i += 1
        
        results = []
        puzzle.get_permutations(group, 0, [], results)

        assert( len(results) == 16 )

        test_compare = []
        test_compare.append( [1,2,3,4] )
        test_compare.append( [1,2,3,1] )
        test_compare.append( [1,2,4,4] )
        test_compare.append( [1,2,3,1] )
        test_compare.append( [1,3,3,4] )
        test_compare.append( [1,3,3,1] )
        test_compare.append( [1,3,4,4] )
        test_compare.append( [1,3,3,1] )
        test_compare.append( [2,2,3,4] )
        test_compare.append( [2,2,3,1] )
        test_compare.append( [2,2,4,4] )
        test_compare.append( [2,2,3,1] )
        test_compare.append( [2,3,3,4] )
        test_compare.append( [2,3,3,1] )
        test_compare.append( [2,3,4,4] )
        test_compare.append( [2,3,3,1] )

        for combo in test_compare:
            assert( combo in results )

        puzzle = KenKen(4)
        group = puzzle.groups["row"][0]
        puzzle.solve_cell( (0,0), 2 )
        results = []
        puzzle.get_permutations(group, 0, [], results)

        assert( len(results) == 3*3*3 )

    def test_add_all(self):
        puzzle = KenKen(4)
        values = [1,3,4,6]
        assert( puzzle.add_all(values) == 14 )
    
    def test_subtract_all(self):
        puzzle = KenKen(4)
        values = [8,3,1,2]
        assert( puzzle.subtract_all(values) == 2 )

    def test_multiply_all(self):
        puzzle = KenKen(4)
        values = [1,3,4,6]
        assert( puzzle.multiply_all(values) == 72 )

    def test_divide_all(self):
        puzzle = KenKen(4)
        values = [6,3,2,1]
        assert( puzzle.divide_all(values) == 1 )
        values = [40,2,5,2]
        assert( puzzle.divide_all(values) == 2 )

    def test_cull_combos(self):
        puzzle = KenKen(6)
        blob = {}
        blob["coords"] = [ (0,0), (1,0), (2,0) ]
        blob["functions"] = []
        blob["properties"] = { "operation":puzzle.add_all, "total":6 }
        puzzle.blobs = {"A":blob}
        puzzle.load_blobs()
        group = puzzle.groups["arithmetic"][0]

        combos = []
        puzzle.get_permutations( group, 0, [], combos )
        assert( len( combos ) == 6*6*6 )

        combos = puzzle.cull_combos( combos, blob["properties"]["operation"], blob["properties"]["total"] )
        assert( len( combos ) == 3*2*1 )

    def test_cull_possibilities(self):
        puzzle = KenKen(6)
        blob = {}
        blob["coords"] = [ (0,0), (1,0), (2,0) ]
        blob["functions"] = []
        blob["properties"] = { "operation":puzzle.add_all, "total":6 }
        puzzle.blobs = {"A":blob}
        puzzle.load_blobs()
        group = puzzle.groups["arithmetic"][0]

        puzzle.cull_possibilities( group )
        for x,y in group["coords"]:
            assert( puzzle.possible[y,x] == set([1,2,3]) )

if __name__ == "__main__":
    unittest.main()