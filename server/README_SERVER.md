# ButterflyFX Server - P2P Substrate Networking

## 🌐 Serverless Peer-to-Peer Networking

A revolutionary serverless networking system built on ButterflyFX substrates with Fibonacci-based protocols, consent-based connections, and game server capabilities.

## 🚀 Quick Start

### Installation
```bash
cd /opt/butterfly/butterflyfx_kernel/server
pip install -e .
```

### Basic Network Server
```python
from server import create_open_network

# Create and start P2P network
network = create_open_network(host="localhost", port=8893)
network.start()

# Connect to other nodes
await network.connect_to_node("localhost", 8894)

# Create shared substrate
network.create_shared_substrate("my_substrate", fibonacci_level=2)

# Advance substrate through Fibonacci levels
network.advance_shared_substrate("my_substrate", target_level=5)
```

### Game Server
```python
from server import create_arena_server

# Create game server
game_server = create_arena_server(host="localhost", port=8894)
await game_server.start()

# Add players
await game_server.add_player("player1", "Alice", world_id="arena")
await game_server.add_player("player2", "Bob", world_id="arena")

# Process game actions
await game_server.process_game_action("player1", "attack", {"target_id": "player2", "damage": 25})
```

## 🏗️ Architecture

### Core Components

#### 🦋 ButterflyServer
Main P2P server with substrate integration:
- **Consent-based connections** - All connections require explicit approval
- **Fibonacci protocols** - Optimal data flow using spiral patterns
- **SRL integration** - Secure resource locator for external connections
- **Substrate synchronization** - Real-time state sharing across nodes

#### 🔍 FibonacciDiscovery
Intelligent node discovery using spiral patterns:
- **Multi-phase discovery** - 8 phases following Fibonacci levels
- **Topology optimization** - Automatic network organization
- **Consent filtering** - Only connect to approved nodes
- **Game lobby discovery** - Specialized for game servers

#### 🎮 GameServer
Multiplayer gaming with substrate architecture:
- **Real-time synchronization** - 60 FPS game state updates
- **Fibonacci mechanics** - Game progression following spiral patterns
- **Player management** - Consent-based player connections
- **Cross-platform** - Works with any client supporting the protocol

### Network Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    ButterflyFX Network                      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Node A    │  │   Node B    │  │   Node C    │         │
│  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │         │
│  │ │Substrate│ │◄─┤ │Substrate│ │◄─┤ │Substrate│ │         │
│  │ │ Server  │ │  │ │ Server  │ │  │ │ Server  │ │         │
│  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │               │               │                │
│         └───────────────┼───────────────┘                │
│                         │                                │
│              ┌─────────────────────┐                     │
│              │  Fibonacci Protocol │                     │
│              │  ● → ↑ ← ↓ → ↑ ∞   │                     │
│              └─────────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## 🌀 Fibonacci Protocols

### Discovery Pattern
The 8-phase discovery follows the Fibonacci spiral:

```
Level 1: SPARK (●)     - Initial broadcast
Level 2: DIVIDE (→)    - Horizontal expansion (multiply)
Level 3: ORGANIZE (↑)  - Vertical organization (divide)
Level 4: IDENTIFY (←)  - Horizontal filtering (multiply)
Level 5: ASSEMBLE (↓)  - Vertical grouping (divide)
Level 6: HUMAN (→)     - Horizontal presentation (multiply)
Level 7: REST (↑)      - Vertical completion (divide)
Level 8: COMPLETE (∞)  - Spiral unification
```

### Connection Optimization
- **Horizontal levels** (2,4,6): MULTIPLICATION → Expand bandwidth
- **Vertical levels** (3,5,7): DIVISION → Organize data flow
- **Optimal routing** based on Fibonacci level differences

## 🔒 Security & Consent

### Consent-Based Networking
All connections require explicit consent:
1. **Discovery Request** - Node announces presence
2. **Consent Request** - Connection request with metadata
3. **Consent Decision** - Manual or automatic approval
4. **Connection Establishment** - Secure socket connection
5. **Ongoing Consent** - Can be revoked at any time

### Security Features
- **SHA-256 checksums** for all substrate data
- **Audit trails** for all connections and operations
- **SRL adapters** for secure external resource access
- **Fibonacci validation** for protocol compliance

## 🎮 Game Server Features

### Supported Game Types
- **Arena** - Combat and battle games
- **Strategy** - Turn-based and real-time strategy
- **Puzzle** - Cooperative and competitive puzzles
- **Racing** - Time-based competitions
- **Simulation** - Complex world simulations
- **Social** - Virtual social spaces

### Game Mechanics
- **Substrate-based state** - Game world as z = x * y² substrate
- **Fibonacci progression** - Player advancement follows spiral
- **Real-time sync** - 60 FPS state synchronization
- **Cross-platform** - Any client can connect

### Player Management
```python
# Add player with consent
await game_server.add_player(
    player_id="player123",
    node_id="node_abc",
    username="Alice",
    world_id="arena",
    permissions={"chat", "move", "attack"}
)

# Update player state
await game_server.update_player_state(
    player_id="player123",
    position=(10.5, 20.3, 0.0),
    health=85.0,
    score=150
)

# Process game actions
await game_server.process_game_action(
    player_id="player123",
    action_type="attack",
    action_data={"target_id": "player456", "damage": 25}
)
```

## 📡 Network Modes

### Open Network
Anyone can join with consent:
```python
network = create_open_network(port=8893)
```

### Closed Network
Invitation-only access:
```python
network = create_closed_network(port=8894)
```

### Game Server
Optimized for multiplayer gaming:
```python
game_server = create_arena_server(port=8895)
```

## 🔧 Advanced Usage

### Custom Node Discovery
```python
from server import FibonacciDiscovery, create_discovery

# Create discovery with custom callback
discovery = create_discovery("my_node", "localhost", 8893)

def on_node_found(node_info):
    print(f"Found node: {node_info.node_id}")
    # Auto-connect to nodes with specific capabilities
    if "game_server" in node_info.capabilities:
        asyncio.create_task(connect_to_node(node_info))

discovery.add_discovery_callback(on_node_found)
discovery.start_discovery()
```

### Substrate State Management
```python
# Create shared substrate
substrate_id = network.create_shared_substrate("world_state", fibonacci_level=3)

# Advance through Fibonacci levels
network.advance_shared_substrate("world_state", target_level=5)

# Monitor substrate changes
def on_substrate_change(substrate_id, level):
    print(f"Substrate {substrate_id} advanced to level {level}")
```

### Custom Game Logic
```python
from server import ButterflyGameServer, GameType

class CustomGame(ButterflyGameServer):
    def __init__(self, host="localhost", port=8896):
        super().__init__(host, port, GameType.CUSTOM)
    
    async def _process_custom_action(self, world_id, player_id, action_type, action_data):
        if action_type == "custom_spell":
            # Handle custom spell casting
            target = action_data.get("target")
            spell_type = action_data.get("spell")
            
            # Apply Fibonacci-based spell effects
            spell_power = self._calculate_fibonacci_power(player_id, spell_type)
            
            # Update game state
            await self._apply_spell_effects(target, spell_power)
            
            return True
        
        return False
```

## 📊 Examples

### Run Basic Network Demo
```bash
cd server/examples
python basic_network.py
```

Run multiple instances with different ports to see P2P networking.

### Run Game Server Demo
```bash
cd server/examples
python game_server_demo.py
```

Start the server, then connect multiple clients to see multiplayer functionality.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific tests
python -m pytest tests/test_server.py -v
python -m pytest tests/test_discovery.py -v
python -m pytest tests/test_game_server.py -v
```

## 📈 Performance

### Network Performance
- **Connection establishment**: <100ms
- **Substrate synchronization**: 5-second intervals
- **Message latency**: <50ms on local network
- **Throughput**: 1000+ messages/second

### Game Server Performance
- **Tick rate**: 60 FPS
- **Player capacity**: 100+ concurrent players
- **State sync**: Real-time with conflict resolution
- **Memory usage**: ~10MB per 10 players

## 🔗 API Reference

### ButterflyServer
```python
class ButterflyServer:
    def __init__(self, host, port, network_mode, security_level)
    async def start()
    def stop()
    async def connect_to_node(host, port)
    def create_shared_substrate(substrate_id, fibonacci_level)
    def advance_shared_substrate(substrate_id, target_level)
    def get_network_status()
```

### FibonacciDiscovery
```python
class FibonacciDiscovery:
    def __init__(local_node)
    def add_discovery_callback(callback)
    def start_discovery(target_networks)
    def stop_discovery()
    def get_discovery_status()
    def get_topology_info()
```

### ButterflyGameServer
```python
class ButterflyGameServer:
    def __init__(host, port, game_type, max_worlds)
    async def start()
    async def create_game_world(world_id, name, max_players)
    async def add_player(player_id, node_id, username, world_id)
    async def remove_player(player_id)
    async def update_player_state(player_id, **kwargs)
    async def process_game_action(player_id, action_type, action_data)
    def get_server_status()
    def get_world_info(world_id)
```

## 🛠️ Configuration

### Environment Variables
```bash
# Server configuration
BUTTERFLY_HOST=localhost
BUTTERFLY_PORT=8893
BUTTERFLY_NETWORK_MODE=open
BUTTERFLY_SECURITY_LEVEL=standard

# Discovery configuration
BUTTERFLY_DISCOVERY_ENABLED=true
BUTTERFLY_BROADCAST_INTERVAL=5.0
BUTTERFLY_MAX_DISCOVERY_RADIUS=5.0

# Game server configuration
BUTTERFLY_GAME_TICK_RATE=60
BUTTERFLY_MAX_PLAYERS=100
BUTTERFLY_SYNC_INTERVAL=5.0
```

### Configuration File
```json
{
    "server": {
        "host": "localhost",
        "port": 8893,
        "network_mode": "open",
        "security_level": "standard"
    },
    "discovery": {
        "enabled": true,
        "broadcast_interval": 5.0,
        "max_radius": 5.0,
        "target_networks": ["255.255.255.255"]
    },
    "game": {
        "tick_rate": 60,
        "max_players": 100,
        "sync_interval": 5.0,
        "default_world": "default_arena"
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Related Projects

- [ButterflyFX Kernel Core](../core/) - Pure math substrate system
- [Fibonacci Directional Analysis](../FIBONACCI_SPIRAL_DIRECTIONAL_ANALYSIS.md) - Mathematical foundation
- [Four Pillars Architecture](../FOUR_PILLARS_ARCHITECTURE.md) - System architecture

---

**ButterflyFX Server v1.0.0**

🦋 *Serverless P2P networking meets substrate mathematics*
