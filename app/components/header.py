import reflex as rx
from app.states.auth_state import AuthState


def header():
    return rx.el.header(
        rx.el.div(class_name="w-1/3"),
        rx.el.div(
            rx.el.a(
                rx.icon("volleyball", class_name="h-8 w-8 text-orange-500"), href="/"
            ),
            class_name="w-1/3 flex justify-center",
        ),
        rx.el.div(
            rx.cond(
                AuthState.in_session,
                rx.el.div(
                    rx.el.a(
                        rx.image(
                            src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user}",
                            class_name="h-9 w-9 rounded-full border-2 border-transparent hover:border-orange-500 transition-colors",
                        ),
                        href="/dashboard",
                    ),
                    class_name="flex items-center gap-4",
                ),
                rx.el.div(
                    rx.el.a(
                        "Sign In",
                        href="/sign-in",
                        class_name="text-sm font-semibold text-white hover:text-orange-500 transition-colors",
                    ),
                    rx.el.a(
                        "Sign Up",
                        href="/sign-up",
                        class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-semibold transition-colors text-white shadow bg-orange-500 hover:bg-orange-600 h-9 px-4 py-2",
                    ),
                    class_name="flex items-center gap-4",
                ),
            ),
            class_name="w-1/3 flex justify-end",
        ),
        class_name="fixed top-0 left-0 right-0 z-50 flex justify-between items-center px-8 py-2 h-16 bg-gray-900/80 backdrop-blur-sm border-b border-gray-700 text-white",
    )