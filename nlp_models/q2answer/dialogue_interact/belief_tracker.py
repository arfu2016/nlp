"""
@Project   : CubeGirl
@Module    : belief_tracker.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/23/18 3:34 PM
@Desc      : 
"""

import nltk
import numpy as np

from collections import defaultdict

UPD = 10


class BeliefTracker(Agent):
    """相当于IntentProcessor in intent.py"""
    def _search(self, w_t, s_t):
        # w_t = to_tokens(w)
        return float(sum([ww in s_t for ww in w_t]))/len(w_t)

    def _search_slots(self, s_t):
        matches = {}
        for slot,slot_t in self.state['database'].slot_tokens.iteritems():
            m = self._search(slot_t,s_t)
            if m>0.:
                matches[slot] = m
        return matches

    def _search_values(self, s_t):
        matches = {}
        for slot in self.state['database'].slots:
            matches[slot] = defaultdict(float)
            for ss in s_t:
                if ss in self.movie_dict.tokens[slot]:
                    for vi in self.movie_dict.tokens[slot][ss]:
                        matches[slot][vi] += 1.
            for vi,f in matches[slot].iteritems():
                val = self.movie_dict.dict[slot][vi]
                matches[slot][vi] = f/len(nltk.word_tokenize(val))
        return matches

    ''' update agent state '''
    def _update_state(self, user_utterance, upd=UPD, verbose=False):
        prev_act, prev_slot = self.state['prevact'].split('@')

        s_t = to_tokens(user_utterance)
        slot_match = self._search_slots(s_t) # search slots
        val_match = self._search_values(s_t) # search values

        for slot, values in val_match.items():
            requested = (prev_act=='request') and (prev_slot==slot)
            matched = (slot in slot_match)
            if not values:
                if requested: # asked for value but did not get it
                    self.state['database'].delete_slot(slot)
                    self.state['num_requests'][slot] = 1000
                    self.state['dont_care'].add(slot)
            else:
                for y, match in values.iteritems():
                    # y = self.movie_dict.dict[slot].index(val)
                    if verbose:
                        print('Detected %s' % self.movie_dict.dict[slot][y],
                              ' update = ', match)
                    if matched and requested:
                        alpha = upd*(match + 1. + slot_match[slot])
                    elif matched and not requested:
                        alpha = upd*(match + slot_match[slot])
                    elif not matched and requested:
                        alpha = upd*(match + 1.)
                    else:
                        alpha = upd*match
                    self.state['inform_slots'][slot][y] += alpha
                self.state['slot_tracker'].add(slot)

    def _init_beliefs(self):
        beliefs = {s: np.copy(self.state['database'].priors[s])
                   for s in self.state['database'].slots}
        return beliefs
