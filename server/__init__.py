"""
ButterflyFX Server Package - Peer-to-Peer Substrate Networking
=================================================================

A complete serverless networking system built on ButterflyFX substrates:
- P2P socket networking with consent-based connections
- Fibonacci-based protocols for optimal data flow
- Game server capabilities with real-time state sync
- Closed network support with invitation system
- Substrate state management across distributed nodes

Core Components:
- ButterflyServer: Main P2P server with substrate integration
- FibonacciDiscovery: Intelligent node discovery using spiral patterns
- GameServer: Multiplayer gaming with substrate state synchronization
- NodeDiscovery: Fibonacci-based network topology optimization

Usage:
    from server import create_game_server, create_open_network
    
    # Create game server
    game_server = create_game_server(port=8894)
    await game_server.start()
    
    # Create open network
    network = create_open_network(port=8893)
    network.start()
"""

from .butterfly_server import (
    ButterflyServer,
    NetworkMode,
    ConnectionType,
    ConsentStatus,
    NodeInfo,
    ConnectionRequest,
    SubstrateSync,
    ButterflyProtocol,
    create_game_server,
    create_closed_network,
    create_open_network
)

from .node_discovery import (
    FibonacciDiscovery,
    GameLobbyDiscovery,
    DiscoveryPhase,
    DiscoveryMethod,
    DiscoveryPacket,
    NetworkTopology,
    create_discovery,
    create_game_lobby_discovery
)

from .game_server import (
    ButterflyGameServer,
    GameType,
    PlayerState,
    Player,
    GameWorld,
    GameEvent,
    create_arena_server,
    create_strategy_server,
    create_puzzle_server,
    create_racing_server
)

__version__ = "1.0.0"
__author__ = "ButterflyFX Kernel Team"

# Quick start functions
async def quick_start_game_server(host: str = "localhost", 
                                 port: int = 8894,
                                 game_type: str = "arena") -> ButterflyGameServer:
    """
    Quick start a game server
    
    Args:
        host: Server host address
        port: Server port
        game_type: Type of game ("arena", "strategy", "puzzle", "racing")
    
    Returns:
        Started game server instance
    """
    game_type_map = {
        "arena": GameType.ARENA,
        "strategy": GameType.STRATEGY,
        "puzzle": GameType.PUZZLE,
        "racing": GameType.RACING
    }
    
    gtype = game_type_map.get(game_type, GameType.ARENA)
    
    server = ButterflyGameServer(host=host, port=port, game_type=gtype)
    await server.start()
    
    return server


def quick_start_network(host: str = "localhost",
                       port: int = 8893,
                       network_mode: str = "open") -> ButterflyServer:
    """
    Quick start a network server
    
    Args:
        host: Server host address
        port: Server port
        network_mode: Network mode ("open", "closed", "game")
    
    Returns:
        Started network server instance
    """
    mode_map = {
        "open": NetworkMode.OPEN,
        "closed": NetworkMode.CLOSED,
        "game": NetworkMode.GAME_SERVER
    }
    
    nmode = mode_map.get(network_mode, NetworkMode.OPEN)
    
    if nmode == NetworkMode.GAME_SERVER:
        return create_game_server(host=host, port=port)
    elif nmode == NetworkMode.CLOSED:
        return create_closed_network(host=host, port=port)
    else:
        return create_open_network(host=host, port=port)


__all__ = [
    # Version info
    '__version__',
    '__author__',
    
    # Quick start functions
    'quick_start_game_server',
    'quick_start_network',
    
    # Main server
    'ButterflyServer',
    'NetworkMode',
    'ConnectionType',
    'ConsentStatus',
    'NodeInfo',
    'ConnectionRequest',
    'SubstrateSync',
    'ButterflyProtocol',
    'create_game_server',
    'create_closed_network',
    'create_open_network',
    
    # Node discovery
    'FibonacciDiscovery',
    'GameLobbyDiscovery',
    'DiscoveryPhase',
    'DiscoveryMethod',
    'DiscoveryPacket',
    'NetworkTopology',
    'create_discovery',
    'create_game_lobby_discovery',
    
    # Game server
    'ButterflyGameServer',
    'GameType',
    'PlayerState',
    'Player',
    'GameWorld',
    'GameEvent',
    'create_arena_server',
    'create_strategy_server',
    'create_puzzle_server',
    'create_racing_server'
]
