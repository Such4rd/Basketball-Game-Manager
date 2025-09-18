import reflex as rx
from app.states.auth_state import AuthState
from app.states.game_state import GameState, Game
from app.components.header import header


def game_card(game: Game):
    is_attendee = game["attendees"].contains(AuthState.current_user)
    is_waitlisted = game["waitlist"].contains(AuthState.current_user)
    return rx.el.div(
        rx.el.div(
            rx.el.h3(game["title"], class_name="text-xl font-bold"),
            rx.el.div(
                rx.icon("calendar", class_name="w-4 h-4 stroke-gray-400"),
                rx.el.p(game["datetime"], class_name="text-sm text-gray-400"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="w-4 h-4 stroke-gray-400"),
                rx.el.p(
                    f"{game['attendees'].length()}/{game['capacity']} spots filled",
                    class_name="text-sm font-medium",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.cond(
                game["waitlist"].length() > 0,
                rx.el.div(
                    rx.icon("user-plus", class_name="w-4 h-4 stroke-gray-400"),
                    rx.el.p(
                        f"{game['waitlist'].length()} on waitlist",
                        class_name="text-sm font-medium text-yellow-400",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(),
            ),
            class_name="flex flex-col gap-2 my-4",
        ),
        rx.el.div(
            rx.cond(
                is_attendee | is_waitlisted,
                rx.el.button(
                    "Leave Game",
                    on_click=lambda: GameState.leave_game(game["id"]),
                    class_name="w-full px-4 py-2 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700 transition-colors",
                ),
                rx.el.button(
                    "Join Game",
                    on_click=lambda: GameState.join_game(game["id"]),
                    class_name="w-full px-4 py-2 rounded-lg bg-orange-500 text-white font-semibold hover:bg-orange-600 transition-colors",
                ),
            ),
            class_name="mt-auto",
        ),
        class_name="flex flex-col p-6 bg-gray-800 border border-gray-700 rounded-xl shadow-lg hover:shadow-orange-500/20 transition-shadow duration-300",
    )


def games_page():
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Available Games", class_name="text-2xl font-bold"),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.el.input(
                    placeholder="Search games by title...",
                    on_change=GameState.set_search_query,
                    class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 md:text-sm font-medium text-white placeholder:text-gray-500 mb-6",
                )
            ),
            rx.el.div(
                rx.foreach(GameState.filtered_games, game_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            class_name="w-full",
        ),
        class_name="font-['Inter'] bg-gray-900 text-white min-h-screen p-8 pt-24",
    )