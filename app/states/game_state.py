import reflex as rx
from typing import TypedDict, Optional
import datetime
from reflex_enterprise.components.map.types import latlng, LatLng


class ChatMessage(TypedDict):
    user: str
    message: str
    timestamp: str


class Game(TypedDict):
    id: int
    title: str
    datetime: str
    capacity: int
    location: LatLng
    creator: str
    attendees: list[str]
    waitlist: list[str]
    chat_messages: list[ChatMessage]


class GameState(rx.State):
    games: list[Game] = [
        {
            "id": 1,
            "title": "Morning Hoops",
            "datetime": "2024-07-26T08:00",
            "capacity": 10,
            "location": latlng(lat=34.0522, lng=-118.2437),
            "creator": "admin@reflex.com",
            "attendees": ["admin@reflex.com"],
            "waitlist": [],
            "chat_messages": [],
        },
        {
            "id": 2,
            "title": "Evening Game",
            "datetime": "2024-07-26T18:00",
            "capacity": 12,
            "location": latlng(lat=34.055, lng=-118.25),
            "creator": "user2@example.com",
            "attendees": [],
            "waitlist": [],
            "chat_messages": [],
        },
    ]
    search_query: str = ""
    current_game: Optional[Game] = None
    chat_input: str = ""

    @rx.var
    def filtered_games(self) -> list[Game]:
        if not self.search_query:
            return self.games
        return [
            game
            for game in self.games
            if self.search_query.lower() in game["title"].lower()
        ]

    @rx.event
    async def create_game(self, form_data: dict):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        new_game = Game(
            id=len(self.games) + 1,
            title=form_data["title"],
            datetime=form_data["datetime"],
            capacity=int(form_data["capacity"]),
            location=latlng(lat=34.0522, lng=-118.2437),
            creator=auth_state.current_user,
            attendees=[auth_state.current_user],
            waitlist=[],
            chat_messages=[],
        )
        self.games.append(new_game)
        yield rx.toast.success("Game created successfully!")

    def _find_game(self, game_id: int) -> Optional[Game]:
        for game in self.games:
            if game["id"] == game_id:
                return game
        return None

    @rx.event
    def load_game(self):
        game_id = self.router.page.params.get("game_id", "")
        if game_id.isdigit():
            game = self._find_game(int(game_id))
            self.current_game = game
            if not game:
                return rx.redirect("/games")
        else:
            return rx.redirect("/games")

    @rx.event
    async def send_message(self, form_data: dict):
        from app.states.auth_state import AuthState

        message = form_data.get("message", "").strip()
        if not message or not self.current_game:
            return
        auth_state = await self.get_state(AuthState)
        new_message = ChatMessage(
            user=auth_state.current_user,
            message=message,
            timestamp=datetime.datetime.now().isoformat(),
        )
        game_id = self.current_game["id"]
        for i, game in enumerate(self.games):
            if game["id"] == game_id:
                self.games[i]["chat_messages"].append(new_message)
                self.current_game = self.games[i]
                break

    @rx.event
    def share_game_link(self):
        url = f"{self.router.page.origin}{self.router.page.full_raw_path}"
        yield rx.set_clipboard(url)
        yield rx.toast.success("Game link copied to clipboard!")

    @rx.event
    def redirect_to_google_maps(self):
        if self.current_game:
            lat = self.current_game["location"]["lat"]
            lng = self.current_game["location"]["lng"]
            url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
            return rx.redirect(url, external=True)

    @rx.var
    async def past_games(self) -> list[Game]:
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        user = auth_state.current_user
        now = datetime.datetime.now()
        past_games_list = []
        for game in self.games:
            game_time = datetime.datetime.fromisoformat(game["datetime"])
            if game_time < now and user in game["attendees"]:
                past_games_list.append(game)
        return past_games_list

    @rx.event
    async def join_game(self, game_id: int):
        from app.states.auth_state import AuthState
        from app.states.user_state import UserState

        game = self._find_game(game_id)
        auth_state = await self.get_state(AuthState)
        user_state = await self.get_state(UserState)
        user = auth_state.current_user
        if game and user:
            if user in game["attendees"] or user in game["waitlist"]:
                yield rx.toast.info("You are already in this game or on the waitlist.")
                return
            if len(game["attendees"]) < game["capacity"]:
                game["attendees"].append(user)
                user_state._update_stats_on_join()
                yield rx.toast.success("Successfully joined the game!")
            else:
                game["waitlist"].append(user)
                yield rx.toast.info("Game is full. You've been added to the waitlist.")

    @rx.event
    async def leave_game(self, game_id: int):
        from app.states.auth_state import AuthState
        from app.states.user_state import UserState

        game = self._find_game(game_id)
        auth_state = await self.get_state(AuthState)
        user_state = await self.get_state(UserState)
        user = auth_state.current_user
        if game and user:
            if user in game["attendees"]:
                game["attendees"].remove(user)
                user_state._update_stats_on_leave()
                if game["waitlist"]:
                    promoted_user = game["waitlist"].pop(0)
                    game["attendees"].append(promoted_user)
                yield rx.toast.success("You have left the game.")
            elif user in game["waitlist"]:
                game["waitlist"].remove(user)
                yield rx.toast.success("You have been removed from the waitlist.")