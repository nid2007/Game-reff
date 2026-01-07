import random
from typing import Dict, Any
from game_state import GameState

class GameEngine:
    """
    The Brain of the operation.
    Contains all the rules and logic to execute turns.
    """
    def __init__(self, state: GameState):
        self.state = state

    def validate_move(self, user_move: str) -> Dict[str, Any]:
        """
        Tool 1: Checks if the user's move is allowed.
        """
        move = user_move.lower().strip()
        valid_moves = ["rock", "paper", "scissors", "bomb"]

        # 1. Check basic dictionary
        if move not in valid_moves:
            return {
                "valid": False,
                "message": f"Invalid move '{user_move}'. Valid moves: rock, paper, scissors, bomb.",
                "normalized_move": "invalid"
            }

        # 2. Check Bomb Rule (Once per game)
        if move == "bomb":
            if self.state.bomb_usage["user"]:
                return {
                    "valid": False,
                    "message": "You have already used your Bomb! You cannot use it again.",
                    "normalized_move": "invalid"
                }

        # If we pass all checks
        return {"valid": True, "message": "Move accepted.", "normalized_move": move}

    def resolve_turn(self, user_move: str) -> Dict[str, Any]:
        """
        Tool 2: Executes the turn, updates state, and determines winner.
        """
        # A. Check Game Over status first
        if self.state.game_over:
            return {"status": "Game Over", "final_scores": self.state.scores}

        self.state.increment_round()
        round_num = self.state.round_count

        # B. Handle Invalid Move Penalty
        if user_move == "invalid":
            self.state.log_history("INVALID", "-", "Waste")
            self.state.check_game_over()
            return {
                "outcome": f"Round {round_num} Wasted due to invalid input. No points.",
                "scores": self.state.scores
            }

        # C. Generate Bot Move
        bot_move = self._get_bot_move()

        # D. Update Bomb Usage State
        if user_move == "bomb":
            self.state.mark_bomb_used("user")
        if bot_move == "bomb":
            self.state.mark_bomb_used("bot")

        # E. Determine Winner
        winner = self._determine_winner(user_move, bot_move)
        self.state.update_score(winner)

        # F. Log & Finalize
        self.state.log_history(user_move, bot_move, winner)
        self.state.check_game_over()

        # G. Return Summary for the Agent
        return {
            "round": round_num,
            "user_move": user_move,
            "bot_move": bot_move,
            "winner": winner,
            "scores": self.state.scores,
            "game_over": self.state.game_over
        }

    def _get_bot_move(self) -> str:
        """Helper: logic for bot's move."""
        options = ["rock", "paper", "scissors"]
        # If bot hasn't used bomb, 10% chance to use it
        if not self.state.bomb_usage["bot"]:
            if random.random() < 0.10:
                return "bomb"
        return random.choice(options)

    def _determine_winner(self, user: str, bot: str) -> str:
        """Helper: Pure logic for R-P-S-Bomb rules."""
        if user == bot:
            return "Draw"
        if user == "bomb":
            return "User"
        if bot == "bomb":
            return "Bot"
        
        # Standard RPS
        wins = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        if wins[user] == bot:
            return "User"
        else:
            return "Bot"
