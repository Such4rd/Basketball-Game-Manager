import reflex as rx


class UserState(rx.State):
    games_played: int = 0
    attendance_rate: float = 100.0
    streaks: int = 0

    def _update_stats_on_join(self):
        self.games_played += 1
        self.streaks += 1

    def _update_stats_on_leave(self):
        if self.games_played > 0:
            self.games_played -= 1
        self.streaks = 0