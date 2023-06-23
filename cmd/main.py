from jam import Jam
from jam.personnel import BasicPersonnel
from jam.instrument import PromptPainter
from jam.persistence.sqlite import SQLitePersistence

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.panel import Panel


def main():
    console = Console()
    color_wheel = ["red", "green", "blue", "yellow", "cyan", "dark_orange"]

    # Welcome message
    panel_text = """
    🍓 Create a Jam Session with AI.\nhttps://github.com/abhishtagatya/jam
    """
    panel = Panel(
        Text(panel_text, justify='center', style='grey100'),
        title=f"[grey100]Jam v{Jam.__version__}",
        subtitle="[grey100]Let's Jam!",
        style='purple'
    )
    console.print(panel)
    console.print()

    jam_room = Jam(
        members=[
            BasicPersonnel.from_json('example/personnel/homer-simpson.json'),
            BasicPersonnel.from_json('example/personnel/walter-white.json')
        ],
        instruments=[
            PromptPainter()
        ],
        # persistence=SQLitePersistence()
    )

    color_map = {x.uid: color_wheel.pop() for x in jam_room.members}
    for member in jam_room.members:
        tc = color_map[member.uid]
        console.print(f"[{tc}]{member.uid}[/{tc}] has entered the room!")

    # Handle user input
    while True:
        user_input = Prompt.ask()
        if str(user_input).lower() == "q":
            user_confirm = Confirm.ask("Leaving the Room? [y/n]")
            if user_confirm:
                break

        # Add user input to the chat history
        messages = jam_room.compose(message=str(user_input), multi=True)

        # Display chat history
        for message in messages:
            tc = color_map[message.author]
            console.print(f"[{tc}]@{message.author}[/{tc}]: {message.content}")

    console.print("You left the room!", style="blue")


if __name__ == "__main__":
    main()
