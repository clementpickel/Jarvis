from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from steam import Steam
from open import Open

load_dotenv()

class Gemini:
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client()

    history = []

    def add_history(self, user, text):
        self.history.append({
            "role": user,
            "text": text
        })

    # Define function declaration
    open_steam_game = types.FunctionDeclaration(
        name="steam_client.start_game_from_name",
        description="Open a game in the steam library",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "game_name": types.Schema(
                    type=types.Type.STRING,
                    description="The steam game to start"
                )
            },
            required=["game_name"],
        ),
    )

    open_calc = types.FunctionDeclaration(
        name="open.open_calc",
        description="Open the calculator"
    )

    open_word = types.FunctionDeclaration(
        name="open.open_word",
        description="Open Word"
    )

    open_excel = types.FunctionDeclaration(
        name="open.open_excel",
        description="Open Excel"
    )

    open_powerpoint = types.FunctionDeclaration(
        name="open.open_powerpoint",
        description="Open the powerpoint"
    )

    tools = types.Tool(function_declarations=[open_steam_game, open_calc, open_word, open_excel, open_powerpoint])
    config = types.GenerateContentConfig(tools=[tools])


    def __init__(self, model="gemini-2.5-flash"):
        self.model = model
        self.steam_client = Steam()
        self.open_client = Open()

    def function_call(self, prompt):
        complete_prompt = self.make_prompt(prompt)

        response = self.client.models.generate_content(
            model=self.model,
            contents=complete_prompt,
            config=self.config,
        )

        fc = response.candidates[0].content.parts[0].function_call
        text = response.candidates[0].content.parts[0].text

        self.add_history("user", prompt)
        self.add_history("model", text)

        if text:
            print("Model text response:", text)
        if fc:
            print(f"Function to call: {fc.name}")
            print(f"Arguments: {fc.args}")
            if fc.name == "steam_client.start_game_from_name":
                self.steam_client.start_game_from_name(**fc.args)
            elif fc.name == "open.open_calc":
                self.open_client.open_calc()
            elif fc.name in ["open.open_word", "open_word"]:
                self.open_client.open_word()
            elif fc.name in ["open.open_excel", "open_excel"]:
                self.open_client.open_excel()
            elif fc.name in ["open.open_powerpoint", "open_powerpoint"]:
                self.open_client.open_powerpoint()
        else:
            print("No function call found.")

    def make_prompt(self, prompt):
        games = list(self.steam_client.games.keys())
        new_prompt = f"""Tu es Jarvis, un assistant sur windows qui peut ouvrir des jeux et quelques applications.
Voici les jeux que possède l'utilisateur: {games}
Historique de la conversation: {self.history}
Répond a cette requête:
{prompt}
"""
        return new_prompt

# Example usage
if __name__ == "__main__":
    gemini_client = Gemini()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        gemini_client.function_call(user_input)
