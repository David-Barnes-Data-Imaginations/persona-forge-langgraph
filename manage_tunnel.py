#!/usr/bin/env python3
"""
Manage SSH tunnel to mini-itx for remote Ollama access

Usage:
    python manage_tunnel.py start   # Start the tunnel
    python manage_tunnel.py stop    # Stop the tunnel
    python manage_tunnel.py status  # Check tunnel status
"""
import sys
from src.io_py.edge.ssh_tunnel import SSHTunnel
from src.io_py.edge.config import MINI_SSH_CONFIG


def main():
    tunnel = SSHTunnel(
        host=MINI_SSH_CONFIG["host"],
        user=MINI_SSH_CONFIG["user"],
        local_port=MINI_SSH_CONFIG["local_port"],
        remote_port=MINI_SSH_CONFIG["remote_port"]
    )

    if len(sys.argv) < 2:
        print("Usage: python manage_tunnel.py [start|stop|status]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "start":
        tunnel.start()
    elif command == "stop":
        tunnel.stop()
    elif command == "status":
        if tunnel.is_running():
            print(f"✅ SSH tunnel is running on port {MINI_SSH_CONFIG['local_port']}")
            print(f"   Forwarding localhost:{MINI_SSH_CONFIG['local_port']} → {MINI_SSH_CONFIG['host']}:{MINI_SSH_CONFIG['remote_port']}")
        else:
            print(f"❌ SSH tunnel is not running")
            print(f"\nTo start the tunnel, run:")
            print(f"   python manage_tunnel.py start")
            print(f"\nOr manually:")
            print(f"   ssh -N -f -L {MINI_SSH_CONFIG['local_port']}:127.0.0.1:{MINI_SSH_CONFIG['remote_port']} {MINI_SSH_CONFIG['user']}@{MINI_SSH_CONFIG['host']}")
    else:
        print(f"Unknown command: {command}")
        print("Usage: python manage_tunnel.py [start|stop|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
