import reflex as rx
from app.states.auth_state import AuthState
from app.states.game_state import GameState, Game
from app.states.user_state import UserState


def stat_card(icon: str, label: str, value: rx.Var):
    return rx.el.div(
        rx.icon(icon, class_name="w-6 h-6 stroke-orange-500"),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-400"),
            rx.el.p(value, class_name="text-2xl font-bold"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-4 bg-gray-800 border border-gray-700 rounded-lg",
    )


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


def dashboard():
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Pickup Hoops", class_name="text-3xl font-bold"),
                rx.el.p(
                    f"Welcome, {AuthState.current_user}!", class_name="text-gray-400"
                ),
                class_name="flex flex-col",
            ),
            rx.el.button(
                "Sign Out",
                on_click=AuthState.sign_out,
                class_name="px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors font-semibold",
            ),
            class_name="flex justify-between items-start mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Your Stats", class_name="text-2xl font-bold mb-4"),
                rx.el.div(
                    stat_card("swords", "Games Played", UserState.games_played),
                    stat_card(
                        "pie-chart",
                        "Attendance Rate",
                        f"{UserState.attendance_rate.to_string()}%",
                    ),
                    stat_card("flame", "Streak", UserState.streaks),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Available Games", class_name="text-2xl font-bold"),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    rx.foreach(GameState.games, game_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                class_name="w-full",
            ),
        ),
        class_name="font-['Inter'] bg-gray-900 text-white min-h-screen p-8",
    )