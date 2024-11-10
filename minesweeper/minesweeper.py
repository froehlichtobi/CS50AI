import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)
        print("empty board: ", self.board)
        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        print("filled board: ", self.board)

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # More generally, any time the number of cells is equal to the count, we know that all of that sentence’s cells must be mines.
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if not self.count:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3)
        # example sentence: Sentence({(1, 1), (1, 2), (1, 3)}, 1)
        # Sentence takes a set of cells and the count
        # need to get the adjacent cells
        adjacent_cells = set()
        # copied from nearby_mines
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # add cell if it is on the board
                if 0 <= i < self.height and 0 <= j < self.width:
                    # only include it if it's not yet known to be safe or a mine
                    # "Be sure to only include cells whose state is still undetermined in the sentence."
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        adjacent_cells.add((i, j))
                    elif (i, j) in self.mines:
                        count -= 1
        print("adjacent cells: ", adjacent_cells)
        if adjacent_cells:
            self.knowledge.append(Sentence(adjacent_cells, count))
        #!!!!!! before i had a explicit function get_adjacent_cells, in which i also changed the
        # count --> but that did not change the count when doing self.knowledge.append(...,count)
        # that's why it did not work all the time

        # 4)
        new_info = True
        while new_info:
            new_info = False

            for sentence in self.knowledge:
                known_safes = sentence.known_safes()
                if known_safes:
                    for s in known_safes.copy():
                        self.mark_safe(s)
                        new_info = True
                known_mines = sentence.known_mines()
                if known_mines:
                    for m in known_mines.copy():
                        self.mark_mine(m)
                        new_info = True

            # 5)More generally, any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2,
            # then we can construct the new sentence set2 - set1 = count2 - count1.
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 != s2 and s2.cells.issubset(s1.cells) and s2.cells:
                        new_cells = s1.cells - s2.cells
                        new_count = s1.count - s2.count
                        new_sentence = Sentence(new_cells, new_count)
                        if new_count >= 0 and new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            new_info = True
            # remove empty sentences:
            new_sentences = []
            for sentence in self.knowledge:
                if sentence.cells:
                    new_sentences.append(sentence)
            self.knowledge = new_sentences

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        available_moves = self.safes - self.moves_made
        if available_moves:
            print("available moves: ", available_moves)
            return random.choice(tuple(available_moves))
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()

        # not optimal to loop over all cells
        for i in range(self.height):
            for j in range(self.width):
                possible_moves.add((i, j))

        possible_moves = possible_moves - self.moves_made - self.mines

        if possible_moves:
            return random.choice(tuple(possible_moves))
        return None
