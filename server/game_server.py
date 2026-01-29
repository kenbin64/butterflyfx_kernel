"""
ButterflyFX Game Server - Substrate-Based Multiplayer Gaming
============================================================

A game server built on ButterflyFX substrate architecture:
- Real-time substrate state synchronization
- Fibonacci-based game mechanics
- Player management with consent-based connections
- Scalable serverless architecture
- Cross-platform game state persistence

Game Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    Game World Substrate                      │
│  z = x * y² where:                                          │
│  x = player position/identity                              │
│  y = game state transformation                              │
│  z = completed game state artifact                          │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼───────┐   ┌───────▼───────┐
            │ Player Nodes  │   │   Game State  │
            │ (Substrates)  │   │ (Substrate)   │
            └───────────────┘   └───────────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Fibonacci Sync   │
                    │  ● → ↑ ← ↓ → ↑ ∞ │
                    └───────────────────┘

Features:
- Real-time multiplayer with substrate state sync
- Fibonacci-based game mechanics and progression
- Player consent and privacy controls
- Serverless scaling with P2P networking
- Persistent game state through substrates
- Cross-platform compatibility
"""

from __future__ import annotations
import asyncio
import json
import time
import math
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

from .butterfly_server import ButterflyServer, NetworkMode, NodeInfo
from core import SecureSubstrate, create_canonical_substrate, SecurityLevel
from core.fibonacci_directional_levels import Direction, Operation, is_multiplication_level


class GameType(Enum):
    """Supported game types"""
    ARENA = "arena"           # Combat arena
    STRATEGY = "strategy"     # Strategy game
    PUZZLE = "puzzle"        # Puzzle game
    SIMULATION = "simulation" # Simulation game
    SOCIAL = "social"        # Social space
    RACING = "racing"        # Racing game


class PlayerState(Enum):
    """Player connection states"""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    PLAYING = "playing"
    SPECTATING = "spectating"
    DISCONNECTED = "disconnected"


@dataclass
class Player:
    """Game player with substrate-based state"""
    player_id: str
    node_id: str  # Network node ID
    username: str
    game_type: GameType
    fibonacci_level: int = 0
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    score: int = 0
    health: float = 100.0
    state: PlayerState = PlayerState.CONNECTING
    joined_at: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    substrate_id: str = ""  # Player's personal substrate
    permissions: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GameWorld:
    """Game world represented as a substrate"""
    world_id: str
    game_type: GameType
    name: str
    description: str
    max_players: int
    current_players: int = 0
    fibonacci_level: int = 3  # Start at ORGANIZE level
    world_bounds: Tuple[float, float, float, float] = (-100.0, 100.0, -100.0, 100.0)
    game_rules: Dict[str, Any] = field(default_factory=dict)
    substrate_id: str = ""
    created_at: float = field(default_factory=time.time)
    active: bool = True


@dataclass
class GameEvent:
    """Game event for state changes"""
    event_id: str
    world_id: str
    player_id: str
    event_type: str
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    fibonacci_sequence: List[int] = field(default_factory=list)


class ButterflyGameServer:
    """
    ButterflyFX-based game server with substrate architecture
    """
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 8894,
                 game_type: GameType = GameType.ARENA,
                 max_worlds: int = 10):
        """
        Initialize game server
        
        Args:
            host: Server host address
            port: Server port
            game_type: Primary game type
            max_worlds: Maximum number of game worlds
        """
        self.host = host
        self.port = port
        self.game_type = game_type
        self.max_worlds = max_worlds
        
        # Core server
        self.server = ButterflyServer(
            host=host,
            port=port,
            network_mode=NetworkMode.GAME_SERVER,
            security_level=SecurityLevel.STANDARD
        )
        
        # Game state
        self.players: Dict[str, Player] = {}
        self.game_worlds: Dict[str, GameWorld] = {}
        self.game_events: List[GameEvent] = []
        self.active_matches: Dict[str, Set[str]] = {}  # world_id -> player_ids
        
        # Substrate management
        self.world_substrates: Dict[str, SecureSubstrate] = {}
        self.player_substrates: Dict[str, SecureSubstrate] = {}
        
        # Game mechanics
        self.game_loops: Dict[str, asyncio.Task] = {}
        self.fibonacci_tick = 0  # Current Fibonacci tick for game updates
        
        # Logging
        self.logger = logging.getLogger(f"ButterflyGameServer-{host}:{port}")
        self.logger.setLevel(logging.INFO)
        
        # Performance tracking
        self.stats = {
            'total_players': 0,
            'active_players': 0,
            'total_events': 0,
            'avg_latency': 0.0,
            'substrate_syncs': 0
        }
    
    async def start(self):
        """Start the game server"""
        self.logger.info(f"🎮 Starting ButterflyFX Game Server: {self.game_type.value}")
        
        # Start base server
        self.server.start()
        
        # Create default game world
        await self.create_game_world(
            world_id="default_arena",
            name="Default Arena",
            description="Default game arena for all players",
            max_players=20
        )
        
        # Start game loops
        await self._start_game_loops()
        
        self.logger.info("✅ Game server started successfully")
    
    async def create_game_world(self, 
                               world_id: str,
                               name: str,
                               description: str,
                               max_players: int = 10,
                               game_rules: Dict[str, Any] = None) -> str:
        """
        Create a new game world
        
        Args:
            world_id: Unique world identifier
            name: World display name
            description: World description
            max_players: Maximum player capacity
            game_rules: Game-specific rules
        
        Returns:
            Created world ID
        """
        if len(self.game_worlds) >= self.max_worlds:
            raise ValueError("Maximum number of worlds reached")
        
        if world_id in self.game_worlds:
            raise ValueError(f"World {world_id} already exists")
        
        # Create game world
        world = GameWorld(
            world_id=world_id,
            game_type=self.game_type,
            name=name,
            description=description,
            max_players=max_players,
            game_rules=game_rules or {}
        )
        
        # Create world substrate
        world_substrate = create_canonical_substrate(
            f"world_{world_id}",
            fibonacci_level=world.fibonacci_level,
            security_level=SecurityLevel.STANDARD
        )
        
        self.world_substrates[world_id] = world_substrate
        world.substrate_id = f"world_{world_id}"
        
        # Store world
        self.game_worlds[world_id] = world
        self.active_matches[world_id] = set()
        
        # Make world substrate shareable
        self.server.create_shared_substrate(world.substrate_id, world.fibonacci_level)
        
        self.logger.info(f"🌍 Created game world: {world_id} ({name})")
        
        return world_id
    
    async def add_player(self, 
                        player_id: str,
                        node_id: str,
                        username: str,
                        world_id: str = "default_arena",
                        permissions: Set[str] = None) -> bool:
        """
        Add a player to the game server
        
        Args:
            player_id: Unique player identifier
            node_id: Network node ID
            username: Player username
            world_id: World to join
            permissions: Player permissions
        
        Returns:
            True if player added successfully
        """
        if world_id not in self.game_worlds:
            self.logger.error(f"World {world_id} not found")
            return False
        
        world = self.game_worlds[world_id]
        
        if world.current_players >= world.max_players:
            self.logger.warning(f"World {world_id} is full")
            return False
        
        if player_id in self.players:
            self.logger.warning(f"Player {player_id} already exists")
            return False
        
        # Create player
        player = Player(
            player_id=player_id,
            node_id=node_id,
            username=username,
            game_type=self.game_type,
            permissions=permissions or set(),
            substrate_id=f"player_{player_id}"
        )
        
        # Create player substrate
        player_substrate = create_canonical_substrate(
            player.substrate_id,
            fibonacci_level=player.fibonacci_level,
            security_level=SecurityLevel.STANDARD
        )
        
        self.player_substrates[player_id] = player_substrate
        
        # Add to world
        self.players[player_id] = player
        self.active_matches[world_id].add(player_id)
        world.current_players += 1
        player.state = PlayerState.CONNECTED
        
        # Make player substrate shareable
        self.server.create_shared_substrate(player.substrate_id, player.fibonacci_level)
        
        # Create game event
        await self._create_game_event(
            world_id=world_id,
            player_id=player_id,
            event_type="player_joined",
            data={"username": username, "position": player.position}
        )
        
        # Update stats
        self.stats['total_players'] += 1
        self.stats['active_players'] += 1
        
        self.logger.info(f"👤 Added player: {username} ({player_id}) to {world_id}")
        
        return True
    
    async def remove_player(self, player_id: str) -> bool:
        """
        Remove a player from the game server
        
        Args:
            player_id: Player to remove
        
        Returns:
            True if player removed successfully
        """
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        
        # Find player's world
        world_id = None
        for wid, players in self.active_matches.items():
            if player_id in players:
                world_id = wid
                break
        
        # Remove from world
        if world_id:
            self.active_matches[world_id].remove(player_id)
            self.game_worlds[world_id].current_players -= 1
            
            # Create game event
            await self._create_game_event(
                world_id=world_id,
                player_id=player_id,
                event_type="player_left",
                data={"username": player.username, "reason": "disconnect"}
            )
        
        # Clean up player
        player.state = PlayerState.DISCONNECTED
        del self.players[player_id]
        
        if player_id in self.player_substrates:
            del self.player_substrates[player_id]
        
        # Update stats
        self.stats['active_players'] -= 1
        
        self.logger.info(f"👋 Removed player: {player.username} ({player_id})")
        
        return True
    
    async def update_player_state(self, 
                                player_id: str,
                                position: Tuple[float, float, float] = None,
                                velocity: Tuple[float, float, float] = None,
                                health: float = None,
                                score: int = None) -> bool:
        """
        Update player state
        
        Args:
            player_id: Player to update
            position: New position (x, y, z)
            velocity: New velocity (vx, vy, vz)
            health: New health value
            score: New score
        
        Returns:
            True if update successful
        """
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        
        # Update player state
        if position:
            player.position = position
        if velocity:
            player.velocity = velocity
        if health is not None:
            player.health = health
        if score is not None:
            player.score = score
        
        player.last_update = time.time()
        
        # Update player substrate
        if player_id in self.player_substrates:
            substrate = self.player_substrates[player_id]
            # Advance substrate based on player actions
            if player.score > 0 and player.score % 100 == 0:
                # Level up every 100 points
                new_level = min(player.fibonacci_level + 1, 8)
                if new_level != player.fibonacci_level:
                    advanced = substrate.advance_fibonacci_level(new_level)
                    self.player_substrates[player_id] = advanced
                    player.fibonacci_level = new_level
                    
                    self.logger.info(f"⬆️ Player {player.username} advanced to Fibonacci level {new_level}")
        
        # Broadcast update to other players in same world
        await self._broadcast_player_update(player_id)
        
        return True
    
    async def process_game_action(self, 
                                player_id: str,
                                action_type: str,
                                action_data: Dict[str, Any]) -> bool:
        """
        Process player game action
        
        Args:
            player_id: Acting player
            action_type: Type of action
            action_data: Action-specific data
        
        Returns:
            True if action processed successfully
        """
        if player_id not in self.players:
            return False
        
        player = self.players[player_id]
        
        # Find player's world
        world_id = None
        for wid, players in self.active_matches.items():
            if player_id in players:
                world_id = wid
                break
        
        if not world_id:
            return False
        
        # Process action based on game type
        success = await self._process_action_by_game_type(
            world_id, player_id, action_type, action_data
        )
        
        if success:
            # Create game event
            await self._create_game_event(
                world_id=world_id,
                player_id=player_id,
                event_type=action_type,
                data=action_data
            )
        
        return success
    
    async def _process_action_by_game_type(self, 
                                          world_id: str,
                                          player_id: str,
                                          action_type: str,
                                          action_data: Dict[str, Any]) -> bool:
        """Process action based on game type"""
        if self.game_type == GameType.ARENA:
            return await self._process_arena_action(world_id, player_id, action_type, action_data)
        elif self.game_type == GameType.STRATEGY:
            return await self._process_strategy_action(world_id, player_id, action_type, action_data)
        elif self.game_type == GameType.PUZZLE:
            return await self._process_puzzle_action(world_id, player_id, action_type, action_data)
        elif self.game_type == GameType.SIMULATION:
            return await self._process_simulation_action(world_id, player_id, action_type, action_data)
        elif self.game_type == GameType.SOCIAL:
            return await self._process_social_action(world_id, player_id, action_type, action_data)
        elif self.game_type == GameType.RACING:
            return await self._process_racing_action(world_id, player_id, action_type, action_data)
        
        return False
    
    async def _process_arena_action(self, 
                                  world_id: str,
                                  player_id: str,
                                  action_type: str,
                                  action_data: Dict[str, Any]) -> bool:
        """Process arena game action"""
        if action_type == "attack":
            # Process attack action
            target_id = action_data.get("target_id")
            damage = action_data.get("damage", 10)
            
            if target_id and target_id in self.players:
                target = self.players[target_id]
                target.health = max(0, target.health - damage)
                
                # Broadcast damage event
                await self._broadcast_game_event(world_id, {
                    "type": "player_damaged",
                    "attacker": player_id,
                    "target": target_id,
                    "damage": damage,
                    "new_health": target.health
                })
                
                return True
        
        elif action_type == "move":
            # Process movement action
            new_position = action_data.get("position")
            if new_position:
                await self.update_player_state(player_id, position=new_position)
                return True
        
        return False
    
    async def _process_strategy_action(self, 
                                     world_id: str,
                                     player_id: str,
                                     action_type: str,
                                     action_data: Dict[str, Any]) -> bool:
        """Process strategy game action"""
        # Implementation for strategy games
        if action_type == "build_unit":
            # Process unit building
            unit_type = action_data.get("unit_type")
            position = action_data.get("position")
            
            # Update world substrate with new unit
            if world_id in self.world_substrates:
                substrate = self.world_substrates[world_id]
                # Advance substrate for strategic development
                if is_multiplication_level(substrate.definition.fibonacci_level):
                    # Expand territory (horizontal operation)
                    new_level = min(substrate.definition.fibonacci_level + 1, 8)
                    advanced = substrate.advance_fibonacci_level(new_level)
                    self.world_substrates[world_id] = advanced
                    
                    self.logger.info(f"🏗️ World {world_id} expanded to Fibonacci level {new_level}")
            
            return True
        
        return False
    
    async def _process_puzzle_action(self, 
                                    world_id: str,
                                    player_id: str,
                                    action_type: str,
                                    action_data: Dict[str, Any]) -> bool:
        """Process puzzle game action"""
        # Implementation for puzzle games
        if action_type == "solve_piece":
            # Process puzzle piece solution
            piece_id = action_data.get("piece_id")
            solution = action_data.get("solution")
            
            # Update player score
            player = self.players[player_id]
            player.score += 10
            
            # Check for Fibonacci pattern in solution
            if self._check_fibonacci_pattern(solution):
                player.score += 50  # Bonus for Fibonacci pattern
                
                self.logger.info(f"🧩 Player {player.username} found Fibonacci pattern!")
            
            await self.update_player_state(player_id, score=player.score)
            return True
        
        return False
    
    async def _process_simulation_action(self, 
                                       world_id: str,
                                       player_id: str,
                                       action_type: str,
                                       action_data: Dict[str, Any]) -> bool:
        """Process simulation game action"""
        # Implementation for simulation games
        return True
    
    async def _process_social_action(self, 
                                   world_id: str,
                                   player_id: str,
                                   action_type: str,
                                   action_data: Dict[str, Any]) -> bool:
        """Process social game action"""
        # Implementation for social games
        if action_type == "chat":
            # Process chat message
            message = action_data.get("message", "")
            
            # Broadcast chat to world
            await self._broadcast_game_event(world_id, {
                "type": "chat_message",
                "player_id": player_id,
                "username": self.players[player_id].username,
                "message": message
            })
            
            return True
        
        return False
    
    async def _process_racing_action(self, 
                                   world_id: str,
                                   player_id: str,
                                   action_type: str,
                                   action_data: Dict[str, Any]) -> bool:
        """Process racing game action"""
        # Implementation for racing games
        if action_type == "update_position":
            # Process racing position update
            position = action_data.get("position")
            lap_time = action_data.get("lap_time")
            
            if position:
                await self.update_player_state(player_id, position=position)
            
            # Check lap completion
            if lap_time and self._check_lap_completion(player_id, lap_time):
                player = self.players[player_id]
                player.score += 100
                
                self.logger.info(f"🏁 Player {player.username} completed lap!")
            
            return True
        
        return False
    
    def _check_fibonacci_pattern(self, solution: Any) -> bool:
        """Check if solution contains Fibonacci pattern"""
        # Simple Fibonacci pattern detection
        if isinstance(solution, list) and len(solution) >= 3:
            for i in range(2, len(solution)):
                if solution[i] == solution[i-1] + solution[i-2]:
                    return True
        return False
    
    def _check_lap_completion(self, player_id: str, lap_time: float) -> bool:
        """Check if player completed a lap"""
        # Simple lap completion check
        # In real implementation, would track checkpoints
        return lap_time > 0 and lap_time < 300  # Complete lap within 5 minutes
    
    async def _create_game_event(self, 
                                world_id: str,
                                player_id: str,
                                event_type: str,
                                data: Dict[str, Any]):
        """Create a game event"""
        event = GameEvent(
            event_id=f"{world_id}_{player_id}_{int(time.time() * 1000)}",
            world_id=world_id,
            player_id=player_id,
            event_type=event_type,
            data=data,
            fibonacci_sequence=self._get_fibonacci_sequence()
        )
        
        self.game_events.append(event)
        self.stats['total_events'] += 1
        
        # Keep only recent events (last 1000)
        if len(self.game_events) > 1000:
            self.game_events = self.game_events[-1000:]
    
    def _get_fibonacci_sequence(self) -> List[int]:
        """Get current Fibonacci sequence for game tick"""
        # Generate Fibonacci sequence up to current tick
        sequence = [0, 1]
        for i in range(2, min(self.fibonacci_tick + 1, 21)):
            sequence.append(sequence[i-1] + sequence[i-2])
        return sequence
    
    async def _broadcast_player_update(self, player_id: str):
        """Broadcast player update to other players"""
        player = self.players[player_id]
        
        # Find player's world
        world_id = None
        for wid, players in self.active_matches.items():
            if player_id in players:
                world_id = wid
                break
        
        if world_id:
            update_data = {
                "type": "player_update",
                "player_id": player_id,
                "username": player.username,
                "position": player.position,
                "velocity": player.velocity,
                "health": player.health,
                "score": player.score,
                "fibonacci_level": player.fibonacci_level
            }
            
            await self._broadcast_game_event(world_id, update_data)
    
    async def _broadcast_game_event(self, world_id: str, event_data: Dict[str, Any]):
        """Broadcast game event to all players in world"""
        if world_id not in self.active_matches:
            return
        
        message = {
            "type": "game_event",
            "world_id": world_id,
            "event_data": event_data,
            "timestamp": time.time()
        }
        
        # Send to all connected nodes
        for player_id in self.active_matches[world_id]:
            if player_id in self.players:
                player = self.players[player_id]
                # Send through server's message system
                await self.server._send_message(player.node_id, message)
    
    async def _start_game_loops(self):
        """Start game update loops"""
        # Start main game loop
        self.game_loops["main"] = asyncio.create_task(self._main_game_loop())
        
        # Start substrate sync loop
        self.game_loops["sync"] = asyncio.create_task(self._substrate_sync_loop())
        
        self.logger.info("🔄 Started game loops")
    
    async def _main_game_loop(self):
        """Main game update loop"""
        while True:
            try:
                # Update Fibonacci tick
                self.fibonacci_tick = (self.fibonacci_tick + 1) % 21  # Reset at 21
                
                # Process game logic based on Fibonacci level
                await self._process_fibonacci_tick()
                
                # Update game physics
                await self._update_game_physics()
                
                # Check win conditions
                await self._check_win_conditions()
                
                # Sleep for game tick (60 FPS)
                await asyncio.sleep(1.0 / 60.0)
                
            except Exception as e:
                self.logger.error(f"Game loop error: {e}")
                await asyncio.sleep(1.0)
    
    async def _process_fibonacci_tick(self):
        """Process game logic based on Fibonacci tick"""
        fib_level = self.fibonacci_tick
        
        if is_multiplication_level(fib_level):
            # Horizontal level - expand gameplay
            await self._expand_gameplay()
        else:
            # Vertical level - organize game state
            await self._organize_game_state()
    
    async def _expand_gameplay(self):
        """Expand gameplay (horizontal Fibonacci operation)"""
        # Spawn new resources, expand play area, etc.
        for world_id, world in self.game_worlds.items():
            if world.active and world.current_players > 0:
                # Advance world substrate
                if world_id in self.world_substrates:
                    substrate = self.world_substrates[world_id]
                    new_level = min(substrate.definition.fibonacci_level + 1, 8)
                    if new_level != substrate.definition.fibonacci_level:
                        advanced = substrate.advance_fibonacci_level(new_level)
                        self.world_substrates[world_id] = advanced
                        world.fibonacci_level = new_level
    
    async def _organize_game_state(self):
        """Organize game state (vertical Fibonacci operation)"""
        # Clean up old events, optimize performance, etc.
        if len(self.game_events) > 500:
            self.game_events = self.game_events[-500:]
    
    async def _update_game_physics(self):
        """Update game physics for all players"""
        for player in self.players.values():
            if player.state == PlayerState.PLAYING:
                # Update position based on velocity
                new_pos = (
                    player.position[0] + player.velocity[0] * (1.0 / 60.0),
                    player.position[1] + player.velocity[1] * (1.0 / 60.0),
                    player.position[2] + player.velocity[2] * (1.0 / 60.0)
                )
                
                # Apply world bounds
                for world in self.game_worlds.values():
                    if world.current_players > 0:
                        bounds = world.world_bounds
                        new_pos = (
                            max(bounds[0], min(bounds[1], new_pos[0])),
                            max(bounds[2], min(bounds[3], new_pos[1])),
                            new_pos[2]
                        )
                
                player.position = new_pos
    
    async def _check_win_conditions(self):
        """Check win conditions for all active games"""
        for world_id, world in self.game_worlds.items():
            if not world.active or world.current_players == 0:
                continue
            
            # Check different win conditions based on game type
            if self.game_type == GameType.ARENA:
                await self._check_arena_win_condition(world_id)
            elif self.game_type == GameType.RACING:
                await self._check_racing_win_condition(world_id)
    
    async def _check_arena_win_condition(self, world_id: str):
        """Check arena win condition"""
        alive_players = [
            p for p in self.players.values() 
            if p.health > 0 and p.state == PlayerState.PLAYING
        ]
        
        if len(alive_players) == 1:
            # Winner found
            winner = alive_players[0]
            await self._broadcast_game_event(world_id, {
                "type": "game_over",
                "winner": winner.player_id,
                "username": winner.username,
                "final_score": winner.score
            })
    
    async def _check_racing_win_condition(self, world_id: str):
        """Check racing win condition"""
        # Check if any player completed required laps
        for player in self.players.values():
            if player.score >= 500:  # 5 laps * 100 points each
                await self._broadcast_game_event(world_id, {
                    "type": "race_complete",
                    "winner": player.player_id,
                    "username": player.username,
                    "final_time": player.score
                })
    
    async def _substrate_sync_loop(self):
        """Synchronize substrates across network"""
        while True:
            try:
                # Sync all shared substrates
                for world_id, substrate in self.world_substrates.items():
                    # Create sync data
                    verification = substrate.verify_integrity()
                    
                    sync_data = {
                        "type": "substrate_sync",
                        "world_id": world_id,
                        "fibonacci_level": substrate.definition.fibonacci_level,
                        "checksum": verification['checksum'],
                        "timestamp": time.time()
                    }
                    
                    # Broadcast to all players in world
                    await self._broadcast_game_event(world_id, sync_data)
                
                self.stats['substrate_syncs'] += 1
                
                # Sleep for sync interval (5 seconds)
                await asyncio.sleep(5.0)
                
            except Exception as e:
                self.logger.error(f"Substrate sync error: {e}")
                await asyncio.sleep(5.0)
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get comprehensive server status"""
        return {
            'server_info': {
                'host': self.host,
                'port': self.port,
                'game_type': self.game_type.value,
                'uptime': time.time() - getattr(self, 'start_time', time.time())
            },
            'player_stats': {
                'total_players': self.stats['total_players'],
                'active_players': self.stats['active_players'],
                'current_online': len(self.players)
            },
            'world_stats': {
                'total_worlds': len(self.game_worlds),
                'active_worlds': len([w for w in self.game_worlds.values() if w.active]),
                'total_capacity': sum(w.max_players for w in self.game_worlds.values()),
                'current_occupancy': sum(w.current_players for w in self.game_worlds.values())
            },
            'fibonacci_info': {
                'current_tick': self.fibonacci_tick,
                'substrate_levels': {
                    world_id: sub.definition.fibonacci_level 
                    for world_id, sub in self.world_substrates.items()
                }
            },
            'performance': {
                'total_events': self.stats['total_events'],
                'substrate_syncs': self.stats['substrate_syncs'],
                'avg_latency': self.stats['avg_latency']
            }
        }
    
    def get_world_info(self, world_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific game world"""
        if world_id not in self.game_worlds:
            return None
        
        world = self.game_worlds[world_id]
        players_in_world = [
            {
                'player_id': p.player_id,
                'username': p.username,
                'score': p.score,
                'health': p.health,
                'fibonacci_level': p.fibonacci_level,
                'state': p.state.value
            }
            for p in self.players.values()
            if p.player_id in self.active_matches.get(world_id, set())
        ]
        
        return {
            'world_info': {
                'world_id': world.world_id,
                'name': world.name,
                'description': world.description,
                'game_type': world.game_type.value,
                'max_players': world.max_players,
                'current_players': world.current_players,
                'fibonacci_level': world.fibonacci_level,
                'active': world.active
            },
            'players': players_in_world,
            'substrate_info': {
                'substrate_id': world.substrate_id,
                'fibonacci_level': self.world_substrates.get(world_id, {}).definition.fibonacci_level if world_id in self.world_substrates else 0
            }
        }
    
    async def shutdown(self):
        """Shutdown the game server"""
        self.logger.info("🛑 Shutting down game server")
        
        # Stop game loops
        for task in self.game_loops.values():
            task.cancel()
        
        # Disconnect all players
        for player_id in list(self.players.keys()):
            await self.remove_player(player_id)
        
        # Stop base server
        self.server.stop()
        
        self.logger.info("✅ Game server shutdown complete")


# Convenience functions
def create_arena_server(host: str = "localhost", port: int = 8894) -> ButterflyGameServer:
    """Create an arena game server"""
    return ButterflyGameServer(host=host, port=port, game_type=GameType.ARENA)


def create_strategy_server(host: str = "localhost", port: int = 8895) -> ButterflyGameServer:
    """Create a strategy game server"""
    return ButterflyGameServer(host=host, port=port, game_type=GameType.STRATEGY)


def create_puzzle_server(host: str = "localhost", port: int = 8896) -> ButterflyGameServer:
    """Create a puzzle game server"""
    return ButterflyGameServer(host=host, port=port, game_type=GameType.PUZZLE)


def create_racing_server(host: str = "localhost", port: int = 8897) -> ButterflyGameServer:
    """Create a racing game server"""
    return ButterflyGameServer(host=host, port=port, game_type=GameType.RACING)


__all__ = [
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
