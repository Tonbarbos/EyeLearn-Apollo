
import random
import time # Using time for simulation, QTimer will be handled by GUI

class MemoryGameLogic():
    def __init__(self):
        self.game_finished_callbacks = []
        self.game_info_updated_callbacks = []
        self.card_flipped_callbacks = []
        self.card_matched_callbacks = []
        self.card_unmatched_callbacks = []

        self.cards_data = []
        self.flipped_card_ids = []
        self.matched_pairs = 0
        self.errors = 0
        self.score = 0
        self.time_elapsed = 0
        self._timer_running = False
        self._timer_start_time = 0

    def connect_game_finished(self, callback):
        self.game_finished_callbacks.append(callback)

    def connect_game_info_updated(self, callback):
        self.game_info_updated_callbacks.append(callback)

    def connect_card_flipped(self, callback):
        self.card_flipped_callbacks.append(callback)

    def connect_card_matched(self, callback):
        self.card_matched_callbacks.append(callback)

    def connect_card_unmatched(self, callback):
        self.card_unmatched_callbacks.append(callback)

    def _emit_game_finished(self):
        for callback in self.game_finished_callbacks:
            callback(self.score, self.time_elapsed, self.errors)

    def _emit_game_info_updated(self):
        for callback in self.game_info_updated_callbacks:
            callback(self.score, self.errors, self.time_elapsed)

    def _emit_card_flipped(self, card_id, show_icon):
        for callback in self.card_flipped_callbacks:
            callback(card_id, show_icon)

    def _emit_card_matched(self, card1_id, card2_id):
        for callback in self.card_matched_callbacks:
            callback(card1_id, card2_id)

    def _emit_card_unmatched(self, card1_id, card2_id):
        for callback in self.card_unmatched_callbacks:
            callback(card1_id, card2_id)

    def init_game(self):
        self.cards_data = []
        self.flipped_card_ids = []
        self.matched_pairs = 0
        self.errors = 0
        self.score = 0
        self.time_elapsed = 0
        self._timer_running = False
        self._timer_start_time = 0

        icons = [
            "fa5s.apple-alt", "fa5s.carrot", "fa5s.lemon", "fa5s.pepper-hot",
            "fa5s.seedling", "fa5s.egg", "fa5s.cheese", "fa5s.bread-slice"
        ]
        game_icons = random.sample(icons, 8) * 2 # 8 pares para um grid 4x4
        random.shuffle(game_icons)

        for i in range(16): # 4x4 grid
            self.cards_data.append({
                "id": i,
                "icon_name": game_icons.pop(),
                "is_flipped": False,
                "is_matched": False
            })
        self._emit_game_info_updated()
        self._timer_start_time = time.time()
        self._timer_running = True

    def handle_card_click(self, card_id):
        if card_id in self.flipped_card_ids or self.cards_data[card_id]["is_matched"] or len(self.flipped_card_ids) == 2:
            return

        self._flip_card(card_id, show_icon=True)
        self.flipped_card_ids.append(card_id)

        if len(self.flipped_card_ids) == 2:
            # In a real GUI, this would be a QTimer.singleShot. Here, we simulate immediate check for logic testing.
            self._check_match()

    def _flip_card(self, card_id, show_icon):
        self.cards_data[card_id]["is_flipped"] = show_icon
        self._emit_card_flipped(card_id, show_icon)

    def _check_match(self):
        card1_id, card2_id = self.flipped_card_ids
        card1_data = self.cards_data[card1_id]
        card2_data = self.cards_data[card2_id]

        if card1_data["icon_name"] == card2_data["icon_name"]:
            # Match found
            card1_data["is_matched"] = True
            card2_data["is_matched"] = True
            self.matched_pairs += 1
            self.score += 10
            self._emit_card_matched(card1_id, card2_id)
            if self.matched_pairs == len(self.cards_data) / 2:
                self._timer_running = False
                self._emit_game_finished()
        else:
            # No match, flip back
            self.errors += 1
            self._flip_card(card1_id, show_icon=False)
            self._flip_card(card2_id, show_icon=False)
            self._emit_card_unmatched(card1_id, card2_id)

        self.flipped_card_ids = []
        self._emit_game_info_updated()

    def update_timer_tick(self):
        if self._timer_running:
            self.time_elapsed = int(time.time() - self._timer_start_time)
            self._emit_game_info_updated()

    def get_card_icon_name(self, card_id):
        return self.cards_data[card_id]["icon_name"]

    def get_game_state(self):
        return {
            "score": self.score,
            "errors": self.errors,
            "time_elapsed": self.time_elapsed,
            "matched_pairs": self.matched_pairs,
            "total_pairs": len(self.cards_data) / 2
        }

if __name__ == '__main__':
    # Example of how to use the logic class (without GUI)
    game_logic = MemoryGameLogic()

    def on_game_finished(score, time, errors):
        print(f"Game Finished! Score: {score}, Time: {time}s, Errors: {errors}")

    def on_game_info_updated(score, errors, time_elapsed):
        print(f"Score: {score}, Errors: {errors}, Time: {time_elapsed}s")

    def on_card_flipped(card_id, show_icon):
        print(f"Card {card_id} flipped: {show_icon}")

    def on_card_matched(card1_id, card2_id):
        print(f"Cards {card1_id} and {card2_id} matched!")

    def on_card_unmatched(card1_id, card2_id):
        print(f"Cards {card1_id} and {card2_id} unmatched. Flipping back.")

    game_logic.connect_game_finished(on_game_finished)
    game_logic.connect_game_info_updated(on_game_info_updated)
    game_logic.connect_card_flipped(on_card_flipped)
    game_logic.connect_card_matched(on_card_matched)
    game_logic.connect_card_unmatched(on_card_unmatched)

    game_logic.init_game()
    print("Initial game state:", game_logic.get_game_state())

    # Simulate some clicks (this part would be handled by the GUI in the actual app)
    # For testing, we need to manually trigger the timer timeout for time_elapsed to update
    # and simulate card clicks.

    # This example is purely for demonstrating the logic class's methods and signals.
    # Actual testing will be done with unittest and mocks.

