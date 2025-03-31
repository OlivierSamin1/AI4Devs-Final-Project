# Hardware Setup & Network Configuration

## Hardware Requirements

### Raspberry Pi 4 (Web Application Server)
- Raspberry Pi 4 Model B (recommended: 4GB or 8GB RAM)
- 32GB+ microSD card (class 10 or better)
- Power supply (USB-C, 5V/3A)
- Case with cooling (fan or heatsinks)
- Ethernet cable

### Additional Hardware
- Network router with VLAN capability
- USB keyboard and mouse (for initial setup)
- HDMI monitor (for initial setup)
- Optional: USB SSD drives for more reliable storage

## Operating System Installation

### Raspberry Pi 4 Setup

1. Download the Raspberry Pi OS (64-bit) from the official website:
   ```
   https://www.raspberrypi.org/software/operating-systems/
   ```

2. Install Raspberry Pi Imager on your computer:
   ```
   https://www.raspberrypi.org/software/
   ```

3. Insert the microSD card into your computer and launch Raspberry Pi Imager.

4. Select "Raspberry Pi OS (64-bit)" as the operating system.

5. Select your microSD card as the storage device.

6. Click on the gear icon (⚙️) to access advanced options:
   - Set hostname: `web-server-pi`
   - Enable SSH
   - Set username and password (do not use the default)
   - Configure your WiFi credentials as backup (though we'll primarily use Ethernet)
   - Set locale settings

7. Click "Write" to flash the OS to the microSD card.

8. Insert the microSD card into the Raspberry Pi 4, connect monitor, keyboard, mouse, and power supply.

## Initial System Configuration

### Raspberry Pi 4 Initial Setup

1. Boot up the Raspberry Pi 4 and log in.

2. Update the system:
   ```bash
   sudo apt update
   sudo apt full-upgrade -y
   sudo reboot
   ```

3. Install essential packages:
   ```bash
   sudo apt install -y vim git curl build-essential python3-pip python3-dev libpq-dev
   ```

4. Set a static IP for the Ethernet connection by editing the dhcpcd.conf file:
   ```bash
   sudo nano /etc/dhcpcd.conf
   ```

5. Add the following at the end of the file (adjust according to your network):
   ```
   interface eth0
   static ip_address=192.168.1.10/24
   static routers=192.168.1.1
   static domain_name_servers=192.168.1.1 8.8.8.8
   ```

6. Save and exit (Ctrl+O, Enter, Ctrl+X).

7. Create a directory for the application:
   ```bash
   mkdir -p ~/personal-db-assistant
   ```

## Network Configuration

### Verifying Connection to Database Server

1. The Raspberry Pi 3B (database server) should already be running on your network with a static IP address. Verify that you can reach it from the Raspberry Pi 4:
   ```bash
   ping 192.168.2.10
   ```
   Replace 192.168.2.10 with the actual IP address of your Raspberry Pi 3B.

2. If connectivity fails, you may need to configure your router to allow communication between the VLANs (if applicable).

### Router Configuration

1. Access your router's admin interface (usually by navigating to 192.168.1.1 or 192.168.0.1 in a web browser).

2. Set up port forwarding for the web server:
   - Forward external port 80 to 192.168.1.10:80
   - Forward external port 443 to 192.168.1.10:443

### Firewall Configuration for Raspberry Pi 4

1. Install and configure UFW (Uncomplicated Firewall):
   ```bash
   sudo apt install -y ufw
   ```

2. Set default policies:
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

3. Allow SSH and web traffic:
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

4. Enable firewall:
   ```bash
   sudo ufw enable
   ```

## Testing Connectivity

1. Test connectivity from Raspberry Pi 4 to Raspberry Pi 3B:
   ```bash
   ping 192.168.2.10
   ```
   Replace 192.168.2.10 with the actual IP address of your Raspberry Pi 3B.

2. If required, test database connectivity (assuming PostgreSQL is running on port 5432):
   ```bash
   nc -zv 192.168.2.10 5432
   ```
   If successful, you should see a message indicating the connection was established.

## Next Steps

After successfully setting up the Raspberry Pi 4 and ensuring it can communicate with the existing database server (Raspberry Pi 3B), proceed to the [Database Server Connection](./01b_Database_Server.md) document to set up the API client to fetch data from the existing database. 