import unittest
from AbstractSudoku import AbstractSudoku

# Test methods in LogicPuzzle
class AbstractTypesTest(unittest.TestCase):
    
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
        pass

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

if __name__ == "__main__":
    unittest.main()