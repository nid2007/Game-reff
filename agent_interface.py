import os
import google.generativeai as genai
from dotenv import load_dotenv
from game_engine import GameEngine

# Load environment variables from .env file
load_dotenv()

class RefereeAgent:
    """
    The Interface layer between the Game Engine and Google's AI.
    Handles configuration and chat session management.
    """
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.model = self._configure_model()

    def _configure_model(self):
        """Sets up the Gemini model with tools and instructions."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not found!")

        genai.configure(api_key=api_key)

        # Register the tools
        tools = [self.engine.validate_move, self.engine.resolve_turn]

        system_instruction = """
        You are a Game Referee for Rock-Paper-Scissors-Plus. 
        Your job is to manage the game using the tools.
        
        PROTOCOL:
        1. Get user move.
        2. ALWAYS call `validate_move` first.
        3. If valid, call `resolve_turn(normalized_move)`.
        4. If not valid, call `resolve_turn("invalid")`. this wastes the round.
        5. Tell the user what happened based on the tool result.
        6. Do not calculate scores yourself.
        
        COMMUNICATION RULES:
        - If asked about rules, explain them in 4 to 5 lines maximum.
        - Be simple and clear.
        """

        return genai.GenerativeModel(
            model_name='gemini-2.0-flash-lite-preview-02-05',
            tools=tools,
            system_instruction=system_instruction
        )

    def start_chat(self):
        """Starts and returns a chat session."""
        return self.model.start_chat(enable_automatic_function_calling=True)
