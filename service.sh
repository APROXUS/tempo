reset
echo "Updating package manager..."
sudo apt-get update

reset
echo "Installing Tempo/Lavalink as a service..."
sudo cp unit/tempo.service /etc/systemd/system/tempo.service
sudo cp unit/lavalink.service /etc/systemd/system/lavalink.service
sudo systemctl daemon-reload
sudo systemctl enable tempo
sudo systemctl enable lavalink
sudo systemctl start tempo
sudo systemctl start lavalink

reset
echo "Installation completed..."
