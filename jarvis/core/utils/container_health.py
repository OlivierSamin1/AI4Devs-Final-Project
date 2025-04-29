"""
Container health check utilities.

This module provides functions and utilities for container health checks.
These functions are used by both the health API endpoints and internal monitoring.
"""
from django.db import connections
from django.db.utils import OperationalError
import socket
import os
import logging

logger = logging.getLogger(__name__)

def check_database_connection():
    """
    Check if the database connection is working.
    
    Returns:
        dict: Status of database connection with details
    """
    try:
        db_conn = connections['default']
        db_conn.cursor()
        return {
            'status': 'healthy',
            'details': 'Database connection established'
        }
    except OperationalError as e:
        logger.error(f"Database connection error: {str(e)}")
        return {
            'status': 'unhealthy',
            'details': f'Database connection failed: {str(e)}'
        }

def check_disk_space(path='/app', threshold_mb=100):
    """
    Check if there is enough disk space.
    
    Args:
        path (str): Path to check
        threshold_mb (int): Minimum required space in MB
        
    Returns:
        dict: Status of disk space check with details
    """
    try:
        stat = os.statvfs(path)
        free_bytes = stat.f_bavail * stat.f_frsize
        free_mb = free_bytes / (1024 * 1024)
        
        if free_mb < threshold_mb:
            logger.warning(f"Low disk space: {free_mb:.2f}MB available, threshold: {threshold_mb}MB")
            return {
                'status': 'unhealthy',
                'details': f'Low disk space: {free_mb:.2f}MB available, threshold: {threshold_mb}MB'
            }
        
        return {
            'status': 'healthy',
            'details': f'Sufficient disk space: {free_mb:.2f}MB available'
        }
    except Exception as e:
        logger.error(f"Disk space check error: {str(e)}")
        return {
            'status': 'unknown',
            'details': f'Error checking disk space: {str(e)}'
        }

def check_memory_usage(threshold_percent=90):
    """
    Check if memory usage is below threshold.
    
    Args:
        threshold_percent (int): Maximum memory usage percentage allowed
        
    Returns:
        dict: Status of memory usage check with details
    """
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        mem_info = {}
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if 'kB' in value:
                    value = int(value.replace('kB', '').strip())
                mem_info[key] = value
        
        if 'MemTotal' in mem_info and 'MemAvailable' in mem_info:
            total = mem_info['MemTotal']
            available = mem_info['MemAvailable']
            used_percent = 100 - (available * 100 / total)
            
            if used_percent > threshold_percent:
                logger.warning(f"High memory usage: {used_percent:.2f}%, threshold: {threshold_percent}%")
                return {
                    'status': 'unhealthy',
                    'details': f'High memory usage: {used_percent:.2f}%, threshold: {threshold_percent}%'
                }
            
            return {
                'status': 'healthy',
                'details': f'Memory usage normal: {used_percent:.2f}%'
            }
        
        return {
            'status': 'unknown',
            'details': 'Could not determine memory usage'
        }
    except Exception as e:
        logger.error(f"Memory check error: {str(e)}")
        return {
            'status': 'unknown',
            'details': f'Error checking memory: {str(e)}'
        }

def get_container_health_status():
    """
    Get overall container health status by checking all components.
    
    Returns:
        tuple: (bool, dict) indicating if healthy and detailed status
    """
    # Check all components
    db_status = check_database_connection()
    disk_status = check_disk_space()
    memory_status = check_memory_usage()
    
    # Compile results
    results = {
        'database': db_status,
        'disk_space': disk_status,
        'memory': memory_status,
    }
    
    # Overall status is healthy only if all components are healthy
    is_healthy = all(component['status'] == 'healthy' for component in results.values())
    
    return is_healthy, results 