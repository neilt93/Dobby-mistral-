# Dobby: Mistral-24B Dolphin on H100 GPU

This Streamlit app connects to a remote H100 GPU server via SSH to run the Mistral-24B Dolphin model through Ollama.

## Prerequisites

### Local Machine
- Python 3.8+
- SSH client
- Streamlit
- Required Python packages (see requirements.txt)

### H100 Server
- SSH access
- Ollama installed and running
- Mistral-24B Dolphin model downloaded
- Sufficient GPU memory (24GB+ recommended)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure SSH Connection

Run the setup script to configure your SSH connection:

```bash
python setup_ssh.py
```

This will:
- Test your SSH connection to the H100 server
- Verify Ollama is running on the server
- Create a `.streamlit/secrets.toml` file with your configuration

### 3. Manual Configuration (Alternative)

If you prefer to configure manually, create `.streamlit/secrets.toml`:

```toml
# SSH Configuration for H100 GPU Server
ssh_host = "your-h100-server.com"
ssh_user = "your-username"
ssh_port = 22
ollama_port = 11434
local_port = 11434
```

### 4. Prepare the H100 Server

On your H100 server, ensure Ollama is running and the model is available:

```bash
# Start Ollama (if not already running)
ollama serve

# Pull the Mistral-24B Dolphin model
ollama pull hf.co/bartowski/cognitivecomputations_Dolphin3.0-R1-Mistral-24B-GGUF:Q5_K_S
```

### 5. Run the Streamlit App

```bash
streamlit run app.py
```

## Usage

1. **Connect SSH Tunnel**: Click "Connect SSH Tunnel" in the sidebar
2. **Verify Connection**: Check that the tunnel status shows "✅ SSH Tunnel Active"
3. **Start Chatting**: Begin chatting with Dobby through the H100 GPU

## Features

- **SSH Tunnel Management**: Automatic SSH tunnel creation and management
- **Connection Status**: Real-time monitoring of SSH and Ollama connections
- **Model Verification**: Checks if the required model is available on the server
- **Error Handling**: Graceful handling of connection issues
- **Cleanup**: Automatic cleanup of SSH tunnels when the app closes

## Troubleshooting

### SSH Connection Issues
- Verify SSH credentials and key setup
- Check firewall settings on both local and remote machines
- Ensure the H100 server is accessible from your network

### Ollama Connection Issues
- Verify Ollama is running on the H100 server: `ollama serve`
- Check if the model is downloaded: `ollama list`
- Ensure sufficient GPU memory is available

### Performance Issues
- The H100 GPU should provide excellent performance for the 24B model
- Monitor GPU usage on the server: `nvidia-smi`
- Consider adjusting model parameters in the app for optimal performance

## Security Notes

- SSH keys are recommended over password authentication
- The SSH tunnel is local-only and secure
- No sensitive data is stored in the app
- Consider using a VPN for additional security if needed

## Model Information

- **Model**: Mistral-24B Dolphin (GGUF format)
- **Size**: ~24B parameters
- **Format**: GGUF (Q5_K_S quantization)
- **GPU Memory**: ~24GB recommended
- **Performance**: Optimized for H100 GPU acceleration

## File Structure

```
Streamlit for dobby mistral/
├── app.py                 # Main Streamlit application
├── setup_ssh.py          # SSH configuration script
├── requirements.txt      # Python dependencies
├── README_H100.md       # This file
└── .streamlit/
    └── secrets.toml     # SSH configuration (created by setup)
``` 