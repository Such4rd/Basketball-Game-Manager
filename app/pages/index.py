import reflex as rx
from app.components.header import header


def index():
    return rx.el.div(
        header(),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "volleyball", class_name="h-24 w-24 text-orange-500 animate-bounce"
                ),
                rx.el.h1(
                    "where amazing happens",
                    class_name="text-3xl font-bold tracking-tighter text-white sm:text-4xl md:text-5xl lg:text-6xl/none",
                ),
                class_name="flex flex-col items-center justify-center space-y-4 text-center",
            ),
            class_name="flex-1 flex items-center justify-center",
        ),
        class_name="font-['Inter'] bg-gray-900 flex flex-col min-h-screen",
    )