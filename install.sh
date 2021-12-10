sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip ffmpeg -y
sudo python3 -m pip install urllib3 asyncio yt-dlp discord.py[voice] validators hurry.filesize

reset
echo "Dependencies intstalled successfully..."
