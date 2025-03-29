# System Requirements

This document outlines the detailed system requirements for running the Personal Asset Management System.

> **IMPORTANT COMPATIBILITY NOTICE**: This project is currently **only compatible with Raspberry Pi devices** (ARM architecture). Support for x86/x64 systems via QEMU emulation is under development.

## Hardware Requirements

### Current Platform Requirement
- **Processor Architecture**: ARM (Raspberry Pi only)
  - Raspberry Pi 4 or newer recommended

### Minimum Requirements
- **CPU**: Dual-core processor (1.5 GHz or higher)
  - Compatible with Raspberry Pi 4 (or newer)
- **RAM**: 2GB
- **Storage**: 5GB available space
- **Network**: Ethernet or WiFi connection

### Recommended Requirements
- **CPU**: Quad-core processor (2.0 GHz or higher)
- **RAM**: 4GB or more
- **Storage**: 10GB+ SSD/fast storage
- **Network**: Ethernet connection (1Gbps)

## Software Requirements

### Core Requirements
- **Operating System**: 
  - Linux (Ubuntu 20.04+, Debian 11+, Raspberry Pi OS)
  - Windows 10+ with WSL2
  - macOS 11+
- **Docker**: 20.10.x or newer
- **Docker Compose**: 2.0.0 or newer
- **Python**: 3.9 or newer (if running without Docker)

### Database
- **PostgreSQL**: 13.0 or newer

### Web Browser (for UI)
- **Chrome**: Version 90+
- **Firefox**: Version 88+
- **Safari**: Version 14+
- **Edge**: Version 90+

## Network Requirements

- **Ports**: 
  - 8000: Web interface
  - 5432: PostgreSQL (internal only)
- **Internet Access**: Required for initial setup and updates
- **Protocols**: HTTP/HTTPS, WebSockets

## Permission Requirements

- File system read/write access to application directory
- Network socket creation and binding
- Docker container management (if using Docker deployment)

## Deployment Options

### Docker Deployment (Recommended for Raspberry Pi)
- **Hardware**: ARM architecture (Raspberry Pi 4 or newer)
- Docker and Docker Compose installed
- User with Docker permissions
- Internet access to pull the required Docker image:
  - Base image: `aipoweredcompany/nas_database:base_with_requirements` (ARM-only)
- At least 1GB of free space for Docker images

> **Note**: The Docker deployment method is only compatible with ARM architecture (Raspberry Pi devices) and will not work on x86/x64 systems.

### Direct Deployment (Works on all platforms)
- Python 3.9+ installed
- PostgreSQL instance
- Virtual environment capability
- Development tools for compiling extensions

## Upcoming Platform Support

### x86/x64 Support via QEMU Emulation (In Development)

Future releases will include support for running on standard PC hardware via QEMU emulation of the ARM environment. When implemented, this will require:

- **CPU**: Any x86/x64 processor with virtualization support
- **RAM**: 4GB minimum (8GB recommended)
- **Additional Software**: QEMU and related libraries
- **Storage**: 10GB+ for emulation overhead

This feature is currently under active development and is not yet available in the stable release.

## Resource Considerations

### Resource Scaling
- Database size will increase with document storage
- Consider storage growth of ~50MB per month with regular usage

### Performance Factors
- Number of stored assets and documents
- Concurrent users (if sharing access)
- Backup frequency and size

## Security Considerations

The system handles sensitive financial information and should be deployed with appropriate security measures:

- Run behind a secured network or VPN
- Use HTTPS for all connections
- Implement regular backups
- Use strong passwords for admin accounts
- Keep all system components updated

For installation instructions, see the [Installation Guide](installation_guide.md). 