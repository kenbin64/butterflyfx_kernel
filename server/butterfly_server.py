"""
ButterflyFX Server - Peer-to-Peer Substrate Networking
========================================================

A serverless, peer-to-peer networking system built on:
- Substrate-based state management with z = x * y² canonical equation
- Fibonacci spiral protocols for connection patterns and data flow
- Consent-based node discovery and secure connections
- Socket-based peer networking with closed network support
- Game server capabilities with substrate state synchronization

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    ButterflyFX Network                      │
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

Features:
- Serverless P2P networking with automatic node discovery
- Fibonacci-based connection patterns for optimal data flow
- Consent-based connections (explicit approval required)
- Closed networks with invitation-only access
- Substrate state synchronization across nodes
- Game server mode with real-time state updates
- Secure socket communication with encryption
"""

from __future__ import annotations
import asyncio
import json
import hashlib
import time
import socket
import threading
from typing import Dict, List, Optional, Tuple, Any, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

# Import core substrate components
from core import (
    SecureSubstrate, SecureSubstrateFactory, SubstrateAPI,
    SecurityLevel, get_fibonacci_creation_point, create_canonical_substrate
)
from core.fibonacci_directional_levels import (
    Direction, Operation, FIBONACCI_LEVELS, is_multiplication_level, is_division_level
)
from core.srl import SRL, bitcount, timestamp_now


class NetworkMode(Enum):
    """Network operation modes"""
    OPEN = "open"           # Anyone can join with consent
    CLOSED = "closed"       # Invitation only
    GAME_SERVER = "game"    # Game server with real-time sync
    HYBRID = "hybrid"       # Mixed mode with different node types


class ConnectionType(Enum):
    """Types of peer connections"""
    DIRECT = "direct"       # Direct socket connection
    RELAY = "relay"         # Through relay node
    BROADCAST = "broadcast" # One-to-many broadcast
    SYNCHRONIZED = "sync"   # Synchronized substrate state


class ConsentStatus(Enum):
    """Connection consent status"""
    PENDING = "pending"     # Awaiting response
    ACCEPTED = "accepted"   # Connection accepted
    REJECTED = "rejected"   # Connection rejected
    REVOKED = "revoked"     # Previously accepted, now revoked


@dataclass
class NodeInfo:
    """Information about a network node"""
    node_id: str
    host: str
    port: int
    public_key: str  # For secure communication
    capabilities: List[str] = field(default_factory=list)
    network_mode: NetworkMode = NetworkMode.OPEN
    fibonacci_level: int = 0  # Current Fibonacci level for this node
    substrate_id: str = ""    # Primary substrate ID
    last_seen: float = field(default_factory=time.time)
    consent_status: ConsentStatus = ConsentStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectionRequest:
    """Connection request between nodes"""
    request_id: str
    from_node: NodeInfo
    to_node: NodeInfo
    connection_type: ConnectionType
    fibonacci_pattern: List[int]  # Levels for connection pattern
    message: str = ""
    timestamp: float = field(default_factory=time.time)
    signature: str = ""  # Cryptographic signature


@dataclass
class SubstrateSync:
    """Substrate synchronization data"""
    substrate_id: str
    fibonacci_level: int
    checksum: str
    data_hash: str
    timestamp: float
    sync_type: str = "full"  # full, delta, state_only
    package_data: Optional[Dict[str, Any]] = None


class ButterflyProtocol:
    """
    Fibonacci-based networking protocol
    
    Uses Fibonacci spiral patterns for:
    - Connection establishment (● → ↑ ← ↓ → ↑ ∞)
    - Data flow optimization (horizontal/vertical operations)
    - Network topology organization
    - Load balancing and routing
    """
    
    def __init__(self):
        self.connection_patterns = {
            ConnectionType.DIRECT: [1, 2, 3],      # Spark → Divide → Organize
            ConnectionType.RELAY: [2, 4, 6],       # Divide → Identify → Human
            ConnectionType.BROADCAST: [3, 5, 7],    # Organize → Assemble → Rest
            ConnectionType.SYNCHRONIZED: [1, 4, 7] # Spark → Identify → Rest
        }
    
    def get_connection_pattern(self, conn_type: ConnectionType) -> List[int]:
        """Get Fibonacci pattern for connection type"""
        return self.connection_patterns.get(conn_type, [1, 2, 3])
    
    def calculate_optimal_route(self, from_node: NodeInfo, to_node: NodeInfo) -> List[int]:
        """
        Calculate optimal Fibonacci route between nodes
        
        Uses directional operations:
        - Horizontal levels (2,4,6): MULTIPLICATION - expand bandwidth
        - Vertical levels (3,5,7): DIVISION - organize data flow
        """
        # Calculate distance in Fibonacci space
        level_diff = abs(from_node.fibonacci_level - to_node.fibonacci_level)
        
        if level_diff <= 2:
            # Close levels - use direct horizontal expansion
            return [from_node.fibonacci_level, to_node.fibonacci_level]
        else:
            # Distant levels - use vertical organization
            mid_level = (from_node.fibonacci_level + to_node.fibonacci_level) // 2
            return [from_node.fibonacci_level, mid_level, to_node.fibonacci_level]
    
    def optimize_data_flow(self, data_size: int, connection_pattern: List[int]) -> Dict[str, Any]:
        """
        Optimize data flow based on Fibonacci pattern
        
        Horizontal levels: Multiply bandwidth (parallel streams)
        Vertical levels: Divide data (chunked transmission)
        """
        optimization = {
            'parallel_streams': 1,
            'chunk_size': data_size,
            'compression': False,
            'priority': 'normal'
        }
        
        # Analyze pattern for optimization
        horizontal_levels = [lvl for lvl in connection_pattern if is_multiplication_level(lvl)]
        vertical_levels = [lvl for lvl in connection_pattern if is_division_level(lvl)]
        
        if horizontal_levels:
            # Multiply bandwidth based on highest horizontal level
            max_horizontal = max(horizontal_levels)
            optimization['parallel_streams'] = max_horizontal
            optimization['priority'] = 'high'
        
        if vertical_levels:
            # Divide data based on highest vertical level
            max_vertical = max(vertical_levels)
            optimization['chunk_size'] = data_size // max_vertical
            optimization['compression'] = True
        
        return optimization


class ButterflyServer:
    """
    Main ButterflyFX server with P2P networking and substrate management
    """
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 8893,
                 node_id: Optional[str] = None,
                 network_mode: NetworkMode = NetworkMode.OPEN,
                 security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize ButterflyFX server
        
        Args:
            host: Host address for this node
            port: Port for this node
            node_id: Unique node identifier (auto-generated if None)
            network_mode: Network operation mode
            security_level: Security validation level
        """
        self.host = host
        self.port = port
        self.node_id = node_id or self._generate_node_id()
        self.network_mode = network_mode
        self.security_level = security_level
        
        # Core components
        self.substrate_api = SubstrateAPI(security_level=security_level)
        self.protocol = ButterflyProtocol()
        
        # Networking
        self.server_socket: Optional[socket.socket] = None
        self.connected_nodes: Dict[str, NodeInfo] = {}
        self.pending_connections: Dict[str, ConnectionRequest] = {}
        self.connection_handlers: Dict[str, asyncio.Task] = {}
        
        # Substrate management
        self.shared_substrates: Dict[str, SecureSubstrate] = {}
        self.sync_queue: List[SubstrateSync] = []
        
        # Game server state
        self.game_state: Dict[str, Any] = {}
        self.game_players: Set[str] = set()
        
        # Logging
        self.logger = logging.getLogger(f"ButterflyServer-{self.node_id}")
        self.logger.setLevel(logging.INFO)
        
        # Threading
        self.running = False
        self.server_thread: Optional[threading.Thread] = None
        self.sync_thread: Optional[threading.Thread] = None
    
    def _generate_node_id(self) -> str:
        """Generate unique node ID based on host, port, and timestamp"""
        data = f"{self.host}:{self.port}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    async def start_server(self):
        """Start the ButterflyFX server"""
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            self.running = True
            self.logger.info(f"🦋 ButterflyFX Server started: {self.host}:{self.port}")
            self.logger.info(f"Node ID: {self.node_id}")
            self.logger.info(f"Network Mode: {self.network_mode.value}")
            self.logger.info(f"Fibonacci Level: 0 (SPARK)")
            
            # Start server loop
            await self._server_loop()
            
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            raise
    
    async def _server_loop(self):
        """Main server loop for accepting connections"""
        while self.running:
            try:
                client_socket, address = await asyncio.get_event_loop().sock_accept(self.server_socket)
                await self._handle_client_connection(client_socket, address)
            except Exception as e:
                if self.running:
                    self.logger.error(f"Server loop error: {e}")
                await asyncio.sleep(0.1)
    
    async def _handle_client_connection(self, client_socket: socket.socket, address: Tuple[str, int]):
        """Handle incoming client connection"""
        try:
            # Receive connection request
            data = await asyncio.get_event_loop().sock_recv(client_socket, 4096)
            if not data:
                return
            
            request_data = json.loads(data.decode())
            request = ConnectionRequest(**request_data)
            
            # Process connection request
            response = await self._process_connection_request(request, client_socket)
            
            # Send response
            response_data = json.dumps(response).encode()
            await asyncio.get_event_loop().sock_sendall(client_socket, response_data)
            
            # If accepted, establish persistent connection
            if response.get('status') == 'accepted':
                await self._establish_connection(request, client_socket)
            
        except Exception as e:
            self.logger.error(f"Error handling client connection: {e}")
        finally:
            client_socket.close()
    
    async def _process_connection_request(self, request: ConnectionRequest, client_socket: socket.socket) -> Dict[str, Any]:
        """Process incoming connection request with consent logic"""
        self.logger.info(f"🔗 Connection request from {request.from_node.node_id}")
        
        # Check network mode compatibility
        if self.network_mode == NetworkMode.CLOSED:
            # Closed network - check if this node is invited
            if not self._is_node_invited(request.from_node.node_id):
                return {
                    'status': 'rejected',
                    'reason': 'Closed network - invitation required',
                    'request_id': request.request_id
                }
        
        # Check if already connected
        if request.from_node.node_id in self.connected_nodes:
            return {
                'status': 'rejected',
                'reason': 'Already connected',
                'request_id': request.request_id
            }
        
        # Store pending request
        self.pending_connections[request.request_id] = request
        
        # For demo purposes, auto-accept. In production, this would require user consent
        consent_given = await self._request_consent(request)
        
        if consent_given:
            # Accept connection
            node_info = request.from_node
            node_info.consent_status = ConsentStatus.ACCEPTED
            node_info.last_seen = time.time()
            
            self.connected_nodes[request.from_node.node_id] = node_info
            
            self.logger.info(f"✅ Accepted connection from {request.from_node.node_id}")
            
            return {
                'status': 'accepted',
                'node_id': self.node_id,
                'fibonacci_level': 0,  # Start at SPARK level
                'substrate_id': self._get_primary_substrate_id(),
                'request_id': request.request_id,
                'network_capabilities': self._get_network_capabilities()
            }
        else:
            # Reject connection
            self.logger.info(f"❌ Rejected connection from {request.from_node.node_id}")
            
            return {
                'status': 'rejected',
                'reason': 'Consent not given',
                'request_id': request.request_id
            }
    
    async def _request_consent(self, request: ConnectionRequest) -> bool:
        """
        Request consent for connection
        
        In production, this would prompt the user. For demo, auto-accept based on:
        - Network mode
        - Node capabilities
        - Fibonacci level compatibility
        """
        if self.network_mode == NetworkMode.OPEN:
            return True
        
        if self.network_mode == NetworkMode.GAME_SERVER:
            # Game server - accept players
            return 'game_client' in request.from_node.capabilities
        
        if self.network_mode == NetworkMode.CLOSED:
            # Already checked invitation in _process_connection_request
            return True
        
        # Check Fibonacci level compatibility
        level_diff = abs(request.from_node.fibonacci_level - 0)  # Our level is 0
        return level_diff <= 3  # Accept within 3 levels
    
    async def _establish_connection(self, request: ConnectionRequest, client_socket: socket.socket):
        """Establish persistent connection with accepted node"""
        node_id = request.from_node.node_id
        
        # Start connection handler task
        handler_task = asyncio.create_task(
            self._handle_connection(node_id, client_socket)
        )
        self.connection_handlers[node_id] = handler_task
        
        self.logger.info(f"🔗 Established persistent connection with {node_id}")
    
    async def _handle_connection(self, node_id: str, client_socket: socket.socket):
        """Handle ongoing communication with connected node"""
        try:
            while self.running and node_id in self.connected_nodes:
                # Receive data
                data = await asyncio.get_event_loop().sock_recv(client_socket, 4096)
                if not data:
                    break
                
                # Process message
                message = json.loads(data.decode())
                await self._process_message(node_id, message)
                
        except Exception as e:
            self.logger.error(f"Error handling connection with {node_id}: {e}")
        finally:
            # Cleanup
            await self._cleanup_connection(node_id)
    
    async def _process_message(self, from_node_id: str, message: Dict[str, Any]):
        """Process incoming message from connected node"""
        message_type = message.get('type')
        
        if message_type == 'substrate_sync':
            await self._handle_substrate_sync(from_node_id, message)
        elif message_type == 'game_update':
            await self._handle_game_update(from_node_id, message)
        elif message_type == 'fibonacci_advance':
            await self._handle_fibonacci_advance(from_node_id, message)
        elif message_type == 'heartbeat':
            await self._handle_heartbeat(from_node_id, message)
        else:
            self.logger.warning(f"Unknown message type: {message_type}")
    
    async def _handle_substrate_sync(self, from_node_id: str, message: Dict[str, Any]):
        """Handle substrate synchronization message"""
        sync_data = SubstrateSync(**message.get('sync_data'))
        
        # Verify substrate integrity
        if sync_data.substrate_id in self.shared_substrates:
            local_substrate = self.shared_substrates[sync_data.substrate_id]
            local_verification = local_substrate.verify_integrity()
            
            if local_verification['checksum'] != sync_data.checksum:
                # Substrates are out of sync - request full sync
                await self._request_full_sync(from_node_id, sync_data.substrate_id)
            else:
                self.logger.debug(f"✅ Substrate {sync_data.substrate_id} already in sync")
        else:
            # New substrate - import it
            if sync_data.package_data:
                try:
                    imported_id = self.substrate_api.import_substrate(sync_data.package_data)
                    self.shared_substrates[sync_data.substrate_id] = self.substrate_api.substrates[imported_id]
                    self.logger.info(f"📥 Imported shared substrate: {sync_data.substrate_id}")
                except Exception as e:
                    self.logger.error(f"Failed to import substrate {sync_data.substrate_id}: {e}")
    
    async def _handle_game_update(self, from_node_id: str, message: Dict[str, Any]):
        """Handle game state update"""
        if self.network_mode != NetworkMode.GAME_SERVER:
            return
        
        game_data = message.get('game_data')
        player_id = message.get('player_id')
        
        # Update game state
        self.game_state.update(game_data)
        if player_id:
            self.game_players.add(player_id)
        
        # Broadcast to other players
        await self._broadcast_game_update(from_node_id, game_data, player_id)
    
    async def _handle_fibonacci_advance(self, from_node_id: str, message: Dict[str, Any]):
        """Handle Fibonacci level advancement notification"""
        target_level = message.get('target_level')
        substrate_id = message.get('substrate_id')
        
        if substrate_id in self.shared_substrates:
            # Advance local substrate to match
            local_substrate = self.shared_substrates[substrate_id]
            advanced = local_substrate.advance_fibonacci_level(target_level)
            self.shared_substrates[substrate_id] = advanced
            
            self.logger.info(f"🌀 Advanced substrate {substrate_id} to level {target_level}")
    
    async def _handle_heartbeat(self, from_node_id: str, message: Dict[str, Any]):
        """Handle heartbeat message"""
        if from_node_id in self.connected_nodes:
            self.connected_nodes[from_node_id].last_seen = time.time()
    
    async def _broadcast_game_update(self, exclude_node: str, game_data: Dict[str, Any], player_id: str):
        """Broadcast game update to all connected players except sender"""
        message = {
            'type': 'game_update',
            'game_data': game_data,
            'player_id': player_id,
            'timestamp': time.time()
        }
        
        for node_id in self.connected_nodes:
            if node_id != exclude_node:
                await self._send_message(node_id, message)
    
    async def _request_full_sync(self, from_node_id: str, substrate_id: str):
        """Request full substrate synchronization from node"""
        message = {
            'type': 'sync_request',
            'substrate_id': substrate_id,
            'requester': self.node_id
        }
        
        await self._send_message(from_node_id, message)
    
    async def _send_message(self, node_id: str, message: Dict[str, Any]):
        """Send message to connected node"""
        # This would use the persistent connection socket
        # For now, just log the message
        self.logger.debug(f"Sending to {node_id}: {message}")
    
    async def _cleanup_connection(self, node_id: str):
        """Clean up connection with node"""
        if node_id in self.connection_handlers:
            self.connection_handlers[node_id].cancel()
            del self.connection_handlers[node_id]
        
        if node_id in self.connected_nodes:
            del self.connected_nodes[node_id]
        
        self.logger.info(f"🔌 Disconnected from node: {node_id}")
    
    def _is_node_invited(self, node_id: str) -> bool:
        """Check if node is invited to closed network"""
        # For demo, accept all. In production, check invitation list
        return True
    
    def _get_primary_substrate_id(self) -> str:
        """Get primary substrate ID for this node"""
        if not self.shared_substrates:
            # Create primary substrate
            primary = create_canonical_substrate(
                f"{self.node_id}_primary",
                fibonacci_level=0,
                security_level=self.security_level
            )
            self.shared_substrates[f"{self.node_id}_primary"] = primary
        
        return f"{self.node_id}_primary"
    
    def _get_network_capabilities(self) -> List[str]:
        """Get network capabilities of this node"""
        capabilities = ['substrate_sync', 'fibonacci_protocol']
        
        if self.network_mode == NetworkMode.GAME_SERVER:
            capabilities.append('game_server')
        
        return capabilities
    
    async def connect_to_node(self, host: str, port: int, message: str = "") -> bool:
        """
        Connect to another node with consent
        
        Args:
            host: Target node host
            port: Target node port
            message: Connection message
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create connection request
            request_id = hashlib.sha256(f"{self.node_id}:{host}:{port}:{time.time()}".encode()).hexdigest()[:16]
            
            from_node = NodeInfo(
                node_id=self.node_id,
                host=self.host,
                port=self.port,
                public_key="",  # Would be actual public key in production
                capabilities=self._get_network_capabilities(),
                network_mode=self.network_mode,
                fibonacci_level=0,
                substrate_id=self._get_primary_substrate_id()
            )
            
            to_node = NodeInfo(
                node_id="",  # Will be filled by response
                host=host,
                port=port,
                public_key=""
            )
            
            request = ConnectionRequest(
                request_id=request_id,
                from_node=from_node,
                to_node=to_node,
                connection_type=ConnectionType.DIRECT,
                fibonacci_pattern=self.protocol.get_connection_pattern(ConnectionType.DIRECT),
                message=message
            )
            
            # Connect to target node
            reader, writer = await asyncio.open_connection(host, port)
            
            # Send request
            request_data = json.dumps(request.__dict__).encode()
            writer.write(request_data)
            await writer.drain()
            
            # Receive response
            response_data = await reader.read(4096)
            response = json.loads(response_data.decode())
            
            writer.close()
            await writer.wait_closed()
            
            if response.get('status') == 'accepted':
                self.logger.info(f"✅ Successfully connected to node at {host}:{port}")
                return True
            else:
                self.logger.info(f"❌ Connection rejected: {response.get('reason')}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to connect to {host}:{port}: {e}")
            return False
    
    def create_shared_substrate(self, substrate_id: str, fibonacci_level: int = 0) -> str:
        """
        Create a substrate that can be shared across the network
        
        Args:
            substrate_id: Unique identifier for the substrate
            fibonacci_level: Initial Fibonacci level
        
        Returns:
            The created substrate ID
        """
        substrate = create_canonical_substrate(
            substrate_id,
            fibonacci_level=fibonacci_level,
            security_level=self.security_level
        )
        
        self.shared_substrates[substrate_id] = substrate
        self.logger.info(f"📐 Created shared substrate: {substrate_id} at level {fibonacci_level}")
        
        return substrate_id
    
    def advance_shared_substrate(self, substrate_id: str, target_level: int) -> bool:
        """
        Advance shared substrate to target Fibonacci level
        
        Args:
            substrate_id: ID of substrate to advance
            target_level: Target Fibonacci level (0-8)
        
        Returns:
            True if successful, False otherwise
        """
        if substrate_id not in self.shared_substrates:
            self.logger.error(f"Substrate {substrate_id} not found")
            return False
        
        try:
            substrate = self.shared_substrates[substrate_id]
            advanced = substrate.advance_fibonacci_level(target_level)
            self.shared_substrates[substrate_id] = advanced
            
            self.logger.info(f"🌀 Advanced substrate {substrate_id} to level {target_level}")
            
            # Notify connected nodes
            asyncio.create_task(self._notify_substrate_advance(substrate_id, target_level))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to advance substrate {substrate_id}: {e}")
            return False
    
    async def _notify_substrate_advance(self, substrate_id: str, target_level: int):
        """Notify connected nodes about substrate advancement"""
        message = {
            'type': 'fibonacci_advance',
            'substrate_id': substrate_id,
            'target_level': target_level,
            'timestamp': time.time()
        }
        
        for node_id in self.connected_nodes:
            await self._send_message(node_id, message)
    
    def start_background_sync(self):
        """Start background substrate synchronization"""
        def sync_loop():
            while self.running:
                try:
                    # Sync all shared substrates
                    for substrate_id, substrate in self.shared_substrates.items():
                        sync_data = self._create_substrate_sync(substrate)
                        if sync_data:
                            self.sync_queue.append(sync_data)
                    
                    # Process sync queue
                    await self._process_sync_queue()
                    
                    time.sleep(5)  # Sync every 5 seconds
                    
                except Exception as e:
                    self.logger.error(f"Background sync error: {e}")
        
        self.sync_thread = threading.Thread(target=sync_loop, daemon=True)
        self.sync_thread.start()
        self.logger.info("🔄 Started background substrate synchronization")
    
    def _create_substrate_sync(self, substrate: SecureSubstrate) -> Optional[SubstrateSync]:
        """Create substrate sync data"""
        try:
            verification = substrate.verify_integrity()
            
            return SubstrateSync(
                substrate_id=substrate.definition.id,
                fibonacci_level=substrate.definition.fibonacci_level,
                checksum=verification['checksum'],
                data_hash=verification.get('sha256', ''),
                timestamp=time.time(),
                package_data=substrate.export_secure_package()
            )
        except Exception as e:
            self.logger.error(f"Failed to create sync data: {e}")
            return None
    
    async def _process_sync_queue(self):
        """Process substrate synchronization queue"""
        while self.sync_queue:
            sync_data = self.sync_queue.pop(0)
            
            # Broadcast to connected nodes
            message = {
                'type': 'substrate_sync',
                'sync_data': sync_data.__dict__
            }
            
            for node_id in self.connected_nodes:
                await self._send_message(node_id, message)
    
    def start(self):
        """Start the server in background"""
        def run_server():
            asyncio.run(self.start_server())
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Start background sync
        self.start_background_sync()
        
        self.logger.info("🚀 ButterflyFX Server started in background")
    
    def stop(self):
        """Stop the server"""
        self.running = False
        
        # Close server socket
        if self.server_socket:
            self.server_socket.close()
        
        # Cancel connection handlers
        for handler in self.connection_handlers.values():
            handler.cancel()
        
        self.logger.info("🛑 ButterflyFX Server stopped")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        return {
            'node_id': self.node_id,
            'host': self.host,
            'port': self.port,
            'network_mode': self.network_mode.value,
            'connected_nodes': len(self.connected_nodes),
            'shared_substrates': len(self.shared_substrates),
            'fibonacci_level': 0,  # Current node level
            'pending_connections': len(self.pending_connections),
            'game_players': len(self.game_players) if self.network_mode == NetworkMode.GAME_SERVER else 0,
            'uptime': time.time() - getattr(self, 'start_time', time.time())
        }


# Convenience functions for quick server setup
def create_game_server(port: int = 8894, host: str = "localhost") -> ButterflyServer:
    """Create a ButterflyFX game server"""
    server = ButterflyServer(
        host=host,
        port=port,
        network_mode=NetworkMode.GAME_SERVER,
        security_level=SecurityLevel.STANDARD
    )
    
    # Create game substrate
    server.create_shared_substrate("game_world", fibonacci_level=3)  # ORGANIZE level
    
    return server


def create_closed_network(port: int = 8895, host: str = "localhost") -> ButterflyServer:
    """Create a closed ButterflyFX network"""
    server = ButterflyServer(
        host=host,
        port=port,
        network_mode=NetworkMode.CLOSED,
        security_level=SecurityLevel.PARANOID
    )
    
    return server


def create_open_network(port: int = 8893, host: str = "localhost") -> ButterflyServer:
    """Create an open ButterflyFX network"""
    server = ButterflyServer(
        host=host,
        port=port,
        network_mode=NetworkMode.OPEN,
        security_level=SecurityLevel.STANDARD
    )
    
    return server


__all__ = [
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
    'create_open_network'
]
