"""
CMDB Integration - Query device inventory
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Device:
    """Network device from CMDB"""
    hostname: str
    management_ip: str
    device_type: str
    device_role: str
    vendor: str
    platform: str
    credential_ref: str
    model: Optional[str] = None
    site: Optional[str] = None
    rack: Optional[str] = None
    serial_number: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    bgp_enabled: bool = False
    ospf_enabled: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def has_tag(self) -> callable:
        """Check if device has a specific tag"""
        return lambda tag: tag in self.tags
    
    @property
    def allows_execution(self) -> bool:
        """Check if device allows write operations"""
        return 'allow_execute' in self.tags
    
    def __str__(self) -> str:
        return f"{self.hostname} ({self.management_ip}) - {self.vendor} {self.platform}"


class CMDB:
    """Configuration Management Database"""
    
    def __init__(self, cmdb_path: Optional[Path] = None):
        """
        Initialize CMDB
        
        Args:
            cmdb_path: Path to CMDB file (default: from config)
        """
        self.cmdb_path = cmdb_path or Config.CMDB_PATH
        self.devices: List[Device] = []
        self._load_devices()
        logger.info("cmdb_initialized", cmdb_path=str(self.cmdb_path), device_count=len(self.devices))
    
    def _load_devices(self):
        """Load devices from CMDB file"""
        if not self.cmdb_path.exists():
            logger.warning("cmdb_file_not_found", path=str(self.cmdb_path))
            return
        
        with open(self.cmdb_path, 'r') as f:
            data = yaml.safe_load(f)
        
        devices_data = data.get('devices', [])
        
        for device_data in devices_data:
            device = Device(
                hostname=device_data['hostname'],
                management_ip=device_data['management_ip'],
                device_type=device_data['device_type'],
                device_role=device_data['device_role'],
                vendor=device_data['vendor'],
                platform=device_data['platform'],
                credential_ref=device_data['credential_ref'],
                model=device_data.get('model'),
                site=device_data.get('site'),
                rack=device_data.get('rack'),
                serial_number=device_data.get('serial_number'),
                tags=device_data.get('tags', []),
                bgp_enabled=device_data.get('bgp_enabled', False),
                ospf_enabled=device_data.get('ospf_enabled', False),
                metadata={k: v for k, v in device_data.items() 
                         if k not in ['hostname', 'management_ip', 'device_type', 'device_role',
                                     'vendor', 'platform', 'credential_ref', 'model', 'site',
                                     'rack', 'serial_number', 'tags', 'bgp_enabled', 'ospf_enabled']}
            )
            self.devices.append(device)
        
        logger.info("devices_loaded", count=len(self.devices))
    
    def get_device(self, hostname: str) -> Optional[Device]:
        """
        Get device by hostname
        
        Args:
            hostname: Device hostname
            
        Returns:
            Device object or None if not found
        """
        for device in self.devices:
            if device.hostname == hostname:
                logger.debug("device_found", hostname=hostname)
                return device
        
        logger.warning("device_not_found", hostname=hostname)
        return None
    
    def query_devices(self, **filters) -> List[Device]:
        """
        Query devices with filters
        
        Args:
            **filters: Filter criteria (vendor, platform, tags, etc.)
            
        Returns:
            List of matching devices
        """
        results = self.devices.copy()
        
        for key, value in filters.items():
            if key == 'tags':
                # Tags can be a list - device must have ALL specified tags
                if isinstance(value, list):
                    results = [d for d in results if all(tag in d.tags for tag in value)]
                else:
                    results = [d for d in results if value in d.tags]
            
            elif key == 'platform':
                # Platform can be a list - device must match ONE of the platforms
                if isinstance(value, list):
                    results = [d for d in results if d.platform in value]
                else:
                    results = [d for d in results if d.platform == value]
            
            else:
                # Direct attribute match
                results = [d for d in results if getattr(d, key, None) == value]
        
        logger.info("devices_queried", filters=filters, result_count=len(results))
        return results
    
    def list_devices(self) -> List[Device]:
        """Get all devices"""
        return self.devices.copy()

