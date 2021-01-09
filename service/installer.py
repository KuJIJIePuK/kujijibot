import sys
import os 

def stop_service():
	os.system("sudo sustemctl stop bot.service")
	os.system("sudo sustemctl disable bot.service")

if __name__ == "__main__":
if sys.argv[0] == "install":
	stop_service()
	os.system("sudo cp bot.service /etc/systemd/system")
	os.system("sudo systemctl start bot.service")
	os.system("sudo systemctl enable bot.service")

elif sys.argv[0] == "uninstall":
	stop_service()
	os.system("sudo rm /etc/systemd/system/bot.service")
else:
	print("arguments: install, uninstall")