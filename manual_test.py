from game_state import GameState
from game_engine import GameEngine

# 1. Setup the Game Logic
state = GameState()
engine = GameEngine(state)

print("--- MANUAL TEST MODE (No AI) ---")
print("Moves: rock, paper, scissors, bomb")

# 2. Simple Loop
while not state.game_over:
    # A. Get Input
    user_input = input(f"\nRound {state.round_count + 1} - Your Move: ")
    if user_input in ["exit", "quit"]:
        break

    # B. Validate
    val_result = engine.validate_move(user_input)
    if not val_result["valid"]:
        # If invalid, punish (waste round)
        print(f"Invalid: {val_result['message']}")
        res = engine.resolve_turn("invalid")
    else:
        # If valid, play turn
        move = val_result["normalized_move"]
        res = engine.resolve_turn(move)

    # C. Print Result (The "Backend" Logic)
    if "outcome" in res:
        # Invalid move result
        print(f"Result: {res['outcome']}")
    else:
        # Valid turn result
        print(f"You: {res['user_move']} | Bot: {res['bot_move']}")
        print(f"Winner: {res['winner']}")
    
    print(f"Score: User {res['scores']['user']} - Bot {res['scores']['bot']}")

# 3. Game Over
print("\n--- GAME OVER ---")
if state.scores['user'] > state.scores['bot']:
    print("USER WINS!")
elif state.scores['bot'] > state.scores['user']:
    print("BOT WINS!")
else:
    print("DRAW!")
