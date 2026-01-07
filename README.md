# AI Game Referee

This is a Rock Paper Scissors game project. It has two parts. One part uses Google AI to manage the game. The other part is untethered and runs offline to test the rules.

## How to Run

You need Python installed on your computer.

### Step 1. Install Requirements
Run this command in your terminal
pip install -r requirements.txt

### Step 2. Setup API Key
Create a file named .env
Put your Google API Key inside it like this
GOOGLE_API_KEY=your_key_here

### Step 3. Play the Game
To play with the AI Referee run this command
python main.py

If you have issues with the API or just want to test the logic run this command
python manual_test.py

## Project Structure
1. main.py is the AI version. It connects to Google Gemini.
2. manual_test.py is the Offline version. It is good for testing logic.
3. game_engine.py has the rules for the game.
4. agent_interface.py handles the connection to Google.
5. game_state.py keeps track of the score.

## Game Rules
There are 3 rounds.
You can choose Rock Paper or Scissors.
You have one special Bomb move per game.
If you type something wrong you lose the turn.
