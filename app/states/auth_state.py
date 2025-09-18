import reflex as rx


class AuthState(rx.State):
    users: dict[str, str] = {"admin@reflex.com": "password123"}
    in_session: bool = False
    current_user: str = ""

    @rx.event
    def sign_up(self, form_data: dict):
        if form_data["email"] in self.users:
            yield rx.toast.error("Email already in use")
        else:
            self.users[form_data["email"]] = form_data["password"]
            self.in_session = True
            self.current_user = form_data["email"]
            return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        if (
            form_data["email"] in self.users
            and self.users[form_data["email"]] == form_data["password"]
        ):
            self.in_session = True
            self.current_user = form_data["email"]
            return rx.redirect("/")
        else:
            self.in_session = False
            yield rx.toast.error("Invalid email or password")

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.current_user = ""
        return rx.redirect("/")

    def check_session(self):
        pass