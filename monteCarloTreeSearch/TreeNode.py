

class TreeNode():
    """
    A class for the nodes, which among other things contains the board state
    """
    def __init__(self, state, parent: "TreeNode") -> None:
        """
        Main condstructor, takes in state and parent node.
        setting all num values as zero. 
        """
        # _ makes the variables private
        self._state = state
        self._is_terminal = state.isTerminal()
        self._is_fully_expanded = self.isTerminal
        self._parent = parent
        self._visits = 0
        self._wins = 0
        self._draws = 0
        self._loses = 0
        self._children = []

    def get_visits(self) -> int:
        """
        Returns numVisits
        """
        return self._visits

    def get_wins(self) -> int:
        """
        Returns numWins
        """
        return self._wins

    def get_draws(self) -> int:
        """
        Returns numDraws
        """
        return self._draws

    def get_loses(self) -> int:
        """
        Returns numLoses
        """
        return self._loses

    def get_parent(self) -> "TreeNode":
        """
        Returns parent
        """
        return self._parent
    
    def is_leaf(self) -> bool:
        """
        Returns True if self is leaf (has no children)
        """
        return bool(len(self._children))
    
    def is_parent(self) -> bool:
        """
        Returns True if self is parent (has children)
        """
        return bool(self._parent)
    
    def get_children(self) -> list:
        """
        Returns list of children
        """
        return self._children
    
    def has_children(self) -> bool:
        """
        Returns True if has children
        """
        return bool(len(self._children))