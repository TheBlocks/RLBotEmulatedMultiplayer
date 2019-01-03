# RLBotEmulatedMultiplayer
A set of bots for emulating multiplayer for RLBot.

Note: This only works for 1v1s.

## Instructions
If you are using this over the internet, the host must port forward the port they are using for RLBotEmulatedMultiplayer. This is not an issue if you are using this over a local network.

### Instructions
1. Get the files required to run bot matches. These files are available in the [RLBotPythonExample](https://github.com/RLBot/RLBotPythonExample) repository. You can drag the contents of the entire RLBotPythonExample repository to the root folder of this repository, if you wish.
1. Depending on if you are the host or client, add `Host/host.cfg` or `Client/client.cfg` (found in this repository) as a participant config in rlbot.cfg (either with the GUI or by editing the file directly).
    - Make sure that the participant index the host is using for `Host/host.cfg` is not the same as the participant index the client is using for `Client/client.cfg`.
    - E.g. If the host is using `participant_config_0` for `Host/host.cfg`, the client must use `participant_config_1` for `Client/client.cfg`.
1. Add your bot cfg as a participant config in rlbot.cfg. Alternatively, you can add a human player.
1. Run the match with `run.bat` or `run-gui.bat`.
1. Pause the game (with the escape key) until the client has connected to the host.
1. Unpause to let the match start.

### Quick explanation of how it works
Every frame, the game state in the host's game is sent to the client. The client then sets the game state it received. Then, the client sends the controls it made to the host, which runs those controls.