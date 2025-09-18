import reflex as rx
from app.states.game_state import GameState, ChatMessage
from app.states.auth_state import AuthState
from app.components.header import header


def chat_message_bubble(message: ChatMessage):
    is_self = message["user"] == AuthState.current_user
    return rx.el.div(
        rx.el.div(
            rx.el.p(message["user"], class_name="text-xs font-bold"),
            rx.el.p(message["message"], class_name="text-sm"),
            class_name=rx.cond(
                is_self,
                "bg-orange-500 text-white rounded-l-lg rounded-br-lg p-2",
                "bg-gray-700 text-white rounded-r-lg rounded-bl-lg p-2",
            ),
        ),
        class_name=rx.cond(
            is_self, "flex justify-end w-full", "flex justify-start w-full"
        ),
    )


def game_detail_page():
    return rx.el.main(
        header(),
        rx.el.div(
            rx.cond(
                GameState.current_game,
                rx.el.div(
                    rx.el.div(
                        rx.el.a(
                            rx.icon("arrow-left", class_name="w-5 h-5"),
                            "Back to Games",
                            href="/games",
                            class_name="flex items-center gap-2 text-sm font-semibold text-gray-400 hover:text-orange-500 transition-colors mb-4",
                        ),
                        rx.el.h2(
                            GameState.current_game["title"],
                            class_name="text-3xl font-bold",
                        ),
                        rx.el.p(
                            GameState.current_game["datetime"],
                            class_name="text-gray-400",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Game Details", class_name="text-xl font-bold mb-4"
                            ),
                            rx.el.button(
                                rx.icon("share-2", class_name="w-4 h-4 mr-2"),
                                "Share Game",
                                on_click=GameState.share_game_link,
                                class_name="flex items-center px-3 py-1.5 text-sm rounded-md bg-gray-700 hover:bg-gray-600 font-semibold transition-colors",
                            ),
                            rx.el.div(
                                rx.cond(
                                    GameState.current_game["attendees"].contains(
                                        AuthState.current_user
                                    )
                                    | GameState.current_game["waitlist"].contains(
                                        AuthState.current_user
                                    ),
                                    rx.el.button(
                                        "Leave Game",
                                        on_click=lambda: GameState.leave_game(
                                            GameState.current_game["id"]
                                        ),
                                        class_name="w-full px-4 py-2 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700 transition-colors",
                                    ),
                                    rx.el.button(
                                        "Join Game",
                                        on_click=lambda: GameState.join_game(
                                            GameState.current_game["id"]
                                        ),
                                        class_name="w-full px-4 py-2 rounded-lg bg-orange-500 text-white font-semibold hover:bg-orange-600 transition-colors",
                                    ),
                                ),
                                class_name="mt-4",
                            ),
                            class_name="p-6 bg-gray-800 border border-gray-700 rounded-xl",
                        ),
                        rx.el.div(
                            rx.el.h3("Live Chat", class_name="text-xl font-bold mb-4"),
                            rx.el.div(
                                rx.foreach(
                                    GameState.current_game["chat_messages"],
                                    chat_message_bubble,
                                ),
                                class_name="flex flex-col gap-3 p-4 h-80 overflow-y-auto bg-gray-900 rounded-lg border border-gray-700 mb-4",
                            ),
                            rx.el.form(
                                rx.el.input(
                                    placeholder="Type a message...",
                                    name="message",
                                    class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm font-medium text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500",
                                    default_value="",
                                ),
                                rx.el.button(
                                    rx.icon("send", class_name="w-5 h-5"),
                                    type="submit",
                                    class_name="inline-flex items-center justify-center rounded-md bg-orange-500 hover:bg-orange-600 h-10 w-10",
                                ),
                                on_submit=GameState.send_message,
                                reset_on_submit=True,
                                class_name="flex items-center gap-2",
                            ),
                            class_name="p-6 bg-gray-800 border border-gray-700 rounded-xl",
                        ),
                        class_name="grid md:grid-cols-2 gap-6",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Game not found or still loading..."),
                    class_name="flex items-center justify-center h-full",
                ),
            ),
            class_name="w-full",
        ),
        class_name="font-['Inter'] bg-gray-900 text-white min-h-screen p-8 pt-24",
    )