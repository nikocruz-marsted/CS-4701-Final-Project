from pypokerengine.players import BasePokerPlayer
import numpy as np
import random


class RandomBot(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        fold = [item for item in valid_actions if item['action'] in ['fold']]
        call = [item for item in valid_actions if item['action'] in ['fold']]
        raise_amount_options = [
            item for item in valid_actions if item['action'] == 'raise'][0]['amount']
        randomRaise = random.randint(
            raise_amount_options['min'], raise_amount_options['max'])
        randomNum = random.randint(0, 2)
        if randomNum == 0:
            return list(np.random.choice(fold).values())
        if randomNum == 1:
            return list(np.random.choice(call).values())
        if randomNum == 2:
            return 'raise', randomRaise

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return RandomBot()
