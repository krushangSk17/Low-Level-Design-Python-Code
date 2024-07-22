class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f"User {self.user_id}: {self.name}"

class TicTacToe:
    def __init__(self, n: int):
        self.size = n
        self.row = [0] * n
        self.col = [0] * n
        self.diag = 0
        self.revdiag = 0

    def move(self, row: int, col: int, player: int) -> int:
        point = 1 if player == 1 else -1
        
        self.row[row] += point
        self.col[col] += point
        
        if row == col:
            self.diag += point
        
        if row + col == self.size - 1:
            self.revdiag += point
        
        if abs(self.row[row]) == self.size or abs(self.col[col]) == self.size or abs(self.diag) == self.size or abs(self.revdiag) == self.size:
            return player
        
        return 0

class Game:
    def __init__(self, n: int, user1: User, user2: User):
        self.tictactoe = TicTacToe(n)
        self.user1 = user1
        self.user2 = user2
        self.current_player = user1  # User1 starts the game
        self.player_map = {user1.user_id: 1, user2.user_id: 2}

    def play_move(self, row: int, col: int):
        player_id = self.player_map[self.current_player.user_id]
        result = self.tictactoe.move(row, col, player_id)
        
        if result == player_id:
            print(f"{self.current_player.name} wins!")
            return result
        elif result == 0:
            self.current_player = self.user1 if self.current_player == self.user2 else self.user2
            print(f"Next turn: {self.current_player.name}")
            return 0

# Example usage:
user1 = User(1, "Alice")
user2 = User(2, "Bob")
game = Game(3, user1, user2)

game.play_move(0, 0)  # Alice
game.play_move(0, 1)  # Bob
game.play_move(1, 1)  # Alice
game.play_move(0, 2)  # Bob
game.play_move(2, 2)  # Alice wins
