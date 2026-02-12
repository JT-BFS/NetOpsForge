"""
Connection Manager - Handle device connections via SSH/Telnet
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from ..core.cmdb import Device
from ..integrations.credentials import CredentialManager, Credential
from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ConnectionResult:
    """Result of a connection attempt"""
    success: bool
    message: str
    connection: Optional[Any] = None
    error: Optional[str] = None


class ConnectionManager:
    """Manage device connections"""
    
    # Map NetOpsForge platform names to Netmiko device types
    PLATFORM_MAP = {
        'ios': 'cisco_ios',
        'ios-xe': 'cisco_xe',
        'nxos': 'cisco_nxos',
        'asa': 'cisco_asa',
        'junos': 'juniper_junos',
        'eos': 'arista_eos',
    }
    
    def __init__(self, credential_manager: Optional[CredentialManager] = None):
        """
        Initialize connection manager
        
        Args:
            credential_manager: Credential manager instance
        """
        self.credential_manager = credential_manager or CredentialManager()
        logger.info("connection_manager_initialized")
    
    def connect(self, device: Device, credential_ref: Optional[str] = None,
                port: Optional[int] = None, timeout: Optional[int] = None) -> ConnectionResult:
        """
        Connect to a device
        
        Args:
            device: Device object from CMDB
            credential_ref: Credential reference (default: from device)
            port: SSH/Telnet port (default: 22 for SSH)
            timeout: Connection timeout in seconds
            
        Returns:
            ConnectionResult object
        """
        # Get credential
        cred_ref = credential_ref or device.credential_ref
        credential = self.credential_manager.get_credential(cred_ref)
        
        if not credential:
            return ConnectionResult(
                success=False,
                message=f"Credential not found: {cred_ref}",
                error="CREDENTIAL_NOT_FOUND"
            )
        
        # Map platform to Netmiko device type
        device_type = self.PLATFORM_MAP.get(device.platform)
        if not device_type:
            return ConnectionResult(
                success=False,
                message=f"Unsupported platform: {device.platform}",
                error="UNSUPPORTED_PLATFORM"
            )
        
        # Build connection parameters
        connection_params = {
            'device_type': device_type,
            'host': device.management_ip,
            'username': credential.username,
            'password': credential.password,
            'port': port or Config.DEFAULT_SSH_PORT,
            'timeout': timeout or Config.DEFAULT_CONNECTION_TIMEOUT,
            'session_log': None,  # Can be enabled for debugging
        }
        
        # Add enable password if available
        if credential.enable_password:
            connection_params['secret'] = credential.enable_password
        
        logger.info("connecting_to_device", 
                   hostname=device.hostname,
                   ip=device.management_ip,
                   platform=device.platform,
                   device_type=device_type)
        
        try:
            connection = ConnectHandler(**connection_params)
            
            logger.info("connection_successful",
                       hostname=device.hostname,
                       ip=device.management_ip)
            
            return ConnectionResult(
                success=True,
                message=f"Connected to {device.hostname}",
                connection=connection
            )
            
        except NetmikoTimeoutException as e:
            logger.error("connection_timeout",
                        hostname=device.hostname,
                        ip=device.management_ip,
                        error=str(e))
            return ConnectionResult(
                success=False,
                message=f"Connection timeout to {device.hostname}",
                error="TIMEOUT"
            )
            
        except NetmikoAuthenticationException as e:
            logger.error("authentication_failed",
                        hostname=device.hostname,
                        ip=device.management_ip,
                        error=str(e))
            return ConnectionResult(
                success=False,
                message=f"Authentication failed for {device.hostname}",
                error="AUTH_FAILED"
            )
            
        except Exception as e:
            logger.error("connection_error",
                        hostname=device.hostname,
                        ip=device.management_ip,
                        error=str(e),
                        error_type=type(e).__name__)
            return ConnectionResult(
                success=False,
                message=f"Connection error: {str(e)}",
                error="CONNECTION_ERROR"
            )
    
    def disconnect(self, connection: Any):
        """
        Disconnect from a device
        
        Args:
            connection: Netmiko connection object
        """
        try:
            if connection:
                connection.disconnect()
                logger.info("disconnected")
        except Exception as e:
            logger.warning("disconnect_error", error=str(e))
    
    def execute_command(self, connection: Any, command: str,
                       timeout: Optional[int] = None) -> str:
        """
        Execute a command on a device
        
        Args:
            connection: Netmiko connection object
            command: Command to execute
            timeout: Command timeout in seconds
            
        Returns:
            Command output
        """
        try:
            logger.debug("executing_command", command=command)
            output = connection.send_command(
                command,
                read_timeout=timeout or Config.DEFAULT_COMMAND_TIMEOUT
            )
            logger.debug("command_executed", command=command, output_length=len(output))
            return output
            
        except Exception as e:
            logger.error("command_execution_error", command=command, error=str(e))
            raise

