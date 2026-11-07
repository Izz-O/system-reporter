# Inventory Service

Serves stock levels on port 8002 (Python, runs in Docker).

## Run it 

	cd system-reporter
	sudo docker build -t trailside-inventory inventory 
	sudo cp systemd/trailside-inventory.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable --now trailside-inventory 

## Check it 

	systemctl status trailside-inventory 
	sudo docker ps 
	curl localhost:8002/api/stock

Routes: /, /api/stock, /api/stock/<id> 
