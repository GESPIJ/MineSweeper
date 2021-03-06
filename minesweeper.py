import itertools
import random


class Minesweeper():
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

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

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
        try:
            i, j = cell
            return self.board[i][j]
        except:
            print(f"EL ERROR ESTA ENNNNNNNNNNNNNNNNNNN {(i,j)}")
        

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
        return self.mines == self.mines_found


class Sentence():
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
        print("Known mines function")
        known_mines=set()
        return self.cells if len(self.cells)==count else known_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        print("Known safes function")
        known_safes=set()
        return self.cells if len(self.cells)==count else known_safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.cells.remove(cell)
            self.count=self.count-1
        return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        

class MinesweeperAI():
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
        #juego=Minesweeper()
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
        self.moves_made.add(cell)
        encontrada=False

        if len(self.knowledge)>0:
            self.mark_safe(cell)
        vecinos=set()
        
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if i>=0 and j>=0 and i<8 and j<8 and (i,j)!=cell:
                    vecinos.add((i,j))
        vecinos.difference_update(self.moves_made)
        vecinos.difference_update(self.safes)
        vecinosMinas=vecinos.difference(self.mines)
        count=count-(len(vecinos)-len(vecinosMinas))
        vecinos.difference_update(self.mines)
        newSentence=Sentence(vecinos,count)

        for index,oracion in enumerate(self.knowledge):
                copia=oracion.cells.copy()
                if(len(oracion.cells)==0):
                    self.knowledge.remove(oracion)
                elif(len(oracion.cells)==oracion.count):
                    for element in copia:
                        self.mark_mine(element)
                elif(oracion.count==0):
                    for element in copia:
                        self.mark_safe(element)
           
        if (newSentence.count==0):
             for celda in newSentence.cells:
                self.mark_safe(celda)
        elif (newSentence.count==len(newSentence.cells)):
            for celda in newSentence.cells:
                self.mark_mine(celda)
        else: 
            diferencias=[]
            for index,sentence in enumerate(self.knowledge):
                if (newSentence.cells.issubset(sentence.cells) or sentence.cells.issubset(newSentence.cells)):
                    difference=newSentence.cells.symmetric_difference(sentence.cells)
                    interseccion=sentence.cells.intersection(newSentence.cells)
                    if (len(difference)>0 and len(difference)==abs(count-sentence.count)):
                        for element in difference:
                            self.mark_mine(element)
                            newSentence.mark_mine(element)
                    elif(len(difference)>0 and count-sentence.count==0):
                        for element in difference:
                            self.mark_safe(element)
                            newSentence.mark_safe(element)
                    elif(len(difference)>0):
                        appendSentence=Sentence(difference,abs(count-sentence.count))
                        diferencias.append(appendSentence)
            self.knowledge.append(newSentence)
            for diferencia in diferencias:
                self.knowledge.append(diferencia)
        return None   

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        seguro=self.safes.difference(self.moves_made)
        seguro.difference_update(self.mines)
        if (len(seguro)>0):
            variable=seguro.pop()
        else:
            set1=set()
            for i in range(self.width):
                for j in range(self.height):
                    set1.add((i,j))
            set1.difference_update(self.moves_made)
            set1.difference_update(self.mines)
            lista=list(set1)
            random.shuffle(lista)
            if len(lista)>0:
                variable=lista.pop()
            else:
                variable=(0,0)
        return variable
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("Beggining making random move")
        set1=set()
        for i in range(self.width):
            for j in range(self.height):
                set1.add((i,j))
        set1.difference_update(self.moves_made)
        set1.difference_update(self.mines)
        lista=list(set1)
        random.shuffle(lista)
        variable=lista[0]
        print("Ending making random move")
        return variable
        
        raise NotImplementedError
