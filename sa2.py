from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
import random
from absl import app
from ZergAgent_1 import ZergAgent as player1
from ZergAgent_10 import ZergAgent as player2
import threading
def main(unused_argv):
	agent = player1()
	agent2 = player2()
	try:
		while True:
			with sc2_env.SC2Env(
					map_name="AbyssalReef",
					players=[sc2_env.Agent(sc2_env.Race.zerg),
							 sc2_env.Agent(sc2_env.Race.zerg)],
					agent_interface_format=features.AgentInterfaceFormat(feature_dimensions=features.Dimensions(screen=128, minimap=64),
					use_feature_units=True),
					step_mul=1, 
					game_steps_per_episode=0,
					visualize=True,address=('',15000)) as env:
				print("hahaha")
				server_thread = threading.Thread(target=env._serv.serve_forever)
				server_thread.start()
				print("hahaha2")
				agent.setup(env.observation_spec(), env.action_spec())
				agent2.setup(env.observation_spec(), env.action_spec())
				timesteps = env.reset()
				agent.reset()
				agent2.reset()
				while True:
					step_actions = [agent.step(timesteps[0]),agent2.step(timesteps[1])]
					if timesteps[0].last():
						break
					timesteps = env.step(step_actions)
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	app.run(main)