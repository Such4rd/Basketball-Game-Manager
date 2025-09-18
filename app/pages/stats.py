import reflex as rx
from app.states.user_state import UserState
from app.components.header import header


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


def stats_page():
    return rx.el.main(
        header(),
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
        class_name="font-['Inter'] bg-gray-900 text-white min-h-screen p-8 pt-24",
    )