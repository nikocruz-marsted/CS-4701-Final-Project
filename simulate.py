from pypokerengine.api.game import start_poker, setup_config

from callbot import CallBot
from nit import Nit
from mcbot import MontecarloBot
from randomBot import RandomBot
import numpy as np

if __name__ == '__main__':
    montecarlo_bot = MontecarloBot()
    callbot = CallBot()
    nit = Nit()
    randombot = RandomBot()

    # Contains payout after each
    payouts = []
    p1, p2 = randombot, montecarlo_bot
    for round in range(500):
        config = setup_config(
            max_round=5, initial_stack=100, small_blind_amount=2)
        config.register_player(name="bot1", algorithm=p1)
        config.register_player(name="bot2", algorithm=p2)
        game_result = start_poker(config, verbose=0)
        payouts.append([player['stack'] for player in game_result['players']
                        if player['uuid'] == montecarlo_bot.uuid])
        print('Avg. Winnings:', '%d' % (int(np.mean(payouts))))
