import reflex as rx
from app.pages.sign_in import sign_in
from app.pages.sign_up import sign_up
from app.pages.dashboard import dashboard
from app.pages.index import index
from app.pages.stats import stats_page
from app.pages.games import games_page
from app.states.auth_state import AuthState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(sign_in, route="/sign-in")
app.add_page(sign_up, route="/sign-up")
app.add_page(dashboard, route="/dashboard", on_load=[AuthState.check_session])
app.add_page(stats_page, route="/stats", on_load=[AuthState.check_session])
app.add_page(games_page, route="/games", on_load=[AuthState.check_session])