"""
Basic ButterflyFX Network Example
=================================

Demonstrates setting up a simple P2P network with:
- Multiple nodes connecting to each other
- Substrate sharing and synchronization
- Fibonacci-based networking protocols
- Consent-based connections

Run multiple instances of this script with different ports to see
the P2P networking in action.
"""

import asyncio
import time
import logging
from server import create_open_network, FibonacciDiscovery, NetworkMode

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def main():
    """Main example function"""
    # Get configuration from user
    print("🦋 ButterflyFX Basic Network Example")
    print("=" * 50)
    
    host = input("Enter host (default: localhost): ").strip() or "localhost"
    port = int(input("Enter port (default: 8893): ").strip() or "8893")
    node_name = input("Enter node name (default: Node1): ").strip() or "Node1"
    
    print(f"\n🚀 Starting {node_name} on {host}:{port}")
    
    # Create network server
    network = create_open_network(host=host, port=port)
    network.start()
    
    # Create node discovery
    from server.node_discovery import create_discovery
    discovery = create_discovery(
        node_id=f"{node_name}_{port}",
        host=host,
        port=port,
        network_mode=NetworkMode.OPEN
    )
    
    # Add discovery callback
    def on_node_discovered(node_info):
        print(f"🔍 Discovered new node: {node_info.node_id} at {node_info.host}:{node_info.port}")
        
        # Try to connect to discovered node
        asyncio.create_task(connect_to_node(network, node_info))
    
    discovery.add_discovery_callback(on_node_discovered)
    
    # Start discovery
    discovery.start_discovery()
    
    # Create a shared substrate
    substrate_id = f"{node_name}_substrate"
    network.create_shared_substrate(substrate_id, fibonacci_level=2)
    print(f"📐 Created shared substrate: {substrate_id}")
    
    # Start interactive console
    print("\n📝 Commands:")
    print("  connect <host> <port> - Connect to another node")
    print("  advance <substrate_id> <level> - Advance substrate level")
    print("  status - Show network status")
    print("  quit - Exit")
    print()
    
    try:
        while True:
            command = input(f"{node_name}> ").strip()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == "quit":
                break
            elif cmd == "connect" and len(parts) >= 3:
                target_host = parts[1]
                target_port = int(parts[2])
                
                print(f"🔗 Connecting to {target_host}:{target_port}...")
                success = await network.connect_to_node(target_host, target_port)
                if success:
                    print(f"✅ Connected to {target_host}:{target_port}")
                else:
                    print(f"❌ Failed to connect to {target_host}:{target_port}")
            
            elif cmd == "advance" and len(parts) >= 3:
                substrate_id = parts[1]
                target_level = int(parts[2])
                
                print(f"🌀 Advancing {substrate_id} to level {target_level}...")
                success = network.advance_shared_substrate(substrate_id, target_level)
                if success:
                    print(f"✅ Advanced {substrate_id} to level {target_level}")
                else:
                    print(f"❌ Failed to advance {substrate_id}")
            
            elif cmd == "status":
                status = network.get_network_status()
                print(f"\n📊 Network Status:")
                print(f"  Node ID: {status['node_id']}")
                print(f"  Connected Nodes: {status['connected_nodes']}")
                print(f"  Shared Substrates: {status['shared_substrates']}")
                print(f"  Pending Connections: {status['pending_connections']}")
                
                discovery_status = discovery.get_discovery_status()
                print(f"  Discovery Active: {discovery_status['active']}")
                print(f"  Discovery Phase: {discovery_status['phase']}")
                print(f"  Discovered Nodes: {discovery_status['discovered_nodes']}")
            
            else:
                print("❌ Unknown command. Try: connect, advance, status, quit")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    finally:
        # Cleanup
        discovery.stop_discovery()
        network.stop()


async def connect_to_node(network, node_info):
    """Connect to a discovered node"""
    try:
        success = await network.connect_to_node(node_info.host, node_info.port)
        if success:
            print(f"✅ Auto-connected to {node_info.node_id}")
        else:
            print(f"❌ Failed to auto-connect to {node_info.node_id}")
    except Exception as e:
        print(f"❌ Error connecting to {node_info.node_id}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
