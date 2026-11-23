# Orders Service

Serves sample orders on **port 8003** (Python, runs under systemd).

## Install

    sudo useradd --system --no-create-home --shell /usr/sbin/nologin svcuser
    sudo mkdir -p /opt/trailside/orders
    sudo cp orders/app.py /opt/trailside/orders/
    sudo cp systemd/trailside-orders.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now trailside-orders

## Check

    systemctl status trailside-orders
    curl localhost:8003/api/orders

Routes: /, /api/orders, /api/orders/<id>
