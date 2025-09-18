import reflex as rx
from app.states.auth_state import AuthState
from app.components.header import header


def dashboard():
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Dashboard", class_name="text-3xl font-bold"),
                    rx.el.p(
                        f"Welcome back, {AuthState.current_user}!",
                        class_name="text-gray-400",
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
        ),
        class_name="font-['Inter'] bg-gray-900 text-white min-h-screen p-8 pt-24",
    )