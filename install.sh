reset
echo "Updating package manager..."
sudo apt update

reset
echo "Installing Node.js/NPM via APT..."
sudo apt install -y nodejs
sudo apt install -y npm

reset
echo "Installing JDK 13 via APT..."
sudo apt install -y openjdk-18-jdk

reset
echo "Updating systems..."
sudo apt update
sudo apt upgrade -y

reset
echo "Installing Node dependencies..."
sudo npm i --production

reset
echo "Installation completed..."
