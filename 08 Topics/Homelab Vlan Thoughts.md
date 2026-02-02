#homelab

Example network:
- VLAN10 - MAIN-DEVICES
- VLAN20 - STREAMING-DEVICES
- VLAN30 - CAMERAS
- VLAN40 - GUEST-NETWORK
- VLAN50 - IOT-DEVICES
- VLAN60 - SERVERS-NAS

# Example rule structure:  
LAN: Allow outgoing connections, block incoming connections from IoT VLAN  
IoT: Allow outgoing to internet, block outgoing to LAN except for authorized services