echo "Updating Package Manager..."
sudo apt update

echo "Installing Node.js/NPM..."
sudo apt install -y nodejs
sudo apt install -y npm

echo "Updating Systems..."
sudo apt upgrade -y

echo "Installing Node Dependencies..."
sudo npm i --production

echo "Installation Completed..."
