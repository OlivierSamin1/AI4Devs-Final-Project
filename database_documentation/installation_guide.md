# Installation Guide

This guide provides detailed instructions for installing and configuring the Personal Asset Management System.

> **IMPORTANT COMPATIBILITY NOTICE**: This project is currently **only compatible with Raspberry Pi devices** (ARM architecture). If you have an x86/x64 system, manual installation is the only option at present. Development is underway to add support for x86/x64 systems through QEMU emulation.

## Prerequisites

Ensure your system meets the [system requirements](system_requirements.md) before proceeding.

## Installation Methods

Choose one of the following installation methods:

1. [Docker Installation](#docker-installation) (Recommended for Raspberry Pi)
2. [Manual Installation](#manual-installation) (Works on all platforms, but limited functionality on x86/x64)
3. [Raspberry Pi Installation](#raspberry-pi-installation)

## Docker Installation

> **Important**: This Docker installation method is specifically designed for Raspberry Pi devices with ARM architecture and is not compatible with x86/x64 CPU architecture. For x86/x64 systems, use the Manual Installation method.

### Step 1: Install Docker and Docker Compose

#### For Ubuntu/Debian:
```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install -y docker-compose
```

#### For other operating systems:
Follow the [official Docker installation guide](https://docs.docker.com/get-docker/).

### Step 2: Clone the Repository
```bash
git clone https://github.com/yourusername/database_v2.git
cd database_v2
```

### Step 3: Configure Environment Variables
```bash
cp .env.example .env
```

Edit the `.env` file with your preferred text editor and set the required variables:
```
DEBUG=False
SECRET_KEY=your_secure_secret_key
DB_NAME=assetdb
DB_USER=assetuser
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
UPLOADED_FILE_PATH=media/
```

### Step 4: Pull and Prepare Docker Image

The system requires a specific Docker image that needs to be pulled and tagged. Please note that this image is only compatible with ARM architecture (Raspberry Pi):

```bash
# Pull the base image from Docker Hub (ARM architecture only)
docker pull aipoweredcompany/nas_database:base_with_requirements

# Tag the image with the required name and tag
docker tag aipoweredcompany/nas_database:base_with_requirements api:20230622
```

### Step 5: Build and Start Containers

#### Understanding the Dockerfile
The system uses the following Dockerfile configuration:

```Dockerfile
FROM api:20230622
COPY database .
WORKDIR /home
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && python watch_directory.py
```

Key components:
- Base image: `api:20230622` which contains all necessary dependencies (ARM architecture only)
- Working directory: `/home`
- Commands run on startup:
  - Database migrations
  - Django development server on port 8000
  - File watcher script for monitoring changes

#### Starting the Application

For local development on Raspberry Pi:
```bash
docker-compose -f api_local.yaml up -d
```

For Raspberry Pi deployment:
```bash
docker-compose -f api_RPI.yaml up -d
```

For standard deployment on Raspberry Pi:
```bash
docker-compose up -d
```

### Step 6: Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### Step 7: Access the Application
Visit `http://localhost:8000` in your web browser.

## Manual Installation

> **Note for x86/x64 Users**: While the manual installation will allow you to run the Django application, some hardware-specific features may not work correctly on x86/x64 platforms. Full support for these platforms via QEMU emulation is under development.

### Step 1: Install PostgreSQL
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Create a database and user:
```bash
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
CREATE DATABASE assetdb;
CREATE USER assetuser WITH PASSWORD 'your_secure_password';
ALTER ROLE assetuser SET client_encoding TO 'utf8';
ALTER ROLE assetuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE assetuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE assetdb TO assetuser;
\q
```

### Step 2: Install Python and Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv
git clone https://github.com/yourusername/database_v2.git
cd database_v2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
```bash
cp .env.example .env
```

Edit the `.env` file with appropriate values.

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 7: Run the Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

For production deployment, consider using Gunicorn and Nginx.

## Raspberry Pi Installation

### Step 1: Prepare the Raspberry Pi

Install Raspberry Pi OS (formerly Raspbian) with desktop on your Raspberry Pi 4 or newer.

Update your system:
```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Docker and Docker Compose

```bash
# Install Docker
curl -sSL https://get.docker.com | sh

# Add user to Docker group
sudo usermod -aG docker $USER

# Install dependencies for Docker Compose
sudo apt install -y libffi-dev libssl-dev python3 python3-pip

# Install Docker Compose
sudo pip3 install docker-compose
```

### Step 3: Follow Docker Installation Steps

Follow Steps 2-6 from the [Docker Installation](#docker-installation) section.

### Additional Notes for Raspberry Pi:
- Ensure you have adequate cooling for your Raspberry Pi
- Consider using an external SSD for better performance
- Adjust the Docker memory limits in `docker-compose.yml` to match your device's capabilities

## Future Compatibility Plans

### Upcoming Support for x86/x64 via QEMU Emulation

Development is in progress to add support for running this project on standard PC hardware (x86/x64 architecture) by emulating the Raspberry Pi environment through QEMU. This feature will allow users to:

- Run the full application stack on regular PCs and servers
- Maintain the same functionality as on Raspberry Pi
- Use the same Docker images through architecture emulation

Stay tuned for updates on this feature. If you have expertise in QEMU or cross-architecture emulation and would like to contribute, please check the project's contribution guidelines.

## Post-Installation Configuration

### Setting Up Backup System
```bash
# Create a backup directory
mkdir -p ~/database_backups

# Add a cron job for automatic backups
(crontab -l 2>/dev/null; echo "0 2 * * * cd /path/to/database_v2 && docker-compose exec -T db pg_dump -U assetuser assetdb > ~/database_backups/assetdb_\$(date +\%Y\%m\%d).sql") | crontab -
```

### Securing Your Installation

1. Set up a firewall:
```bash
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow 8000
sudo ufw enable
```

2. Set up HTTPS with Let's Encrypt (if publicly accessible).

## Troubleshooting

If you encounter issues during installation, refer to the [troubleshooting guide](troubleshooting.md).

For additional help, check the project's issue tracker on GitHub.