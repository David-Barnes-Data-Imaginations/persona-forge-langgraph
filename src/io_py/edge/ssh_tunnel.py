"""SSH Tunnel Manager for remote Ollama connections"""
import subprocess
import time
import os
import signal
from typing import Optional


class SSHTunnel:
    """Manages SSH tunnel to mini-itx for remote Ollama access"""

    def __init__(self, host: str, user: str, local_port: int, remote_port: int):
        self.host = host
        self.user = user
        self.local_port = local_port
        self.remote_port = remote_port
        self.process: Optional[subprocess.Popen] = None

    def start(self):
        """Start the SSH tunnel in background"""
        if self.is_running():
            print(f"✅ SSH tunnel already running on port {self.local_port}")
            return

        # Build SSH command: ssh -N -f -L local_port:127.0.0.1:remote_port user@host
        cmd = [
            "ssh",
            "-N",  # No command execution
            "-f",  # Background mode
            "-L", f"{self.local_port}:127.0.0.1:{self.remote_port}",
            f"{self.user}@{self.host}"
        ]

        try:
            print(f"🔌 Starting SSH tunnel to {self.user}@{self.host}...")
            print(f"   Forwarding localhost:{self.local_port} → {self.host}:{self.remote_port}")

            # Start the tunnel
            subprocess.run(cmd, check=True)

            # Wait a moment for tunnel to establish
            time.sleep(1)

            if self.is_running():
                print(f"✅ SSH tunnel established on port {self.local_port}")
            else:
                print(f"⚠️  SSH tunnel may not be running. Check manually with: lsof -i :{self.local_port}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create SSH tunnel: {e}")
            raise

    def is_running(self) -> bool:
        """Check if tunnel is running by checking if port is in use"""
        try:
            result = subprocess.run(
                ["lsof", "-i", f":{self.local_port}"],
                capture_output=True,
                text=True
            )
            return "ssh" in result.stdout.lower()
        except Exception:
            return False

    def stop(self):
        """Stop the SSH tunnel"""
        try:
            # Find and kill SSH processes using this port
            result = subprocess.run(
                ["lsof", "-ti", f":{self.local_port}"],
                capture_output=True,
                text=True
            )

            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"✅ Stopped SSH tunnel (PID: {pid})")
        except Exception as e:
            print(f"⚠️  Error stopping tunnel: {e}")

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # Don't stop the tunnel on exit - keep it running for future use
        pass


# Global tunnel instance
_mini_tunnel: Optional[SSHTunnel] = None


def ensure_mini_tunnel():
    """Ensure SSH tunnel to mini-itx is running"""
    global _mini_tunnel

    from .config import MINI_SSH_CONFIG

    if _mini_tunnel is None:
        _mini_tunnel = SSHTunnel(
            host=MINI_SSH_CONFIG["host"],
            user=MINI_SSH_CONFIG["user"],
            local_port=MINI_SSH_CONFIG["local_port"],
            remote_port=MINI_SSH_CONFIG["remote_port"]
        )

    _mini_tunnel.start()
    return _mini_tunnel


def stop_mini_tunnel():
    """Stop the mini-itx SSH tunnel"""
    global _mini_tunnel
    if _mini_tunnel:
        _mini_tunnel.stop()
        _mini_tunnel = None
