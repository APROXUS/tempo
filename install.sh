sudo apt-get update
sudo apt-get install python3 python3-pip ffmpeg -y
sudo python3 -m pip install yt-dlp
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
nvm --version
nvm install --lts
node --version
npm install

reset
echo "Dependencies intstalled successfully..."
