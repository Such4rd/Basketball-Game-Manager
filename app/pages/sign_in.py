import reflex as rx
from app.components.sign_in_card import sign_in_card
from app.components.header import header


def sign_in():
    return rx.el.div(
        header(),
        rx.el.div(sign_in_card(), class_name="flex-1 flex items-center justify-center"),
        class_name="font-['Inter'] bg-gray-900 flex flex-col min-h-screen",
    )