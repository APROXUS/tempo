reset
echo "Updating package manager..."
sudo apt-get update

reset
echo "Installing Conducter/Lavalink as a service..."
sudo cp conducter.service /etc/systemd/system/conducter.service
sudo cp lavalink.service /etc/systemd/system/lavalink.service
sudo systemctl daemon-reload
sudo systemctl enable conducter
sudo systemctl enable lavalink
sudo systemctl start conducter
sudo systemctl start lavalink

reset
echo "Installation completed..."
