import socket
import pickle
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState, BOT_CONFIG_AGENT_HEADER
from rlbot.parsing.custom_config import ConfigHeader, ConfigObject
from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.rigid_body_struct import RigidBodyTick


class Client(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.ip: str  # Set in bot cfg
        self.port: int  # Set in bot cfg

    def initialize_agent(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def load_config(self, config_header: ConfigHeader) -> None:
        self.ip: str = config_header["ip"].value
        self.port: int = config_header.getint("port")

    def retire(self):
        self.socket.close()

    @staticmethod
    def create_agent_configurations(config: ConfigObject) -> None:
        params: ConfigHeader = config.get_header(BOT_CONFIG_AGENT_HEADER)
        params.add_value("ip", str, default="127.0.0.1", description="The IP address of the host machine")
        params.add_value("port", int, default=5555, description="The port of the host machine that should be used")

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Set game state received from host
        pickled_game_state: bytes = self.socket.recv(8192)
        game_state: GameState = pickle.loads(pickled_game_state)
        self.set_game_state(game_state)

        # Send controls to host
        rb: RigidBodyTick = self.get_rigid_body_tick()
        player_input: PlayerInput = rb.players[not self.index].input

        controller: SimpleControllerState = SimpleControllerState()
        player_input.steer = controller.steer
        player_input.throttle = controller.throttle
        player_input.pitch = controller.pitch
        player_input.yaw = controller.yaw
        player_input.roll = controller.roll
        player_input.jump = controller.jump
        player_input.boost = controller.boost
        player_input.handbrake = controller.handbrake

        pickled_controller: bytes = pickle.dumps(controller, pickle.HIGHEST_PROTOCOL)
        self.socket.sendall(pickled_controller)

        return SimpleControllerState()
