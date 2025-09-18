import reflex as rx
from app.components.sign_up_card import sign_up_card
from app.components.header import header


def sign_up():
    return rx.el.div(
        header(),
        rx.el.div(sign_up_card(), class_name="flex-1 flex items-center justify-center"),
        class_name="font-['Inter'] bg-gray-900 flex flex-col min-h-screen",
    )