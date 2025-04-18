# Raspberry Pi Hardware Preparation Guide

This guide provides detailed instructions for preparing both Raspberry Pi devices for the Personal Database Assistant project.

## Overview

We'll set up two Raspberry Pi devices:
- **Raspberry Pi 3B**: For the offline database server
- **Raspberry Pi 4**: For the internet-facing application server

## Hardware Requirements

### For Raspberry Pi 3B (Database Server)

- Raspberry Pi 3B or 3B+
- 32GB+ high-endurance microSD card
- 5V/2.5A power supply with micro USB connector
- Ethernet cable
- Optional: Case with passive cooling

### For Raspberry Pi 4 (Application Server)

- Raspberry Pi 4 (4GB or 8GB RAM recommended)
- 64GB+ high-endurance microSD card
- 5V/3A USB-C power supply
- Ethernet cable
- Raspberry Pi 4 case with active cooling (fan/heatsink)

### Additional Hardware

- Network router with VLAN capability (recommended)
- microSD card reader for your computer
- HDMI monitor and keyboard (for initial setup)

## Step 1: Operating System Installation

### For Both Raspberry Pi Devices

1. Download the Raspberry Pi Imager from [the official website](https://www.raspberrypi.org/software/)

2. Insert your microSD card into your computer

3. Launch Raspberry Pi Imager and select:
   - **Choose OS**: Raspberry Pi OS (64-bit) for Pi 4, Raspberry Pi OS (32-bit) for Pi 3B
   - **Choose Storage**: Select your microSD card
   - Click the gear icon ⚙️ for advanced options before writing

4. In advanced options:
   - Set hostname: `pi3b-db-server` for the 3B and `pi4-app-server` for the Pi 4
   - Enable SSH with password authentication (initially)
   - Configure your WiFi if needed (but we'll use Ethernet)
   - Set your timezone and keyboard layout
   - Create a user account (don't use the default 'pi' user for security)

5. Click "Write" and wait for the process to complete

6. Insert the microSD card into the respective Raspberry Pi

## Step 2: Initial Boot and Configuration

1. Connect each Raspberry Pi to:
   - Monitor via HDMI
   - Keyboard via USB
   - Ethernet cable to your router
   - Power supply

2. Power on and wait for the initial boot process to complete

3. Login with the credentials you set during the image creation

4. Update the system:
   ```bash
   sudo apt update
   sudo apt full-upgrade -y
   sudo reboot
   ```

5. After reboot, login again and secure SSH:
   ```bash
   # Disable password authentication
   sudo nano /etc/ssh/sshd_config
   ```
   
   Find and modify these lines:
   ```
   PasswordAuthentication no
   PermitRootLogin no
   ```
   
   Save and exit (Ctrl+X, then Y, then Enter)
   
   ```bash
   sudo systemctl restart ssh
   ```

6. Set up SSH keys from your main computer to each Raspberry Pi

## Step 3: Network Configuration

### For Both Raspberry Pi Devices

1. Set static IP addresses:
   ```bash
   sudo nano /etc/dhcpcd.conf
   ```

2. Add the following (adjust according to your network):
   
   For Pi 3B (Database Server):
   ```
   interface eth0
   static ip_address=192.168.1.101/24
   static routers=192.168.1.1
   static domain_name_servers=192.168.1.1 8.8.8.8
   ```
   
   For Pi 4 (Application Server):
   ```
   interface eth0
   static ip_address=192.168.1.100/24
   static routers=192.168.1.1
   static domain_name_servers=192.168.1.1 8.8.8.8
   ```

3. Reboot to apply network changes:
   ```bash
   sudo reboot
   ```

## Step 4: Security Hardening

### For Both Raspberry Pi Devices

1. Install and configure UFW firewall:
   ```bash
   sudo apt install ufw -y
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   ```

2. Configure specific firewall rules:
   
   For Pi 3B (Database Server):
   ```bash
   sudo ufw allow from 192.168.1.100 to any port 5432 proto tcp  # PostgreSQL
   sudo ufw allow from 192.168.1.100 to any port 8001 proto tcp  # Data Privacy Vault
   sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp   # SSH from local network
   ```
   
   For Pi 4 (Application Server):
   ```bash
   sudo ufw allow 80/tcp                                         # HTTP
   sudo ufw allow 443/tcp                                        # HTTPS
   sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp   # SSH from local network
   ```

3. Enable the firewall:
   ```bash
   sudo ufw enable
   ```

4. Verify firewall status:
   ```bash
   sudo ufw status verbose
   ```

## Step 5: Install Required Software

### For Raspberry Pi 3B (Database Server)

1. Install PostgreSQL:
   ```bash
   sudo apt install postgresql postgresql-contrib -y
   ```

2. Secure PostgreSQL installation:
   ```bash
   # Change to postgres user
   sudo -i -u postgres
   
   # Create a new superuser (replace secure_password with a strong password)
   createuser --interactive --pwprompt
   # Enter name of role to add: dbadmin
   # Enter password for new role: 
   # Enter it again: 
   # Shall the new role be a superuser? (y/n) y
   
   # Exit postgres user shell
   exit
   ```

3. Configure PostgreSQL to listen on all interfaces:
   ```bash
   sudo nano /etc/postgresql/13/main/postgresql.conf
   ```
   
   Find and modify this line:
   ```
   listen_addresses = '*'
   ```
   
   Save and exit

4. Configure PostgreSQL authentication:
   ```bash
   sudo nano /etc/postgresql/13/main/pg_hba.conf
   ```
   
   Add this line at the end (to allow connections only from Pi 4):
   ```
   host    all             all             192.168.1.100/32         md5
   ```
   
   Save and exit

5. Restart PostgreSQL:
   ```bash
   sudo systemctl restart postgresql
   ```

### For Raspberry Pi 4 (Application Server)

1. Install Docker and Docker Compose:
   ```bash
   # Add Docker's official GPG key
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   
   # Set up the repository
   echo "deb [arch=arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
   # Update and install Docker
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io -y
   
   # Add your user to the docker group
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo apt install python3-pip -y
   sudo pip3 install docker-compose
   ```

2. Install Nginx:
   ```bash
   sudo apt install nginx -y
   ```

3. Enable and start the services:
   ```bash
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

## Step 6: Set Up Storage

### For Both Raspberry Pi Devices

1. Check available storage:
   ```bash
   df -h
   ```

2. If using external storage, mount it:
   ```bash
   # Create mount points
   sudo mkdir -p /mnt/data
   
   # For USB drives, find the device
   lsblk
   
   # Mount the device (replace sdX1 with your device)
   sudo mount /dev/sdX1 /mnt/data
   
   # To make it permanent, add to fstab
   sudo nano /etc/fstab
   ```
   
   Add a line like this (replace UUID with your drive's UUID from `blkid` command):
   ```
   UUID=your-drive-uuid  /mnt/data  ext4  defaults,noatime  0  2
   ```
   
   Save and exit

## Step 7: Performance Optimization

### For Both Raspberry Pi Devices

1. Adjust swap size:
   ```bash
   sudo nano /etc/dphys-swapfile
   ```
   
   Change the value:
   ```
   CONF_SWAPSIZE=1024
   ```
   
   Save, exit, and restart swap:
   ```bash
   sudo systemctl restart dphys-swapfile
   ```

2. Adjust GPU memory split (lower for server use):
   ```bash
   sudo nano /boot/config.txt
   ```
   
   Add or modify:
   ```
   gpu_mem=16
   ```
   
   Save and exit

## Step 8: System Monitoring Tools

### For Both Raspberry Pi Devices

1. Install monitoring tools:
   ```bash
   sudo apt install htop iotop iftop -y
   ```

2. Install temperature monitoring:
   ```bash
   sudo apt install lm-sensors -y
   sudo sensors-detect
   # Answer YES to all questions
   sudo sensors
   ```

## Step 9: Backup Configuration

1. Create a backup directory:
   ```bash
   mkdir -p ~/backups
   ```

2. Create a backup script:
   ```bash
   nano ~/backup.sh
   ```
   
   Add the following:
   ```bash
   #!/bin/bash
   BACKUP_DIR=~/backups
   DATE=$(date +%Y-%m-%d_%H-%M-%S)
   
   # Backup important configuration files
   sudo tar -czf $BACKUP_DIR/system_config_$DATE.tar.gz \
     /etc/ssh \
     /etc/fstab \
     /etc/dhcpcd.conf \
     /etc/ufw \
     /etc/nginx \
     /boot/config.txt
   
   # For database server, add PostgreSQL backup
   if [ -d "/etc/postgresql" ]; then
     sudo -u postgres pg_dumpall > $BACKUP_DIR/postgres_$DATE.sql
   fi
   
   echo "Backup completed: $BACKUP_DIR"
   ```
   
   Make it executable:
   ```bash
   chmod +x ~/backup.sh
   ```

3. Set up a cron job for regular backups:
   ```bash
   crontab -e
   ```
   
   Add:
   ```
   0 3 * * * ~/backup.sh
   ```
   
   This will run the backup script daily at 3 AM

## Step a: Verification

1. Verify systems are properly configured:
   ```bash
   # Check system status
   top -b -n 1
   
   # Check disk usage
   df -h
   
   # Check network connectivity
   ping -c 4 192.168.1.101  # From Pi 4 to Pi 3B
   ping -c 4 192.168.1.100  # From Pi 3B to Pi 4
   
   # Check services
   systemctl status postgresql  # On Pi 3B
   systemctl status docker      # On Pi 4
   systemctl status nginx       # On Pi 4
   ```

## Next Steps

Now that your Raspberry Pi hardware is prepared, proceed to [Container Infrastructure Setup](./02_container_infrastructure_setup.md) to configure the Docker containers for the Personal Database Assistant. 