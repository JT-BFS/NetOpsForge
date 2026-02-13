"""
CMDB Integration - Query device inventory

Supports multiple CMDB sources:
- YAML file (local)
- SolarWinds Orion
- ServiceNow (future)
- Database (future)
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
    """
    Configuration Management Database

    Supports multiple sources:
    - yaml: Local YAML file
    - solarwinds: SolarWinds Orion API
    - servicenow: ServiceNow CMDB (future)
    - database: PostgreSQL/MySQL (future)
    """

    def __init__(self, source: str = 'yaml', cmdb_path: Optional[Path] = None, **kwargs):
        """
        Initialize CMDB

        Args:
            source: CMDB source type ('yaml', 'solarwinds', etc.)
            cmdb_path: Path to CMDB file (for yaml source)
            **kwargs: Additional source-specific configuration
        """
        self.source = source
        self.cmdb_path = cmdb_path or Config.CMDB_PATH
        self.devices: List[Device] = []
        self.source_config = kwargs

        # Load devices from appropriate source
        if source == 'yaml':
            self._load_from_yaml()
        elif source == 'solarwinds':
            self._load_from_solarwinds()
        else:
            raise ValueError(f"Unsupported CMDB source: {source}")

        logger.info("cmdb_initialized", source=source, device_count=len(self.devices))
    
    def _load_from_yaml(self):
        """Load devices from YAML file"""
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

        logger.info("devices_loaded_from_yaml", count=len(self.devices))

    def _load_from_solarwinds(self):
        """Load devices from SolarWinds Orion"""
        try:
            from ..integrations.solarwinds import (
                SolarWindsClient,
                SolarWindsConfig,
                SolarWindsDeviceMapper,
                get_solarwinds_credentials
            )
        except ImportError as e:
            logger.error("solarwinds_import_error", error=str(e))
            raise ImportError("SolarWinds integration requires 'orionsdk' package. Install with: pip install orionsdk")

        # Get hostname
        hostname = self.source_config.get('hostname') or Config.SOLARWINDS_HOSTNAME

        # Get credentials - try Windows Credential Manager first, then config/env
        credential_ref = self.source_config.get('credential_ref', 'solarwinds_api')
        username = self.source_config.get('username')
        password = self.source_config.get('password')

        # If credentials not provided directly, try Windows Credential Manager
        if not (username and password):
            cred_username, cred_password = get_solarwinds_credentials(credential_ref)
            if cred_username and cred_password:
                username = cred_username
                password = cred_password
                logger.info("solarwinds_credentials_from_credman", credential_ref=credential_ref)
            else:
                # Fall back to environment variables
                username = Config.SOLARWINDS_USERNAME
                password = Config.SOLARWINDS_PASSWORD
                logger.info("solarwinds_credentials_from_env")

        if not (hostname and username and password):
            raise ValueError(
                "SolarWinds credentials not found. Please either:\n"
                "1. Add credentials to Windows Credential Manager: netopsforge creds add solarwinds_api\n"
                "2. Set environment variables: SOLARWINDS_HOSTNAME, SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD\n"
                "3. Pass credentials directly to CMDB constructor"
            )

        # Get SolarWinds configuration
        sw_config = SolarWindsConfig(
            hostname=hostname,
            username=username,
            password=password,
            verify_ssl=self.source_config.get('verify_ssl', Config.SOLARWINDS_VERIFY_SSL),
            timeout=self.source_config.get('timeout', 30),
            cache_ttl=self.source_config.get('cache_ttl', Config.SOLARWINDS_CACHE_TTL)
        )

        # Initialize SolarWinds client
        client = SolarWindsClient(sw_config)

        # Get all nodes
        nodes = client.get_all_nodes()

        # Map nodes to devices
        for node in nodes:
            device_data = SolarWindsDeviceMapper.map_node_to_device(node)

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

        logger.info("devices_loaded_from_solarwinds", count=len(self.devices))
    
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

