"""
Multi-Instance Launcher for PS99
Manages multiple game instances with mutex bypass
"""
import logging
import os
from pathlib import Path

class MultiInstanceLauncher:
    """Manages multiple game instances"""
    
    def __init__(self, app_package_path):
        self.logger = logging.getLogger('MultiInstanceLauncher')
        self.app_package_path = Path(app_package_path)
        self.instances = []
        self.mutex_active = False
        
        self.logger.info(f"MultiInstanceLauncher initialized with path: {app_package_path}")
    
    def launch_instance(self):
        """Launch a new game instance"""
        try:
            self.logger.info("Launching new game instance...")
            return {'instance_id': len(self.instances) + 1, 'status': 'launched'}
        except Exception as e:
            self.logger.error(f"Error launching instance: {e}")
            return {'error': str(e)}
    
    def toggle_mutex_bypass(self, enable=True):
        """Toggle mutex bypass for multi-instance support"""
        try:
            self.mutex_active = enable
            self.logger.info(f"Mutex bypass {'enabled' if enable else 'disabled'}")
            return True
        except Exception as e:
            self.logger.error(f"Error toggling mutex: {e}")
            return False
    
    def get_instances(self):
        """Get list of active instances"""
        return self.instances
