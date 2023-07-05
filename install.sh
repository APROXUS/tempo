echo "Updating Package Manager..."
sudo apt update

echo "Installing Node.js/NPM..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
sudo apt install -y npm

echo "Updating Systems..."
sudo apt upgrade -y

echo "Installing Node Dependencies..."
npm i --production

echo "Installation Completed..."
