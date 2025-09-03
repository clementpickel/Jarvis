from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from steam import Steam
from open import Open
from model import Function

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

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model
        self.steam_client = Steam()
        self.open_client = Open()
        self.functions: list[Function] = [
            Function(
                to_execute = self.steam_client.start_game_from_name,
                recognized_names = ["steam_client.start_game_from_name", "start_game_from_name"],
                gemini= types.FunctionDeclaration(
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
            ),
            Function(
                to_execute= self.open_client.open_brave,
                recognized_names= ["open.open_brave", "open_brave"],
                gemini= types.FunctionDeclaration(
                    name="open.open_brave",
                    description="Open a web browser",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "url": types.Schema(
                                type=types.Type.STRING,
                                description="The url to open, google.com by default"
                            )
                        },
                    ),
                )
            ),
            Function(
                to_execute= self.open_client.open_file,
                recognized_names= ["open.open_file", "open_file"],
                gemini= types.FunctionDeclaration(
                    name="open_file",
                    description="Open a file",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "path": types.Schema(
                                type=types.Type.STRING,
                                description="Path to the file"
                            )
                        },
                    ),
                )
            ),
            Function(
                to_execute= self.open_client.open_calc,
                recognized_names= ["open.open_calc", "open_calc"],
                gemini= types.FunctionDeclaration(
                    name="open.open_calc",
                    description="Open the calculator"
                )
            ),
            Function(
                to_execute= self.open_client.open_word,
                recognized_names= ["open.open_word", "open_word"],
                gemini= types.FunctionDeclaration(
                    name="open.open_word",
                    description="Open Word"
                )
            ),
            Function(
                to_execute= self.open_client.open_excel,
                recognized_names= ["open.open_excel", "open_excel"],
                gemini= types.FunctionDeclaration(
                    name="open.open_excel",
                    description="Open Excel"
                )
            ),
            Function(
                to_execute= self.open_client.open_powerpoint,
                recognized_names= ["open.open_powerpoint", "open_powerpoint"],
                gemini= types.FunctionDeclaration(
                    name="open.open_powerpoint",
                    description="Open the powerpoint"
                )
            ),
        ]

        self.tools = types.Tool(function_declarations=[fct.gemini for fct in self.functions])
        self.config = types.GenerateContentConfig(tools=[self.tools])

    def function_call(self, prompt):
        complete_prompt = self.make_prompt(prompt)

        response = self.client.models.generate_content(
            model=self.model,
            contents=complete_prompt,
            config=self.config,
        )

        self.add_history("user", prompt)

        for parts in response.candidates[0].content.parts:
            fc = parts.function_call
            text = parts.text    

            if text:
                self.add_history("model", text)
                print("Model text response:", text)
            if fc:
                print(f"Function to call: {fc.name}")
                print(f"Arguments: {fc.args}")
                for fct in self.functions:
                    if fc.name in fct.recognized_names:
                        fct.to_execute(**fc.args)
            else:
                print("No function call found.")

    def make_prompt(self, prompt):
        games = list(self.steam_client.games.keys())
        new_prompt = fr"""Tu es Jarvis, un assistant sur windows qui peut ouvrir des jeux et quelques applications.
Voici les jeux que possède l'utilisateur: {games}
L'utilisateur utilise ces sites:
immich.clementpickel.fr pour stocker des photos
webmin.clementpickel.fr pour administrer son serveur
amp.clementpickel.fr pour lancer des serveurs de jeux

La plupart des fichiers sont dans C:\Users\cpick
Les repo github sont dans C:\Users\cpick\Documents\GitHub

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
