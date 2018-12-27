from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
import random
from absl import app
_BOT_FEATURES_VIEW_INDEX = features.SCREEN_FEATURES.player_relative.index

_NO_OP = actions.FUNCTIONS.no_op.id
_MOVE_TO_POSITION_ON_SCREEN = actions.FUNCTIONS.Attack_screen.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id

_AI_NEUTRAL = 3
_SELECT_ALL = [0]
_NOT_QUEUED = [0]

class MyAgent(base_agent.BaseAgent):
	def step(self, obs):
		super(MyAgent, self).step(obs)
		if _MOVE_TO_POSITION_ON_SCREEN not in obs.observation['available_actions']:
			return self.select_bot()
		else:
			return self.select_bot_action(obs)
	def get_beacon_location(self, ai_relative_view):
		return (ai_relative_view == _AI_NEUTRAL).nonzero()

	def move_to_beacon(self, beacon_x, beacon_y):
		beacon_position = [beacon_y.mean(), beacon_x.mean()]
		return actions.FunctionCall(_MOVE_TO_POSITION_ON_SCREEN, [_NOT_QUEUED, beacon_position])


	def do_nothing(self):
		return actions.FunctionCall(_NO_OP, [])


	def select_bot(self):
		return actions.FunctionCall(_SELECT_ARMY, [_SELECT_ALL])


	def select_bot_action(self, obs):
		bot_view = obs.observation['feature_screen'][_BOT_FEATURES_VIEW_INDEX]
		beacon_x, beacon_y = self.get_beacon_location(bot_view)
		if not beacon_y.any():
			return self.do_nothing()
		return self.move_to_beacon(beacon_x, beacon_y)

		