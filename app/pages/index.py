import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.auth_state import AuthState
from app.states.game_state import GameState, Game
from app.components.header import header


def create_game_dialog():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="w-4 h-4 mr-2"),
                "Create Game",
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-semibold transition-colors text-white shadow bg-orange-500 hover:bg-orange-600 h-9 px-4 py-2",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Create a New Game"),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Title", class_name="text-sm font-medium leading-none"),
                    rx.el.input(
                        name="title",
                        required=True,
                        class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm font-medium text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500",
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.el.div(
                    rx.el.label(
                        "Date & Time", class_name="text-sm font-medium leading-none"
                    ),
                    rx.el.input(
                        name="datetime",
                        type="datetime-local",
                        required=True,
                        class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm font-medium text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500",
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.el.div(
                    rx.el.label(
                        "Capacity", class_name="text-sm font-medium leading-none"
                    ),
                    rx.el.input(
                        name="capacity",
                        type="number",
                        required=True,
                        class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm font-medium text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500",
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.dialog.close(
                    rx.el.button(
                        "Create Game",
                        type="submit",
                        class_name="w-full mt-4 inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-semibold transition-colors text-white shadow bg-orange-500 hover:bg-orange-600 h-10 px-4 py-2",
                    )
                ),
                on_submit=GameState.create_game,
                reset_on_submit=True,
                class_name="flex flex-col gap-4 mt-4",
            ),
            style={
                "background_color": "#111827",
                "border_radius": "12px",
                "border": "1px solid #374151",
            },
        ),
    )


def logged_in_view():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Dashboard", class_name="text-3xl font-bold"),
                rx.el.p(
                    f"Welcome back, {AuthState.current_user}!",
                    class_name="text-gray-400",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                create_game_dialog(),
                rx.el.button(
                    "Sign Out",
                    on_click=AuthState.sign_out,
                    class_name="px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors font-semibold",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-start mb-8",
        ),
        rx.el.div(
            rx.el.h2("Nearby Games", class_name="text-2xl font-bold mb-4"),
            rxe.map(
                rxe.map.tile_layer(
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                ),
                rx.foreach(
                    GameState.games,
                    lambda game: rxe.map.marker(
                        rxe.map.popup(
                            rx.el.div(
                                rx.el.h3(game["title"], class_name="font-bold"),
                                rx.el.p(game["datetime"]),
                                rx.el.a(
                                    "View Details",
                                    href=f"/games/{game['id']}",
                                    class_name="text-orange-500",
                                ),
                                class_name="text-black",
                            )
                        ),
                        position=latlng(
                            game["location"]["lat"], game["location"]["lng"]
                        ),
                    ),
                ),
                id="games-map",
                center=latlng(lat=34.0522, lng=-118.2437),
                zoom=10.0,
                height="400px",
                width="100%",
                class_name="rounded-xl border border-gray-700",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.el.h3("View Your Stats", class_name="text-xl font-bold"),
                    rx.el.p(
                        "Check your games played, attendance, and streaks.",
                        class_name="text-gray-400",
                    ),
                    class_name="p-6 bg-gray-800 border border-gray-700 rounded-xl hover:bg-gray-700/50 transition-colors",
                ),
                href="/stats",
            ),
            rx.el.a(
                rx.el.div(
                    rx.el.h3("Find a Game", class_name="text-xl font-bold"),
                    rx.el.p(
                        "Browse and join upcoming pickup games.",
                        class_name="text-gray-400",
                    ),
                    class_name="p-6 bg-gray-800 border border-gray-700 rounded-xl hover:bg-gray-700/50 transition-colors",
                ),
                href="/games",
            ),
            rx.el.a(
                rx.el.div(
                    rx.el.h3("Game History", class_name="text-xl font-bold"),
                    rx.el.p(
                        "Review your past games and results.",
                        class_name="text-gray-400",
                    ),
                    class_name="p-6 bg-gray-800 border border-gray-700 rounded-xl hover:bg-gray-700/50 transition-colors",
                ),
                href="/history",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="font-['Inter'] bg-gray-900 text-white p-8 pt-24 min-h-screen",
    )


def logged_out_view():
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "volleyball", class_name="h-24 w-24 text-orange-500 animate-bounce"
            ),
            rx.el.h1(
                "where amazing happens",
                class_name="text-4xl md:text-6xl font-bold tracking-tighter text-white",
            ),
            rx.el.p(
                "The ultimate platform for pickup basketball.",
                class_name="text-lg text-gray-400",
            ),
            rx.el.a(
                "Let's Hoop",
                href="/sign-in",
                class_name="mt-6 inline-flex items-center justify-center whitespace-nowrap rounded-md text-lg font-semibold transition-colors text-white shadow-lg bg-orange-500 hover:bg-orange-600 h-12 px-8 py-3",
            ),
            class_name="flex flex-col items-center justify-center space-y-4 text-center",
        ),
        class_name="flex-1 flex items-center justify-center",
    )


def index():
    return rx.el.div(
        header(),
        rx.cond(AuthState.in_session, logged_in_view(), logged_out_view()),
        class_name="font-['Inter'] bg-gray-900 flex flex-col min-h-screen",
    )