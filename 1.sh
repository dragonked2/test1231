#!/bin/bash

set -e  # Exit on error
set -o pipefail  # Catch pipeline errors
LOGFILE="/var/log/openvpn_install.log"
exec > >(tee -a "$LOGFILE") 2>&1

# Variables
VPN_NET="10.8.0.0"
VPN_MASK="255.255.255.0"
VPN_PORT=1194
VPN_PROTO="udp"
SERVER_IP=$(curl -s ifconfig.me)
EASY_RSA_DIR="/etc/openvpn/easy-rsa"

# Ensure script is run as root
if [[ "$EUID" -ne 0 ]]; then
  echo "This script must be run as root!" >&2
  exit 1
fi

# Update and install dependencies
echo "Updating system and installing required packages..."
apt update && apt upgrade -y
apt install -y openvpn easy-rsa iptables-persistent curl

# Set up OpenVPN configuration
echo "Setting up OpenVPN server..."
mkdir -p /etc/openvpn/server
cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/server/
gunzip /etc/openvpn/server/server.conf

sed -i "s/^port .*/port $VPN_PORT/" /etc/openvpn/server/server.conf
sed -i "s/^proto .*/proto $VPN_PROTO/" /etc/openvpn/server/server.conf
sed -i "s/^dev .*/dev tun/" /etc/openvpn/server/server.conf

# Set up Easy-RSA for certificates
echo "Initializing Easy-RSA..."
make-cadir $EASY_RSA_DIR
cd $EASY_RSA_DIR
cp vars.example vars

# Build CA and keys
source vars
./clean-all
./build-ca --batch
./build-key-server --batch server
./build-dh
openvpn --genkey --secret ta.key

cp $EASY_RSA_DIR/keys/{server.crt,server.key,ca.crt,dh2048.pem,ta.key} /etc/openvpn/server/

# Enable IP forwarding
echo "Enabling IP forwarding..."
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# Configure firewall rules
echo "Configuring firewall rules..."
iptables -t nat -A POSTROUTING -s $VPN_NET/$VPN_MASK -o eth0 -j MASQUERADE
iptables-save > /etc/iptables/rules.v4

# Enable and start OpenVPN service
echo "Starting OpenVPN service..."
systemctl enable openvpn@server
systemctl start openvpn@server

# Generate Client Configuration
echo "Generating client configuration..."
mkdir -p /etc/openvpn/client-configs
cat > /etc/openvpn/client-configs/client.ovpn <<EOF
client
dev tun
proto $VPN_PROTO
remote $SERVER_IP $VPN_PORT
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
tls-auth ta.key 1
cipher AES-256-CBC
EOF

# Provide instructions
echo "OpenVPN setup is complete. Copy the client.ovpn file to your client machine."
echo "Reboot the server if necessary."
