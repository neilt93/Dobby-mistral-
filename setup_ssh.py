#!/usr/bin/env python3
"""
Setup script for SSH connection to H100 GPU server
"""

import os
import sys
import subprocess
import requests
import json

def test_ssh_connection(host, user, port=22, key_path=None):
    """Test SSH connection to the server"""
    try:
        ssh_cmd = [
            "ssh", "-o", "ConnectTimeout=10", 
            "-o", "BatchMode=yes", 
            "-p", str(port), 
            f"{user}@{host}", 
            "echo 'SSH connection successful'"
        ]
        
        if key_path:
            ssh_cmd.extend(["-i", key_path])
        
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            return True, "SSH connection successful"
        else:
            return False, f"SSH connection failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "SSH connection timed out"
    except Exception as e:
        return False, f"SSH connection error: {str(e)}"

def test_ollama_connection(host, user, port=22, ollama_port=11434, key_path=None):
    """Test if Ollama is running on the remote server"""
    try:
        # Create temporary SSH tunnel for testing
        tunnel_cmd = [
            "ssh", "-L", f"11435:localhost:{ollama_port}",
            "-N", "-T", f"{user}@{host}", "-p", str(port)
        ]
        
        if key_path:
            tunnel_cmd.extend(["-i", key_path])
        
        tunnel = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for tunnel to establish
        import time
        time.sleep(3)
        
        # Test Ollama API
        response = requests.get("http://localhost:11435/api/tags", timeout=10)
        tunnel.terminate()
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            return True, f"Ollama is running. Available models: {[m['name'] for m in models]}"
        else:
            return False, f"Ollama API returned status {response.status_code}"
            
    except Exception as e:
        return False, f"Ollama connection error: {str(e)}"

def main():
    print("🔧 H100 GPU Server Setup")
    print("=" * 40)
    
    # Get connection details
    host = input("Enter H100 server hostname/IP: ").strip()
    user = input("Enter SSH username: ").strip()
    port = input("Enter SSH port (default 22): ").strip() or "22"
    ollama_port = input("Enter Ollama port (default 11434): ").strip() or "11434"
    
    # Get SSH key path
    key_path = input("Enter path to SSH private key (or press Enter for default ~/.ssh/id_rsa): ").strip()
    if not key_path:
        # Use default key location
        import os
        if os.name == 'nt':  # Windows
            key_path = os.path.expanduser("~/.ssh/id_rsa")
        else:  # Unix/Linux/Mac
            key_path = os.path.expanduser("~/.ssh/id_rsa")
    
    print(f"\n🔍 Testing connection to {user}@{host}:{port}...")
    
    # Test SSH connection
    ssh_success, ssh_msg = test_ssh_connection(host, user, int(port), key_path)
    if ssh_success:
        print(f"✅ {ssh_msg}")
    else:
        print(f"❌ {ssh_msg}")
        print("\nPlease check:")
        print("1. Server hostname/IP is correct")
        print("2. SSH credentials are correct")
        print("3. SSH key is set up (or use password authentication)")
        print("4. Firewall allows SSH connections")
        return
    
    # Test Ollama connection
    print(f"\n🔍 Testing Ollama connection...")
    ollama_success, ollama_msg = test_ollama_connection(host, user, int(port), int(ollama_port), key_path)
    if ollama_success:
        print(f"✅ {ollama_msg}")
    else:
        print(f"❌ {ollama_msg}")
        print("\nPlease check:")
        print("1. Ollama is installed and running on the H100 server")
        print("2. Ollama port is correct")
        print("3. Firewall allows connections to Ollama port")
        return
    
    # Create secrets.toml
    secrets_content = f"""# SSH Configuration for H100 GPU Server
ssh_host = "{host}"
ssh_user = "{user}"
ssh_port = {port}
ssh_key_path = "{key_path}"
ollama_port = {ollama_port}
local_port = 11434
"""
    
    secrets_dir = ".streamlit"
    secrets_file = os.path.join(secrets_dir, "secrets.toml")
    
    os.makedirs(secrets_dir, exist_ok=True)
    
    with open(secrets_file, "w") as f:
        f.write(secrets_content)
    
    print(f"\n✅ Configuration saved to {secrets_file}")
    print("\n🚀 You can now run the Streamlit app:")
    print("streamlit run app.py")
    
    print("\n📝 Next steps:")
    print("1. Make sure your model is available on the H100 server")
    print("2. Run: ollama pull hf.co/bartowski/cognitivecomputations_Dolphin3.0-R1-Mistral-24B-GGUF:Q5_K_S")
    print("3. Start the Streamlit app and click 'Connect SSH Tunnel'")

if __name__ == "__main__":
    main() 