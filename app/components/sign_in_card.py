import reflex as rx
from app.states.auth_state import AuthState


def sign_in_card():
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Sign in to your account",
                class_name="font-semibold tracking-tight text-xl text-white",
            ),
            rx.el.p(
                "Enter your email below to sign in to your account",
                class_name="text-sm text-gray-400 font-medium",
            ),
            class_name="flex flex-col text-center",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email", class_name="text-sm font-medium leading-none text-gray-300"
                ),
                rx.el.input(
                    type="email",
                    placeholder="user@example.com",
                    id="email",
                    name="email",
                    required=True,
                    class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 md:text-sm font-medium text-white placeholder:text-gray-500",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="text-sm font-medium leading-none text-gray-300",
                ),
                rx.el.input(
                    type="password",
                    id="password",
                    name="password",
                    required=True,
                    class_name="flex h-10 w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 md:text-sm font-medium text-white placeholder:text-gray-500",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.button(
                "Sign in",
                type="submit",
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-semibold transition-colors text-white shadow bg-orange-500 hover:bg-orange-600 h-10 px-4 py-2 w-full",
            ),
            rx.el.div(
                rx.el.span(
                    "Don't have an account?",
                    class_name="text-sm text-gray-400 font-medium",
                ),
                rx.el.a(
                    "Sign up",
                    href="/sign-up",
                    class_name="text-sm text-orange-500 font-medium underline hover:text-orange-400 transition-colors",
                ),
                class_name="flex flex-row gap-2 justify-center",
            ),
            class_name="flex flex-col gap-4",
            on_submit=AuthState.sign_in,
        ),
        class_name="font-bold p-8 rounded-xl bg-gray-900/80 backdrop-blur-sm flex flex-col gap-6 shadow-lg border border-gray-700 text-white min-w-[27rem]",
    )