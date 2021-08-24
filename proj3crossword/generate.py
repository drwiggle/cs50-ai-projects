import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for word in self.crossword.words:
            for var in self.domains:
                if var.length != len(word) and word in self.domains[var]:
                    self.domains[var].remove(word)
        return None

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        if not self.crossword.overlaps[x,y]:
            return False
        xind, yind = self.crossword.overlaps[x,y]

        # Compute allowable letters for x[xind]
        validletters = set()
        for word in self.domains[y]:
            validletters.add(word[yind])
            
        origlen = len(self.domains[x])
        # remove words whose xind-th letter is not in validletters
        self.domains[x] = [word for word in self.domains[x] if word[xind] in validletters]

        # return T/F according to whether a change was made
        return len(self.domains[x]) != origlen
            
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        from collections import deque
        if arcs == None:
            arcs = self.crossword.overlaps.keys()
        queue = deque(arcs)

        
        while queue:
            x,y = queue.popleft()
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((x,z))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(var in assignment.keys() for var in self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # verify that no words are repeated
        if len(assignment.values()) != len(set(assignment.values())):
            return False
        
        for x in assignment:
            # verify that the value of x has correct length
            if len(assignment[x]) != x.length:
                return False

            # verify that all neighbors are consistent
            for y in self.crossword.neighbors(x):
                if y in assignment:
                    xind, yind = self.crossword.overlaps[x,y]
                    if assignment[x][xind] != assignment[y][yind]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # implement optimization later
        wordranks = dict()
        i = 1
        for word in self.domains[var]:
            count = 0
            for y in self.crossword.neighbors(var).difference(set(assignment.keys())):
                varind, yind = self.crossword.overlaps[var,y]
                count += len({w for w in self.domains[y] if w[yind] != word[varind]})
            wordranks[word] = (count, i)
            i += 1

        # print(f"rankings: {wordranks}")
        words = list(self.domains[var])
        # print(f"Orig list: {words}")
        words.sort(key = lambda w: wordranks[w])
        # print(f"sorted list: {words}")

        return words

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining_vars = list(set(self.domains.keys()) - set(assignment.keys()))
        varranks = dict()
        i=1
        for x in remaining_vars:
            varranks[x] = (len(self.domains[x]), -len(self.crossword.neighbors(x)), i)
            i += 1
        # print(varranks)
        remaining_vars.sort(key = lambda x : varranks[x])
        # print(remaining_vars)
        return remaining_vars

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)[0]
        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = word
            if self.consistent(new_assignment):
                orig_domains = self.domains
                # Make inferences
                inferences = self.ac3(arcs = [(y,var) for y in
                                              self.crossword.neighbors(var)])
                if inferences:
                    inferred_vars = {y:self.domains[y][0] for y in
                                     self.domains if len(self.domains[y]) == 1}
                    for y in inferred_vars:
                        if y not in new_assignment:
                            new_assignment[y] = inferred_vars[y]
                        
                result = self.backtrack(new_assignment)
                if result:
                    return result
                self.domains = orig_domains
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
