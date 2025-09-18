import reflex as rx
from app.states.game_state import GameState, Game
from app.components.header import header


def past_game_card(game: Game):
    return rx.el.div(
        rx.el.div(
            rx.el.h3(game["title"], class_name="text-lg font-bold"),
            rx.el.p(
                f"Played on: {game['datetime']}", class_name="text-sm text-gray-400"
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.p(f"Creator: {game['creator']}", class_name="text-sm text-gray-400"),
            class_name="mt-2 pt-2 border-t border-gray-700",
        ),
        class_name="p-4 bg-gray-800 border border-gray-700 rounded-xl",
    )


def history_page():
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.h2("Game History", class_name="text-2xl font-bold mb-6"),
            rx.cond(
                GameState.past_games.length() > 0,
                rx.el.div(
                    rx.foreach(GameState.past_games, past_game_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.el.p(
                        "You haven't played any games yet.", class_name="text-gray-400"
                    ),
                    class_name="text-center py-10",
                ),
            ),
        ),
        class_name="font-['Inter'] bg-gray-900 text-white min-h-screen p-8 pt-24",
    )