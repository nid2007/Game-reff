from game_state import GameState
from game_engine import GameEngine
from agent_interface import RefereeAgent

def main():
    print("--- AI Game Referee ---")
    print("Initializing components...")

    # 1. Dependency Injection Chain
    # State -> Engine -> Agent
    state = GameState()
    engine = GameEngine(state)
    
    try:
        agent = RefereeAgent(engine)
    except Exception as e:
        print(f"Startup Error: {e}")
        return
            agent = MockRefereeAgent(engine)
        else:
            print("Critical: Could not load backup agent.")
            return

    # 2. Start the Chat Session
    chat = agent.start_chat()
    print("Ready! Game on. (Type 'exit' to quit)\n")
    print("Game Rules:")
    print("1. This is a best-of-3 format.")
    print("2. Choose Rock, Paper, or Scissors.")
    print("3. You have one BOMB to use per game (beats all).")
    print("4. Invalid moves will waste the round.")

    # 3. Main Event Loop
    while not state.game_over:
        user_input = input(f"\nRound {state.round_count + 1} - Your Move: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Game aborted.")
            break

        try:
            # The Agent handles the thinking and tool calling
            response = chat.send_message(user_input)
            print(f"\nReferee: {response.text}")
        except Exception as e:
            print(f"\nError during turn execution: {e}")
            print("Tip: If it's a quota error, wait 30s and try the move again.")
            # Do not break, allow retry
            continue

    # 4. Final Wrap-up
    if state.game_over:
        print("\n--- FINAL RESULTS ---")
        s = state.scores
        print(f"User: {s['user']} | Bot: {s['bot']}")
        if s['user'] > s['bot']:
            print("USER WINS!")
        elif s['bot'] > s['user']:
            print("BOT WINS!")
        else:
            print("IT'S A DRAW!")

if __name__ == "__main__":
    main()
