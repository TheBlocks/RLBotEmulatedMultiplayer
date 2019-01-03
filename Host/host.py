import socket
import pickle
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState, BOT_CONFIG_AGENT_HEADER
from rlbot.parsing.custom_config import ConfigHeader, ConfigObject
from rlbot.utils.game_state_util import GameState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.bot_input_struct import PlayerInput


class Host(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.ip: str  # Set in bot cfg
        self.port: int  # Set in bot cfg

    def initialize_agent(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(0)
        self.conn: socket.socket
        self.conn, addr = self.socket.accept()
        self.logger.debug(f"Connected to {addr}:{self.port}")

    def load_config(self, config_header: ConfigHeader) -> None:
        self.ip = config_header["ip"].value
        self.port = config_header.getint("port")

    def retire(self):
        self.conn.close()
        self.socket.close()

    @staticmethod
    def create_agent_configurations(config: ConfigObject) -> None:
        params: ConfigHeader = config.get_header(BOT_CONFIG_AGENT_HEADER)
        params.add_value("ip", str, default="127.0.0.1", description="The IP address of the host machine")
        params.add_value("port", int, default=5555, description="The port of the host machine that should be used")

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Send game state to client
        game_state: GameState = GameState.create_from_gametickpacket(packet)
        pickled: bytes = pickle.dumps(game_state, pickle.HIGHEST_PROTOCOL)
        self.conn.sendall(pickled)

        # Set controller state received from client
        pickled_controller: bytes = self.conn.recv(8192)
        controller: SimpleControllerState = pickle.loads(pickled_controller)

        return controller
