"""
SolarWinds Orion CMDB Integration

This module provides integration with SolarWinds Orion as a CMDB source.
It queries the Orion API to retrieve network device inventory and maps
it to the NetOpsForge device schema.

Credentials can be stored in:
1. Windows Credential Manager (recommended for security)
2. Environment variables (for testing/development)
"""

import logging
import os
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def get_solarwinds_credentials(credential_ref: str = "solarwinds_api") -> tuple[Optional[str], Optional[str]]:
    """
    Get SolarWinds credentials from Windows Credential Manager

    Args:
        credential_ref: Credential reference name in Windows Credential Manager

    Returns:
        Tuple of (username, password) or (None, None) if not found
    """
    try:
        from ..integrations.credentials import CredentialManager

        cred_manager = CredentialManager()
        cred = cred_manager.get_credential(credential_ref)

        if cred:
            logger.info(f"Retrieved SolarWinds credentials from Windows Credential Manager: {credential_ref}")
            return cred.username, cred.password
        else:
            logger.warning(f"SolarWinds credentials not found in Windows Credential Manager: {credential_ref}")
            return None, None

    except Exception as e:
        logger.warning(f"Failed to retrieve credentials from Windows Credential Manager: {e}")
        return None, None


@dataclass
class SolarWindsConfig:
    """SolarWinds Orion connection configuration"""
    hostname: str
    username: str
    password: str
    verify_ssl: bool = True
    timeout: int = 30
    cache_ttl: int = 300  # Cache TTL in seconds (5 minutes default)


class SolarWindsClient:
    """
    Client for interacting with SolarWinds Orion API

    Uses the Orion REST API (SWIS - SolarWinds Information Service)
    to query device inventory.
    """

    def __init__(self, config: SolarWindsConfig):
        """
        Initialize SolarWinds client

        Args:
            config: SolarWinds connection configuration
        """
        self.config = config

        # Import the official SolarWinds SDK
        try:
            from orionsdk import SwisClient
        except ImportError:
            raise ImportError("SolarWinds integration requires 'orionsdk' package. Install with: pip install orionsdk")

        # Initialize SwisClient
        self.swis = SwisClient(
            config.hostname,
            config.username,
            config.password,
            verify=config.verify_ssl
        )

        # Cache for device queries
        self._cache: Dict[str, Any] = {}
        self._cache_timestamp: Optional[datetime] = None

        logger.info(f"Initialized SolarWinds client for {config.hostname}")
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        if self._cache_timestamp is None:
            return False
        
        age = datetime.now() - self._cache_timestamp
        return age.total_seconds() < self.config.cache_ttl
    
    def _swql_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SWQL (SolarWinds Query Language) query

        Args:
            query: SWQL query string

        Returns:
            List of result dictionaries
        """
        try:
            logger.debug(f"Executing SWQL query: {query}")
            results = self.swis.query(query)

            # The SwisClient returns a dict with 'results' key
            if isinstance(results, dict) and 'results' in results:
                results = results['results']

            logger.info(f"SWQL query returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"SolarWinds API error: {e}")
            raise ConnectionError(f"Failed to query SolarWinds: {e}")
    
    def discover_custom_properties(self) -> List[str]:
        """
        Discover available custom properties in SolarWinds

        Returns:
            List of custom property names
        """
        # Check cache first
        if 'custom_properties' in self._cache:
            logger.debug("Returning cached custom properties")
            return self._cache['custom_properties']

        query = """
        SELECT Name, Type
        FROM Metadata.Property
        WHERE EntityName = 'Orion.NodesCustomProperties'
        """

        try:
            results = self._swql_query(query)
            custom_props = [row['Name'] for row in results]

            # Cache the results
            self._cache['custom_properties'] = custom_props

            logger.info(f"Discovered {len(custom_props)} custom properties: {custom_props}")
            return custom_props

        except Exception as e:
            logger.warning(f"Failed to discover custom properties: {e}")
            return []

    def get_all_nodes(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get all network nodes from SolarWinds

        Args:
            use_cache: Whether to use cached results

        Returns:
            List of node dictionaries
        """
        # Check cache first
        if use_cache and self._is_cache_valid() and 'nodes' in self._cache:
            logger.debug("Returning cached nodes")
            return self._cache['nodes']

        # Discover available custom properties
        available_custom_props = self.discover_custom_properties()

        # Build SELECT clause with standard fields
        select_fields = [
            "n.NodeID",
            "n.Caption AS Hostname",
            "n.IPAddress",
            "n.MachineType",
            "n.Vendor",
            "n.IOSVersion",
            "n.Location",
            "n.Contact",
            "n.Description",
            "n.Status",
            "n.StatusDescription",
            "n.UnManaged",
            "n.UnManageFrom",
            "n.UnManageUntil"
        ]

        # Add custom properties if they exist
        desired_custom_props = ['Site', 'DeviceRole', 'Platform', 'Model',
                               'SerialNumber', 'Rack', 'CredentialRef', 'Tags']

        for prop in desired_custom_props:
            if prop in available_custom_props:
                select_fields.append(f"n.CustomProperties.{prop}")
                logger.debug(f"Including custom property: {prop}")
            else:
                logger.debug(f"Skipping unavailable custom property: {prop}")

        # Build dynamic query
        query = f"""
        SELECT {', '.join(select_fields)}
        FROM Orion.Nodes n
        WHERE n.Vendor IN ('Cisco', 'Arista', 'Juniper', 'HP', 'Dell')
        ORDER BY n.Caption
        """

        logger.debug(f"Executing dynamic SWQL query with {len(select_fields)} fields")
        nodes = self._swql_query(query)

        # Update cache
        self._cache['nodes'] = nodes
        self._cache_timestamp = datetime.now()

        return nodes

    def get_node_by_hostname(self, hostname: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific node by hostname

        Args:
            hostname: Node hostname/caption

        Returns:
            Node dictionary or None if not found
        """
        # Discover available custom properties
        available_custom_props = self.discover_custom_properties()

        # Build SELECT clause with standard fields
        select_fields = [
            "n.NodeID",
            "n.Caption AS Hostname",
            "n.IPAddress",
            "n.MachineType",
            "n.Vendor",
            "n.IOSVersion",
            "n.Location",
            "n.Contact",
            "n.Description",
            "n.Status",
            "n.StatusDescription"
        ]

        # Add custom properties if they exist
        desired_custom_props = ['Site', 'DeviceRole', 'Platform', 'Model',
                               'SerialNumber', 'Rack', 'CredentialRef', 'Tags']

        for prop in desired_custom_props:
            if prop in available_custom_props:
                select_fields.append(f"n.CustomProperties.{prop}")

        # Build dynamic query
        query = f"""
        SELECT {', '.join(select_fields)}
        FROM Orion.Nodes n
        WHERE n.Caption = '{hostname}'
        """

        results = self._swql_query(query)
        return results[0] if results else None

    def query_nodes(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query nodes with filters

        Args:
            filters: Dictionary of filter criteria
                - vendor: Vendor name
                - platform: Platform type
                - site: Site location
                - device_role: Device role
                - status: Node status

        Returns:
            List of matching nodes
        """
        # Discover available custom properties
        available_custom_props = self.discover_custom_properties()

        # Build WHERE clause from filters
        conditions = []

        if 'vendor' in filters:
            conditions.append(f"n.Vendor = '{filters['vendor']}'")

        if 'platform' in filters and 'Platform' in available_custom_props:
            conditions.append(f"n.CustomProperties.Platform = '{filters['platform']}'")

        if 'site' in filters and 'Site' in available_custom_props:
            conditions.append(f"n.CustomProperties.Site = '{filters['site']}'")

        if 'device_role' in filters and 'DeviceRole' in available_custom_props:
            conditions.append(f"n.CustomProperties.DeviceRole = '{filters['device_role']}'")

        if 'status' in filters:
            status_map = {
                'up': 1,
                'down': 2,
                'warning': 3,
                'unknown': 0
            }
            status_value = status_map.get(filters['status'].lower(), 1)
            conditions.append(f"n.Status = {status_value}")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        # Build SELECT clause with standard fields
        select_fields = [
            "n.NodeID",
            "n.Caption AS Hostname",
            "n.IPAddress",
            "n.MachineType",
            "n.Vendor",
            "n.IOSVersion",
            "n.Location"
        ]

        # Add custom properties if they exist
        desired_custom_props = ['Site', 'DeviceRole', 'Platform', 'Model',
                               'SerialNumber', 'Rack', 'CredentialRef', 'Tags']

        for prop in desired_custom_props:
            if prop in available_custom_props:
                select_fields.append(f"n.CustomProperties.{prop}")

        query = f"""
        SELECT {', '.join(select_fields)}
        FROM Orion.Nodes n
        WHERE {where_clause}
        ORDER BY n.Caption
        """

        return self._swql_query(query)

    def clear_cache(self):
        """Clear the device cache"""
        self._cache.clear()
        self._cache_timestamp = None
        logger.info("SolarWinds cache cleared")


class SolarWindsDeviceMapper:
    """
    Maps SolarWinds node data to NetOpsForge device schema
    """

    # Platform mapping from SolarWinds to NetOpsForge
    PLATFORM_MAP = {
        'IOS': 'ios',
        'IOS-XE': 'ios-xe',
        'NX-OS': 'nxos',
        'ASA': 'asa',
        'JunOS': 'junos',
        'EOS': 'eos',
    }

    # Vendor normalization
    VENDOR_MAP = {
        'Cisco Systems': 'cisco',
        'Cisco': 'cisco',
        'Arista Networks': 'arista',
        'Arista': 'arista',
        'Juniper Networks': 'juniper',
        'Juniper': 'juniper',
    }

    @staticmethod
    def map_node_to_device(node: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map a SolarWinds node to NetOpsForge device format

        Args:
            node: SolarWinds node dictionary

        Returns:
            NetOpsForge device dictionary
        """
        # Normalize vendor
        vendor = node.get('Vendor', 'unknown')
        vendor = SolarWindsDeviceMapper.VENDOR_MAP.get(vendor, vendor.lower())

        # Normalize platform
        platform = node.get('Platform') or SolarWindsDeviceMapper._infer_platform(node)
        platform = SolarWindsDeviceMapper.PLATFORM_MAP.get(platform, platform.lower() if platform else 'unknown')

        # Parse tags from comma-separated string or list
        tags_raw = node.get('Tags', '')
        if isinstance(tags_raw, str):
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
        elif isinstance(tags_raw, list):
            tags = tags_raw
        else:
            tags = []

        # Add status-based tags
        if node.get('Status') == 1:  # Up
            tags.append('online')

        # Determine device type from role or machine type
        device_type = SolarWindsDeviceMapper._infer_device_type(node)

        # Build NetOpsForge device
        device = {
            'hostname': node.get('Hostname', ''),
            'management_ip': node.get('IPAddress', ''),
            'device_type': device_type,
            'device_role': node.get('DeviceRole', 'unknown'),
            'vendor': vendor,
            'platform': platform,
            'model': node.get('Model', node.get('MachineType', '')),
            'site': node.get('Site', node.get('Location', '')),
            'rack': node.get('Rack', ''),
            'serial_number': node.get('SerialNumber', ''),
            'tags': tags,
            'credential_ref': node.get('CredentialRef', 'default'),

            # Additional metadata from SolarWinds
            'solarwinds_node_id': node.get('NodeID'),
            'solarwinds_status': node.get('StatusDescription', ''),
            'ios_version': node.get('IOSVersion', ''),
            'description': node.get('Description', ''),
            'contact': node.get('Contact', ''),
        }

        return device

    @staticmethod
    def _infer_platform(node: Dict[str, Any]) -> str:
        """Infer platform from IOSVersion or MachineType"""
        ios_version = node.get('IOSVersion', '').upper()
        machine_type = node.get('MachineType', '').upper()

        if 'NX-OS' in ios_version or 'NXOS' in machine_type:
            return 'NX-OS'
        elif 'IOS-XE' in ios_version or 'IOS XE' in ios_version:
            return 'IOS-XE'
        elif 'IOS' in ios_version:
            return 'IOS'
        elif 'ASA' in machine_type:
            return 'ASA'
        elif 'JUNOS' in ios_version:
            return 'JunOS'
        elif 'EOS' in ios_version:
            return 'EOS'

        return 'unknown'

    @staticmethod
    def _infer_device_type(node: Dict[str, Any]) -> str:
        """Infer device type from role or machine type"""
        role = node.get('DeviceRole', '').lower()
        machine_type = node.get('MachineType', '').lower()

        if 'router' in role or 'rtr' in role:
            return 'router'
        elif 'switch' in role or 'sw' in role:
            return 'switch'
        elif 'firewall' in role or 'fw' in role or 'asa' in machine_type:
            return 'firewall'
        elif 'router' in machine_type:
            return 'router'
        elif 'switch' in machine_type:
            return 'switch'

        return 'unknown'

