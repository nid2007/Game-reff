from typing import TypedDict, List, Dict

class RoundResult(TypedDict):
    """Defines the structure of a single round's history."""
    round_num: int
    user_move: str
    bot_move: str
    winner: str

class GameState:
    """
    Holds the entire state of the game.
    Acts as the 'Database' in memory.
    """
    def __init__(self):
        self.round_count: int = 0
        self.scores: Dict[str, int] = {"user": 0, "bot": 0}
        self.bomb_usage: Dict[str, bool] = {"user": False, "bot": False}
        self.history: List[RoundResult] = []
        self.game_over: bool = False

    def increment_round(self):
        """Increases the round counter."""
        self.round_count += 1

    def update_score(self, winner: str):
        """Updates score based on the winner."""
        if winner == "User":
            self.scores["user"] += 1
        elif winner == "Bot":
            self.scores["bot"] += 1

    def mark_bomb_used(self, player: str):
        """Marks the bomb as used for a specific player ('user' or 'bot')."""
        if player in self.bomb_usage:
            self.bomb_usage[player] = True

    def log_history(self, user_move: str, bot_move: str, winner: str):
        """Adds the round result to history."""
        record: RoundResult = {
            "round_num": self.round_count,
            "user_move": user_move,
            "bot_move": bot_move,
            "winner": winner
        }
        self.history.append(record)

    def check_game_over(self):
        """Checks if the game should end (Best of 3)."""
        if self.round_count >= 3:
            self.game_over = True

    def to_dict(self):
        """Returns the state as a dictionary (useful for debugging)."""
        return {
            "round_count": self.round_count,
            "scores": self.scores,
            "bomb_usage": self.bomb_usage,
            "game_over": self.game_over
        }
