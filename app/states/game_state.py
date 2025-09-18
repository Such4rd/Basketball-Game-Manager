import reflex as rx
from typing import TypedDict


class Game(TypedDict):
    id: int
    title: str
    datetime: str
    capacity: int
    location: tuple[float, float]
    creator: str
    attendees: list[str]
    waitlist: list[str]


class GameState(rx.State):
    games: list[Game] = [
        {
            "id": 1,
            "title": "Morning Hoops",
            "datetime": "2024-07-26T08:00",
            "capacity": 10,
            "location": (34.0522, -118.2437),
            "creator": "admin@reflex.com",
            "attendees": ["admin@reflex.com"],
            "waitlist": [],
        },
        {
            "id": 2,
            "title": "Evening Game",
            "datetime": "2024-07-26T18:00",
            "capacity": 12,
            "location": (34.055, -118.25),
            "creator": "user2@example.com",
            "attendees": [],
            "waitlist": [],
        },
    ]
    search_query: str = ""

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
            location=(34.0522, -118.2437),
            creator=auth_state.current_user,
            attendees=[auth_state.current_user],
            waitlist=[],
        )
        self.games.append(new_game)
        yield rx.toast.success("Game created successfully!")

    def _find_game(self, game_id: int) -> Game | None:
        for game in self.games:
            if game["id"] == game_id:
                return game
        return None

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