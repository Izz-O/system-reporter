# Inventory Service Setup

Serves stock levels on port 8002.

## Install
```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin svcuser
sudo mkdir -p /opt/trailside/inventory
sudo cp inventory/app.py /opt/trailside/inventory/
sudo cp systemd/trailside-inventory.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now trailside-inventory
```
(Skip the `useradd` line if `svcuser` already exists.)

## Verify
```bash
systemctl status trailside-inventory
curl localhost:8002/api/stock
curl localhost:8002/api/stock/fishing-rod
```
