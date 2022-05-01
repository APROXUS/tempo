reset
echo "Updating package manager..."
sudo apt-get update

reset
echo "Installing .NET Core 6 via APT..."
wget https://packages.microsoft.com/config/ubuntu/21.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y apt-transport-https
sudo apt-get update
sudo apt-get install -y dotnet-runtime-6.0

reset
echo "Installing JDK 13 via APT..."
sudo apt-get update
sudo apt-get install openjdk-17-jdk

reset
echo "Installation completed..."
