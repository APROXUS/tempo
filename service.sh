echo "Updating Package Manager..."
sudo apt update

echo "Installing Conducter as a Service..."
sudo cp conducter.service /etc/systemd/system/conducter.service
sudo systemctl daemon-reload
sudo systemctl enable conducter
sudo systemctl start conducter

echo "Installation Completed..."
