echo "Updating Package Manager..."
sudo apt update

echo "Installing Virtuoso as a Service..."
sudo cp virtuoso.service /etc/systemd/system/virtuoso.service
sudo systemctl daemon-reload
sudo systemctl enable virtuoso
sudo systemctl start virtuoso

echo "Installation Completed..."
