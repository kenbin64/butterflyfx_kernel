"""
ButterflyFX Game Server Demo
============================

Demonstrates the game server capabilities with:
- Multiplayer arena game
- Real-time substrate state synchronization
- Fibonacci-based game mechanics
- Player management and scoring

Run the server first, then connect multiple clients to see the multiplayer functionality.
"""

import asyncio
import time
import logging
import random
import math
from server import create_arena_server, GameType

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ArenaGame:
    """Simple arena game implementation"""
    
    def __init__(self, game_server):
        self.server = game_server
        self.game_loop_task = None
        self.running = False
        
    async def start(self):
        """Start the arena game"""
        print("🎮 Starting Arena Game Demo")
        print("=" * 50)
        
        # Create game world
        await self.server.create_game_world(
            world_id="demo_arena",
            name="Demo Arena",
            description="A simple arena for testing",
            max_players=10,
            game_rules={
                "respawn_time": 5.0,
                "max_health": 100,
                "damage_per_hit": 10,
                "score_per_kill": 100
            }
        )
        
        # Start game loop
        self.running = True
        self.game_loop_task = asyncio.create_task(self.game_loop())
        
        print("✅ Arena game started!")
        print("\n📝 Game Commands:")
        print("  add_player <player_id> <username> - Add a player")
        print("  move <player_id> <x> <y> <z> - Move player")
        print("  attack <attacker> <target> - Attack another player")
        print("  status - Show game status")
        print("  simulate - Simulate some game activity")
        print("  quit - Stop game")
        print()
    
    async def game_loop(self):
        """Main game loop"""
        while self.running:
            try:
                # Spawn power-ups (Fibonacci-based spawning)
                if random.random() < 0.1:  # 10% chance per tick
                    await self.spawn_powerup()
                
                # Check for idle players
                await self.check_idle_players()
                
                # Update game state
                await self.update_game_state()
                
                await asyncio.sleep(1.0)  # 1 FPS for demo
                
            except Exception as e:
                print(f"Game loop error: {e}")
                await asyncio.sleep(1.0)
    
    async def spawn_powerup(self):
        """Spawn power-ups using Fibonacci pattern"""
        # Use Fibonacci sequence for power-up positions
        fib_positions = [
            (0, 0, 0),           # F0
            (1, 1, 1),           # F1
            (2, 2, 2),           # F2
            (3, 3, 3),           # F3
            (5, 5, 5),           # F4
            (8, 8, 8),           # F5
            (13, 13, 13),        # F6
        ]
        
        if fib_positions:
            pos = random.choice(fib_positions)
            # Add some randomness
            x = pos[0] + random.uniform(-10, 10)
            y = pos[1] + random.uniform(-10, 10)
            z = pos[2]
            
            print(f"💎 Spawned power-up at ({x:.1f}, {y:.1f}, {z:.1f})")
            
            # Broadcast power-up spawn
            await self.server._broadcast_game_event("demo_arena", {
                "type": "powerup_spawned",
                "position": (x, y, z),
                "powerup_type": random.choice(["health", "speed", "damage"])
            })
    
    async def check_idle_players(self):
        """Check for idle players and respawn if needed"""
        current_time = time.time()
        
        for player_id, player in self.server.players.items():
            if player.state.value == "playing":
                # Check if player has been inactive
                if current_time - player.last_update > 30.0:  # 30 seconds idle
                    print(f"⏰ Player {player.username} is idle, respawning...")
                    
                    # Respawn player
                    new_pos = (
                        random.uniform(-50, 50),
                        random.uniform(-50, 50),
                        0.0
                    )
                    
                    await self.server.update_player_state(
                        player_id,
                        position=new_pos,
                        health=100.0
                    )
                    
                    await self.server._broadcast_game_event("demo_arena", {
                        "type": "player_respawned",
                        "player_id": player_id,
                        "position": new_pos
                    })
    
    async def update_game_state(self):
        """Update overall game state"""
        # Update world substrate based on game activity
        if "demo_arena" in self.server.world_substrates:
            substrate = self.server.world_substrates["demo_arena"]
            
            # Advance substrate based on player activity
            active_players = len([p for p in self.server.players.values() if p.state.value == "playing"])
            
            if active_players > 0 and active_players % 3 == 0:  # Every 3 active players
                current_level = substrate.definition.fibonacci_level
                if current_level < 8:
                    advanced = substrate.advance_fibonacci_level(current_level + 1)
                    self.server.world_substrates["demo_arena"] = advanced
                    
                    print(f"🌍 Game world advanced to Fibonacci level {current_level + 1}")
    
    async def add_player(self, player_id: str, username: str):
        """Add a player to the game"""
        success = await self.server.add_player(
            player_id=player_id,
            node_id=f"node_{player_id}",
            username=username,
            world_id="demo_arena"
        )
        
        if success:
            # Set initial position
            start_pos = (
                random.uniform(-30, 30),
                random.uniform(-30, 30),
                0.0
            )
            
            await self.server.update_player_state(
                player_id,
                position=start_pos,
                health=100.0,
                score=0
            )
            
            print(f"✅ Added player: {username} at {start_pos}")
        else:
            print(f"❌ Failed to add player: {username}")
    
    async def move_player(self, player_id: str, x: float, y: float, z: float):
        """Move player to new position"""
        success = await self.server.update_player_state(
            player_id,
            position=(x, y, z)
        )
        
        if success:
            player = self.server.players.get(player_id)
            if player:
                print(f"🏃 Moved {player.username} to ({x:.1f}, {y:.1f}, {z:.1f})")
        else:
            print(f"❌ Failed to move player: {player_id}")
    
    async def attack_player(self, attacker_id: str, target_id: str):
        """Process attack action"""
        success = await self.server.process_game_action(
            attacker_id,
            "attack",
            {
                "target_id": target_id,
                "damage": 15
            }
        )
        
        if success:
            attacker = self.server.players.get(attacker_id)
            target = self.server.players.get(target_id)
            
            if attacker and target:
                print(f"⚔️ {attacker.username} attacked {target.username} (HP: {target.health:.1f})")
        else:
            print(f"❌ Failed attack: {attacker_id} -> {target_id}")
    
    async def simulate_activity(self):
        """Simulate some game activity"""
        print("🎲 Simulating game activity...")
        
        players = list(self.server.players.values())
        if len(players) < 2:
            print("❌ Need at least 2 players for simulation")
            return
        
        # Random movements
        for player in random.sample(players, min(3, len(players))):
            if player.state.value == "playing":
                new_x = player.position[0] + random.uniform(-10, 10)
                new_y = player.position[1] + random.uniform(-10, 10)
                new_z = 0.0
                
                await self.move_player(player.player_id, new_x, new_y, new_z)
        
        # Random attacks
        if len(players) >= 2:
            attackers = [p for p in players if p.state.value == "playing" and p.health > 0]
            targets = [p for p in players if p.state.value == "playing" and p.health > 0]
            
            if len(attackers) >= 1 and len(targets) >= 2:
                attacker = random.choice(attackers)
                possible_targets = [t for t in targets if t.player_id != attacker.player_id]
                
                if possible_targets:
                    target = random.choice(possible_targets)
                    await self.attack_player(attacker.player_id, target.player_id)
    
    def show_status(self):
        """Show current game status"""
        status = self.server.get_server_status()
        
        print("\n📊 Game Status:")
        print(f"  Total Players: {status['player_stats']['total_players']}")
        print(f"  Active Players: {status['player_stats']['current_online']}")
        print(f"  Fibonacci Tick: {status['fibonacci_info']['current_tick']}")
        
        world_info = self.server.get_world_info("demo_arena")
        if world_info:
            print(f"\n🌍 Demo Arena:")
            print(f"  Players: {world_info['world_info']['current_players']}/{world_info['world_info']['max_players']}")
            print(f"  Fibonacci Level: {world_info['world_info']['fibonacci_level']}")
            
            print("\n👥 Players:")
            for player in world_info['players']:
                print(f"  {player['username']}: HP={player['health']:.1f}, Score={player['score']}, Level={player['fibonacci_level']}")
    
    async def stop(self):
        """Stop the game"""
        self.running = False
        if self.game_loop_task:
            self.game_loop_task.cancel()
        
        await self.server.shutdown()
        print("🛑 Game stopped")


async def main():
    """Main demo function"""
    print("🦋 ButterflyFX Game Server Demo")
    print("=" * 50)
    
    # Get configuration
    host = input("Enter host (default: localhost): ").strip() or "localhost"
    port = int(input("Enter port (default: 8894): ").strip() or "8894")
    
    print(f"\n🚀 Starting game server on {host}:{port}")
    
    # Create game server
    server = create_arena_server(host=host, port=port)
    await server.start()
    
    # Create and start arena game
    game = ArenaGame(server)
    await game.start()
    
    try:
        while True:
            command = input("arena> ").strip()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == "quit":
                break
            elif cmd == "add_player" and len(parts) >= 3:
                player_id = parts[1]
                username = parts[2]
                await game.add_player(player_id, username)
            
            elif cmd == "move" and len(parts) >= 5:
                player_id = parts[1]
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4])
                await game.move_player(player_id, x, y, z)
            
            elif cmd == "attack" and len(parts) >= 3:
                attacker = parts[1]
                target = parts[2]
                await game.attack_player(attacker, target)
            
            elif cmd == "status":
                game.show_status()
            
            elif cmd == "simulate":
                await game.simulate_activity()
            
            else:
                print("❌ Unknown command. Try: add_player, move, attack, status, simulate, quit")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    finally:
        await game.stop()


if __name__ == "__main__":
    asyncio.run(main())
