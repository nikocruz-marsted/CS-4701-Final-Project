from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import _pick_unused_card
from pypokerengine.utils.card_utils import _fill_community_card
from pypokerengine.utils.card_utils import gen_cards


def estimate_winrate(num_simulations, hole_cards, community_cards=None):
    community_cards = gen_cards(community_cards)
    hole_cards = gen_cards(hole_cards)

    # do mc simulation
    win_count = sum([montecarlo(hole_cards,
                                community_cards) for x in range(num_simulations)])
    return float(win_count) / num_simulations


def montecarlo(hole_cards, community_cards):
    community_cards = _fill_community_card(
        community_cards, used_card=hole_cards + community_cards)
    unused_cards = _pick_unused_card(
        2, hole_cards + community_cards)
    opponents_hole = [unused_cards[2 * 0:2 * 0 + 2]]
    opponents_score = [HandEvaluator.eval_hand(
        hole, community_cards) for hole in opponents_hole]
    my_score = HandEvaluator.eval_hand(hole_cards, community_cards)
    return 1 if my_score >= max(opponents_score) else 0


class MontecarloBot(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_cards, round_state):
        # Estimate the win rate
        win_rate = estimate_winrate(
            100, hole_cards, round_state['community_card'])

        # Check whether it is possible to call
        can_call = len(
            [item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [
                item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        amount = None

        # If the win rate is large enough, then raise
        if win_rate > 0.5:
            raise_amount_options = [
                item for item in valid_actions if item['action'] == 'raise'][0]['amount']
            if win_rate > 0.75:
                # If our win probabilities are high, we want to bet to get
                # worse hands to call us and potentially fold out better hands
                action = 'raise'
                amount = raise_amount_options['max']
                pot = round_state['pot']
                main_pot = pot['main']
                amount = .75 * float(main_pot['amount'])
            elif win_rate > 0.625:
                # If it is likely to win, but not a super strong holding,
                # raise by a smaller amount
                action = 'raise'
                amount = raise_amount_options['max']
                pot = round_state['pot']
                main_pot = pot['main']
                amount = .5 * float(main_pot['amount'])
            else:
                # If we just have a decent chance to win, purely call
                action = 'call'
        else:
            call_amount = [
                item for item in valid_actions if item['action'] == 'call'][0]['amount']
            if call_amount == 0:
                action = 'call'
            else:
                action = 'fold'

        # Set the amount
        if amount is None:
            items = [item for item in valid_actions if item['action'] == action]
            amount = items[0]['amount']

        return action, amount

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_cards, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return MontecarloBot()
