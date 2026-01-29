"""
ButterflyFX Node Discovery - Fibonacci Pattern-Based Network Discovery
======================================================================

Implements intelligent node discovery using Fibonacci spiral patterns:
- Automatic node detection through Fibonacci broadcasting
- Consent-based connection establishment
- Network topology optimization using directional operations
- Closed network invitation system
- Game server lobby management

Discovery Pattern:
● → ↑ ← ↓ → ↑ ∞ (Fibonacci spiral)
SPARK → DIVIDE → ORGANIZE → IDENTIFY → ASSEMBLE → HUMAN → REST → COMPLETE

Each discovery phase follows Fibonacci directional operations:
- Horizontal (→ ←): MULTIPLICATION - Expand search radius
- Vertical (↑ ↓): DIVISION - Organize discovered nodes
"""

from __future__ import annotations
import asyncio
import json
import socket
import time
import threading
from typing import Dict, List, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

from .butterfly_server import NodeInfo, NetworkMode, ConnectionType, ConsentStatus


class DiscoveryPhase(Enum):
    """Node discovery phases following Fibonacci levels"""
    SPARK = "spark"           # Level 1: Initial broadcast
    DIVIDE = "divide"         # Level 2: Horizontal expansion
    ORGANIZE = "organize"     # Level 3: Vertical organization
    IDENTIFY = "identify"     # Level 4: Horizontal filtering
    ASSEMBLE = "assemble"     # Level 5: Vertical grouping
    HUMAN = "human"           # Level 6: Human presentation
    REST = "rest"             # Level 7: Final organization
    COMPLETE = "complete"     # Level 8: Discovery complete


class DiscoveryMethod(Enum):
    """Methods for node discovery"""
    BROADCAST = "broadcast"   # UDP broadcast to local network
    MULTICAST = "multicast"   # IP multicast for larger networks
    DIRECT = "direct"         # Direct connection to known hosts
    INVITATION = "invitation" # Invitation-based for closed networks
    REGISTRY = "registry"     # Central registry (optional)


@dataclass
class DiscoveryPacket:
    """Discovery packet broadcast across network"""
    packet_id: str
    node_info: NodeInfo
    discovery_phase: DiscoveryPhase
    fibonacci_level: int
    search_radius: float
    target_networks: List[str] = field(default_factory=list)
    invitation_token: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    ttl: int = 3  # Time to live (hops)


@dataclass
class NetworkTopology:
    """Network topology information"""
    nodes: Dict[str, NodeInfo] = field(default_factory=dict)
    connections: Dict[str, Set[str]] = field(default_factory=dict)  # node_id -> connected nodes
    fibonacci_levels: Dict[str, int] = field(default_factory=dict)
    network_density: float = 0.0
    optimal_routes: Dict[Tuple[str, str], List[str]] = field(default_factory=dict)


class FibonacciDiscovery:
    """
    Fibonacci-based node discovery system
    
    Uses the Fibonacci spiral pattern to optimize network discovery:
    - Expands search radius following horizontal levels (multiply)
    - Organizes discovered nodes following vertical levels (divide)
    - Optimizes network topology based on Fibonacci relationships
    """
    
    def __init__(self, local_node: NodeInfo):
        self.local_node = local_node
        self.discovered_nodes: Dict[str, NodeInfo] = {}
        self.topology = NetworkTopology()
        self.discovery_callbacks: List[Callable[[NodeInfo], None]] = []
        
        # Discovery state
        self.current_phase = DiscoveryPhase.SPARK
        self.fibonacci_level = 1
        self.search_radius = 1.0
        self.discovery_active = False
        
        # Fibonacci pattern for discovery
        self.discovery_pattern = {
            DiscoveryPhase.SPARK: {'level': 1, 'radius': 1.0, 'method': DiscoveryMethod.BROADCAST},
            DiscoveryPhase.DIVIDE: {'level': 2, 'radius': 2.0, 'method': DiscoveryMethod.MULTICAST},
            DiscoveryPhase.ORGANIZE: {'level': 3, 'radius': 1.5, 'method': DiscoveryMethod.DIRECT},
            DiscoveryPhase.IDENTIFY: {'level': 4, 'radius': 3.0, 'method': DiscoveryMethod.BROADCAST},
            DiscoveryPhase.ASSEMBLE: {'level': 5, 'radius': 2.5, 'method': DiscoveryMethod.MULTICAST},
            DiscoveryPhase.HUMAN: {'level': 6, 'radius': 4.0, 'method': DiscoveryMethod.DIRECT},
            DiscoveryPhase.REST: {'level': 7, 'radius': 3.5, 'method': DiscoveryMethod.INVITATION},
            DiscoveryPhase.COMPLETE: {'level': 8, 'radius': 5.0, 'method': DiscoveryMethod.REGISTRY}
        }
        
        self.logger = logging.getLogger(f"FibonacciDiscovery-{local_node.node_id}")
    
    def add_discovery_callback(self, callback: Callable[[NodeInfo], None]):
        """Add callback for when new nodes are discovered"""
        self.discovery_callbacks.append(callback)
    
    def start_discovery(self, target_networks: List[str] = None):
        """Start Fibonacci-based node discovery"""
        self.discovery_active = True
        self.target_networks = target_networks or ["255.255.255.255"]  # Broadcast by default
        
        self.logger.info(f"🔍 Starting Fibonacci discovery from phase {self.current_phase.value}")
        
        # Start discovery loop
        threading.Thread(target=self._discovery_loop, daemon=True).start()
    
    def stop_discovery(self):
        """Stop node discovery"""
        self.discovery_active = False
        self.logger.info("🛑 Stopped Fibonacci discovery")
    
    def _discovery_loop(self):
        """Main discovery loop following Fibonacci phases"""
        phase_sequence = [
            DiscoveryPhase.SPARK,
            DiscoveryPhase.DIVIDE,
            DiscoveryPhase.ORGANIZE,
            DiscoveryPhase.IDENTIFY,
            DiscoveryPhase.ASSEMBLE,
            DiscoveryPhase.HUMAN,
            DiscoveryPhase.REST,
            DiscoveryPhase.COMPLETE
        ]
        
        for phase in phase_sequence:
            if not self.discovery_active:
                break
            
            self.current_phase = phase
            phase_config = self.discovery_pattern[phase]
            self.fibonacci_level = phase_config['level']
            self.search_radius = phase_config['radius']
            
            self.logger.info(f"🌀 Discovery phase: {phase.value} (Level {self.fibonacci_level}, Radius {self.search_radius})")
            
            # Execute discovery for this phase
            asyncio.run(self._execute_phase_discovery(phase, phase_config))
            
            # Wait before next phase
            time.sleep(2.0)
        
        self.logger.info("✅ Fibonacci discovery complete")
        self._optimize_topology()
    
    async def _execute_phase_discovery(self, phase: DiscoveryPhase, config: Dict):
        """Execute discovery for a specific Fibonacci phase"""
        method = config['method']
        
        if method == DiscoveryMethod.BROADCAST:
            await self._broadcast_discovery()
        elif method == DiscoveryMethod.MULTICAST:
            await self._multicast_discovery()
        elif method == DiscoveryMethod.DIRECT:
            await self._direct_discovery()
        elif method == DiscoveryMethod.INVITATION:
            await self._invitation_discovery()
        elif method == DiscoveryMethod.REGISTRY:
            await self._registry_discovery()
    
    async def _broadcast_discovery(self):
        """UDP broadcast discovery for local network"""
        packet = DiscoveryPacket(
            packet_id=self._generate_packet_id(),
            node_info=self.local_node,
            discovery_phase=self.current_phase,
            fibonacci_level=self.fibonacci_level,
            search_radius=self.search_radius
        )
        
        packet_data = json.dumps(packet.__dict__).encode()
        
        # Create UDP socket for broadcasting
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1.0)
        
        try:
            # Broadcast to all networks
            for network in self.target_networks:
                sock.sendto(packet_data, (network, 8892))  # Discovery port
                
            self.logger.debug(f"📡 Broadcast discovery packet (Level {self.fibonacci_level})")
            
            # Listen for responses
            await self._listen_for_responses(sock, timeout=3.0)
            
        except Exception as e:
            self.logger.error(f"Broadcast discovery error: {e}")
        finally:
            sock.close()
    
    async def _multicast_discovery(self):
        """IP multicast discovery for larger networks"""
        multicast_group = '224.0.0.251'  # Link-local multicast
        port = 8892
        
        packet = DiscoveryPacket(
            packet_id=self._generate_packet_id(),
            node_info=self.local_node,
            discovery_phase=self.current_phase,
            fibonacci_level=self.fibonacci_level,
            search_radius=self.search_radius
        )
        
        packet_data = json.dumps(packet.__dict__).encode()
        
        # Create multicast socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        ttl = struct.pack('b', 1)  # TTL = 1 (local network)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
        try:
            sock.sendto(packet_data, (multicast_group, port))
            self.logger.debug(f"📡 Multicast discovery packet (Level {self.fibonacci_level})")
            
            await self._listen_for_responses(sock, timeout=3.0)
            
        except Exception as e:
            self.logger.error(f"Multicast discovery error: {e}")
        finally:
            sock.close()
    
    async def _direct_discovery(self):
        """Direct discovery to known hosts"""
        # Common ports to check for ButterflyFX nodes
        common_ports = [8893, 8894, 8895, 8896]
        
        # Local network ranges to scan
        local_ip = self._get_local_ip()
        if local_ip:
            network_parts = local_ip.split('.')
            base_network = f"{network_parts[0]}.{network_parts[1]}.{network_parts[2]}"
            
            # Scan last octet based on search radius
            start_octet = max(1, int(network_parts[3]) - int(self.search_radius * 10))
            end_octet = min(254, int(network_parts[3]) + int(self.search_radius * 10))
            
            for octet in range(start_octet, end_octet + 1):
                target_ip = f"{base_network}.{octet}"
                
                for port in common_ports:
                    if await self._probe_node(target_ip, port):
                        break  # Found node at this IP, try next IP
    
    async def _probe_node(self, host: str, port: int) -> bool:
        """Probe a specific host:port for ButterflyFX node"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=1.0
            )
            
            # Send discovery probe
            probe = {
                'type': 'discovery_probe',
                'node_id': self.local_node.node_id,
                'fibonacci_level': self.fibonacci_level
            }
            
            probe_data = json.dumps(probe).encode()
            writer.write(probe_data)
            await writer.drain()
            
            # Wait for response
            response_data = await asyncio.wait_for(
                reader.read(1024),
                timeout=1.0
            )
            
            response = json.loads(response_data.decode())
            
            if response.get('type') == 'discovery_response':
                node_info = NodeInfo(**response.get('node_info'))
                await self._handle_discovered_node(node_info)
            
            writer.close()
            await writer.wait_closed()
            
            return True
            
        except Exception:
            return False
    
    async def _invitation_discovery(self):
        """Invitation-based discovery for closed networks"""
        # For closed networks, only discover invited nodes
        # This would integrate with the server's invitation system
        pass
    
    async def _registry_discovery(self):
        """Registry-based discovery (optional central service)"""
        # Optional: Connect to central registry for node discovery
        pass
    
    async def _listen_for_responses(self, sock: socket.socket, timeout: float):
        """Listen for discovery responses"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                data, addr = sock.recvfrom(1024)
                
                # Parse response packet
                response_data = json.loads(data.decode())
                
                if response_data.get('type') == 'discovery_response':
                    node_info = NodeInfo(**response_data.get('node_info'))
                    await self._handle_discovered_node(node_info)
                
            except socket.timeout:
                break
            except Exception as e:
                self.logger.debug(f"Error parsing discovery response: {e}")
    
    async def _handle_discovered_node(self, node_info: NodeInfo):
        """Handle a newly discovered node"""
        if node_info.node_id == self.local_node.node_id:
            return  # Skip self
        
        if node_info.node_id not in self.discovered_nodes:
            self.discovered_nodes[node_info.node_id] = node_info
            self.topology.nodes[node_info.node_id] = node_info
            self.topology.fibonacci_levels[node_info.node_id] = node_info.fibonacci_level
            
            self.logger.info(f"🔍 Discovered node: {node_info.node_id} at {node_info.host}:{node_info.port}")
            
            # Call discovery callbacks
            for callback in self.discovery_callbacks:
                try:
                    callback(node_info)
                except Exception as e:
                    self.logger.error(f"Discovery callback error: {e}")
    
    def _optimize_topology(self):
        """Optimize network topology using Fibonacci relationships"""
        self.logger.info("🔧 Optimizing network topology")
        
        # Calculate network density
        total_nodes = len(self.topology.nodes) + 1  # +1 for self
        self.topology.network_density = total_nodes / 255.0  # Max nodes in /24 network
        
        # Calculate optimal routes based on Fibonacci levels
        for node_id1 in self.topology.nodes:
            for node_id2 in self.topology.nodes:
                if node_id1 != node_id2:
                    route = self._calculate_fibonacci_route(node_id1, node_id2)
                    self.topology.optimal_routes[(node_id1, node_id2)] = route
        
        self.logger.info(f"✅ Topology optimized: {total_nodes} nodes, density: {self.topology.network_density:.3f}")
    
    def _calculate_fibonacci_route(self, from_node: str, to_node: str) -> List[str]:
        """
        Calculate optimal route between nodes using Fibonacci levels
        
        Route calculation follows Fibonacci spiral:
        - Connect nodes with similar Fibonacci levels directly
        - Use intermediate nodes for large level differences
        - Prefer horizontal connections (multiplication) for bandwidth
        - Use vertical connections (division) for organization
        """
        from_level = self.topology.fibonacci_levels.get(from_node, 0)
        to_level = self.topology.fibonacci_levels.get(to_node, 0)
        
        level_diff = abs(from_level - to_level)
        
        if level_diff <= 2:
            # Direct connection for close levels
            return [from_node, to_node]
        else:
            # Find intermediate node
            intermediate_level = (from_level + to_level) // 2
            
            # Find node with closest Fibonacci level
            intermediate_node = None
            min_diff = float('inf')
            
            for node_id, node_level in self.topology.fibonacci_levels.items():
                if node_id != from_node and node_id != to_node:
                    diff = abs(node_level - intermediate_level)
                    if diff < min_diff:
                        min_diff = diff
                        intermediate_node = node_id
            
            if intermediate_node:
                return [from_node, intermediate_node, to_node]
            else:
                return [from_node, to_node]  # Fallback to direct
    
    def _generate_packet_id(self) -> str:
        """Generate unique packet ID"""
        import hashlib
        data = f"{self.local_node.node_id}:{time.time()}:{self.fibonacci_level}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _get_local_ip(self) -> Optional[str]:
        """Get local IP address"""
        try:
            # Connect to external address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return None
    
    def get_discovery_status(self) -> Dict[str, Any]:
        """Get current discovery status"""
        return {
            'active': self.discovery_active,
            'phase': self.current_phase.value,
            'fibonacci_level': self.fibonacci_level,
            'search_radius': self.search_radius,
            'discovered_nodes': len(self.discovered_nodes),
            'network_density': self.topology.network_density,
            'topology_optimized': len(self.topology.optimal_routes) > 0
        }
    
    def get_topology_info(self) -> Dict[str, Any]:
        """Get network topology information"""
        return {
            'total_nodes': len(self.topology.nodes) + 1,  # +1 for self
            'node_levels': self.topology.fibonacci_levels,
            'network_density': self.topology.network_density,
            'optimal_routes': len(self.topology.optimal_routes),
            'connections': {k: list(v) for k, v in self.topology.connections.items()}
        }


class GameLobbyDiscovery:
    """
    Specialized discovery for game server lobbies
    
    Extends Fibonacci discovery with game-specific features:
    - Game type filtering
    - Player count limits
    - Latency-based matchmaking
    - Skill level matching
    """
    
    def __init__(self, local_node: NodeInfo, game_type: str = "default"):
        self.base_discovery = FibonacciDiscovery(local_node)
        self.game_type = game_type
        self.game_lobbies: Dict[str, Dict[str, Any]] = {}
        self.player_preferences: Dict[str, Dict[str, Any]] = {}
        
        # Add game-specific discovery callback
        self.base_discovery.add_discovery_callback(self._handle_game_node)
    
    async def _handle_game_node(self, node_info: NodeInfo):
        """Handle discovery of game server node"""
        if 'game_server' in node_info.capabilities:
            # Query game server for lobby information
            await self._query_game_lobby(node_info)
    
    async def _query_game_lobby(self, node_info: NodeInfo):
        """Query game server for lobby information"""
        try:
            reader, writer = await asyncio.open_connection(node_info.host, node_info.port)
            
            query = {
                'type': 'lobby_query',
                'game_type': self.game_type,
                'node_id': self.base_discovery.local_node.node_id
            }
            
            query_data = json.dumps(query).encode()
            writer.write(query_data)
            await writer.drain()
            
            response_data = await reader.read(2048)
            response = json.loads(response_data.decode())
            
            if response.get('type') == 'lobby_response':
                lobby_info = response.get('lobby_info', {})
                self.game_lobbies[node_info.node_id] = lobby_info
                
                self.logger.info(f"🎮 Found game lobby: {node_info.node_id} - {lobby_info.get('name', 'Unknown')}")
            
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            self.logger.error(f"Error querying game lobby {node_info.node_id}: {e}")
    
    def find_best_lobby(self, player_preferences: Dict[str, Any]) -> Optional[str]:
        """Find best game lobby based on player preferences"""
        best_lobby = None
        best_score = -1
        
        for lobby_id, lobby_info in self.game_lobbies.items():
            score = self._calculate_lobby_score(lobby_info, player_preferences)
            
            if score > best_score:
                best_score = score
                best_lobby = lobby_id
        
        return best_lobby
    
    def _calculate_lobby_score(self, lobby_info: Dict[str, Any], preferences: Dict[str, Any]) -> float:
        """Calculate score for lobby matching"""
        score = 0.0
        
        # Player count matching
        current_players = lobby_info.get('current_players', 0)
        max_players = lobby_info.get('max_players', 10)
        preferred_players = preferences.get('preferred_players', max_players)
        
        if current_players < max_players:
            player_score = 1.0 - abs(current_players - preferred_players) / max_players
            score += player_score * 0.4
        
        # Latency (if available)
        latency = lobby_info.get('latency', 100)
        max_latency = preferences.get('max_latency', 200)
        
        if latency <= max_latency:
            latency_score = 1.0 - (latency / max_latency)
            score += latency_score * 0.3
        
        # Game mode matching
        if lobby_info.get('game_mode') == preferences.get('game_mode'):
            score += 0.2
        
        # Skill level matching
        lobby_skill = lobby_info.get('average_skill', 5.0)
        player_skill = preferences.get('skill_level', 5.0)
        
        skill_diff = abs(lobby_skill - player_skill)
        skill_score = 1.0 - (skill_diff / 10.0)  # Max skill difference of 10
        score += skill_score * 0.1
        
        return score
    
    def get_lobby_status(self) -> Dict[str, Any]:
        """Get current lobby discovery status"""
        return {
            'game_type': self.game_type,
            'available_lobbies': len(self.game_lobbies),
            'lobbies': self.game_lobbies,
            'discovery_status': self.base_discovery.get_discovery_status()
        }


# Convenience functions
def create_discovery(node_id: str, host: str, port: int, network_mode: NetworkMode = NetworkMode.OPEN) -> FibonacciDiscovery:
    """Create Fibonacci discovery instance"""
    node_info = NodeInfo(
        node_id=node_id,
        host=host,
        port=port,
        public_key="",
        capabilities=['substrate_sync', 'fibonacci_protocol'],
        network_mode=network_mode,
        fibonacci_level=0
    )
    
    return FibonacciDiscovery(node_info)


def create_game_lobby_discovery(node_id: str, host: str, port: int, game_type: str = "default") -> GameLobbyDiscovery:
    """Create game lobby discovery instance"""
    node_info = NodeInfo(
        node_id=node_id,
        host=host,
        port=port,
        public_key="",
        capabilities=['game_server', 'substrate_sync'],
        network_mode=NetworkMode.GAME_SERVER,
        fibonacci_level=3  # Start at ORGANIZE level for games
    )
    
    return GameLobbyDiscovery(node_info, game_type)


import struct  # Added for multicast TTL

__all__ = [
    'FibonacciDiscovery',
    'GameLobbyDiscovery',
    'DiscoveryPhase',
    'DiscoveryMethod',
    'DiscoveryPacket',
    'NetworkTopology',
    'create_discovery',
    'create_game_lobby_discovery'
]
