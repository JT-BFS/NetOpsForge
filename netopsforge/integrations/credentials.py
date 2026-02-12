"""
Credential Management - Windows Credential Manager integration
"""

import sys
from typing import Optional, Tuple
from dataclasses import dataclass
from ..utils.logging import get_logger

logger = get_logger(__name__)

# Import Windows-specific modules only on Windows
if sys.platform == "win32":
    try:
        import win32cred
        import pywintypes
        WINDOWS_CRED_AVAILABLE = True
    except ImportError:
        logger.warning("pywin32_not_available", message="Windows Credential Manager integration unavailable")
        WINDOWS_CRED_AVAILABLE = False
else:
    WINDOWS_CRED_AVAILABLE = False


@dataclass
class Credential:
    """Network device credential"""
    username: str
    password: str
    enable_password: Optional[str] = None
    
    def __repr__(self) -> str:
        return f"Credential(username={self.username}, password=***)"


class CredentialManager:
    """Manage credentials using Windows Credential Manager"""
    
    PREFIX = "NetOpsForge/"
    
    def __init__(self):
        """Initialize credential manager"""
        if not WINDOWS_CRED_AVAILABLE:
            logger.warning("credential_manager_unavailable", 
                          message="Windows Credential Manager not available on this platform")
        else:
            logger.info("credential_manager_initialized")
    
    def get_credential(self, credential_ref: str) -> Optional[Credential]:
        """
        Get credential from Windows Credential Manager
        
        Args:
            credential_ref: Credential reference name (e.g., "cisco_readonly")
            
        Returns:
            Credential object or None if not found
        """
        if not WINDOWS_CRED_AVAILABLE:
            logger.error("credential_manager_unavailable", credential_ref=credential_ref)
            raise RuntimeError("Windows Credential Manager not available")
        
        target_name = f"{self.PREFIX}{credential_ref}"
        
        try:
            cred = win32cred.CredRead(
                TargetName=target_name,
                Type=win32cred.CRED_TYPE_GENERIC
            )
            
            username = cred['UserName']
            password = cred['CredentialBlob'].decode('utf-16-le')
            
            logger.info("credential_retrieved", credential_ref=credential_ref, username=username)
            
            return Credential(username=username, password=password)
            
        except pywintypes.error as e:
            if e.winerror == 1168:  # ERROR_NOT_FOUND
                logger.error("credential_not_found", credential_ref=credential_ref, target_name=target_name)
                return None
            else:
                logger.error("credential_retrieval_error", credential_ref=credential_ref, error=str(e))
                raise
    
    def store_credential(self, credential_ref: str, username: str, password: str, 
                        comment: Optional[str] = None) -> bool:
        """
        Store credential in Windows Credential Manager
        
        Args:
            credential_ref: Credential reference name
            username: Username
            password: Password
            comment: Optional comment/description
            
        Returns:
            True if successful
        """
        if not WINDOWS_CRED_AVAILABLE:
            logger.error("credential_manager_unavailable", credential_ref=credential_ref)
            raise RuntimeError("Windows Credential Manager not available")
        
        target_name = f"{self.PREFIX}{credential_ref}"
        
        try:
            cred = {
                'Type': win32cred.CRED_TYPE_GENERIC,
                'TargetName': target_name,
                'UserName': username,
                'CredentialBlob': password,
                'Comment': comment or f"NetOpsForge credential: {credential_ref}",
                'Persist': win32cred.CRED_PERSIST_LOCAL_MACHINE
            }
            
            win32cred.CredWrite(cred, 0)
            logger.info("credential_stored", credential_ref=credential_ref, username=username)
            return True
            
        except pywintypes.error as e:
            logger.error("credential_storage_error", credential_ref=credential_ref, error=str(e))
            raise
    
    def delete_credential(self, credential_ref: str) -> bool:
        """
        Delete credential from Windows Credential Manager
        
        Args:
            credential_ref: Credential reference name
            
        Returns:
            True if successful
        """
        if not WINDOWS_CRED_AVAILABLE:
            logger.error("credential_manager_unavailable", credential_ref=credential_ref)
            raise RuntimeError("Windows Credential Manager not available")
        
        target_name = f"{self.PREFIX}{credential_ref}"
        
        try:
            win32cred.CredDelete(
                TargetName=target_name,
                Type=win32cred.CRED_TYPE_GENERIC
            )
            logger.info("credential_deleted", credential_ref=credential_ref)
            return True
            
        except pywintypes.error as e:
            if e.winerror == 1168:  # ERROR_NOT_FOUND
                logger.warning("credential_not_found_for_deletion", credential_ref=credential_ref)
                return False
            else:
                logger.error("credential_deletion_error", credential_ref=credential_ref, error=str(e))
                raise
    
    def list_credentials(self) -> list:
        """
        List all NetOpsForge credentials
        
        Returns:
            List of credential reference names
        """
        if not WINDOWS_CRED_AVAILABLE:
            logger.error("credential_manager_unavailable")
            raise RuntimeError("Windows Credential Manager not available")
        
        try:
            all_creds = win32cred.CredEnumerate(None, 0)
            netopsforge_creds = [
                cred['TargetName'].replace(self.PREFIX, '')
                for cred in all_creds
                if cred['TargetName'].startswith(self.PREFIX)
            ]
            
            logger.info("credentials_listed", count=len(netopsforge_creds))
            return netopsforge_creds
            
        except pywintypes.error as e:
            logger.error("credential_listing_error", error=str(e))
            raise

