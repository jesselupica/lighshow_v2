sudo cp boot_lightshow.sh /etc/init.d
sudo chmod +x /etc/init.d/boot_lightshow.sh
sudo chown root:root /etc/init.d/boot_lightshow.sh

sudo update-rc.d boot_lightshow.sh defaults
sudo update-rc.d boot_lightshow.sh enable

sudo apt-get install portaudio19-dev 

sudo pip3 install -r requirements.txt

sudo chmod +x ../run.sh
sudo chown root:root ../run.sh

