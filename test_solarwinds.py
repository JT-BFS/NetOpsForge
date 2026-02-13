"""
Test script for SolarWinds CMDB integration

This script tests the SolarWinds Orion integration by:
1. Connecting to SolarWinds API
2. Retrieving device inventory
3. Mapping devices to NetOpsForge schema
4. Displaying results

Usage:
    python test_solarwinds.py --hostname <solarwinds-server> --username <user> --password <pass>
    
Or set environment variables:
    SOLARWINDS_HOSTNAME=solarwinds.company.com
    SOLARWINDS_USERNAME=netops_readonly
    SOLARWINDS_PASSWORD=your_password
    python test_solarwinds.py
"""

import sys
import os
import argparse
from pathlib import Path

# Add netopsforge to path
sys.path.insert(0, str(Path(__file__).parent))

from netopsforge.integrations.solarwinds import SolarWindsClient, SolarWindsConfig, SolarWindsDeviceMapper
from netopsforge.core.cmdb import CMDB
from netopsforge.utils.logging import get_logger
import json

logger = get_logger(__name__)


def test_solarwinds_client(hostname: str, username: str, password: str, verify_ssl: bool = True):
    """Test SolarWinds client directly"""
    print("\n" + "="*80)
    print("TEST 1: SolarWinds Client Connection")
    print("="*80)
    
    try:
        # Create config
        config = SolarWindsConfig(
            hostname=hostname,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            timeout=30,
            cache_ttl=300
        )
        
        print(f"✓ Config created for {hostname}")
        
        # Create client
        client = SolarWindsClient(config)
        print(f"✓ Client initialized")
        
        # Get all nodes
        print(f"\nQuerying SolarWinds for network devices...")
        nodes = client.get_all_nodes(use_cache=False)
        
        print(f"✓ Retrieved {len(nodes)} nodes from SolarWinds")
        
        # Display first few nodes
        if nodes:
            print(f"\nFirst 5 nodes:")
            for i, node in enumerate(nodes[:5], 1):
                print(f"\n  {i}. {node.get('Hostname', 'N/A')}")
                print(f"     IP: {node.get('IPAddress', 'N/A')}")
                print(f"     Vendor: {node.get('Vendor', 'N/A')}")
                print(f"     Platform: {node.get('Platform', 'N/A')}")
                print(f"     Role: {node.get('DeviceRole', 'N/A')}")
        
        return True, nodes
        
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error("solarwinds_client_test_failed", error=str(e))
        return False, []


def test_device_mapping(nodes):
    """Test device mapping from SolarWinds to NetOpsForge schema"""
    print("\n" + "="*80)
    print("TEST 2: Device Mapping")
    print("="*80)
    
    try:
        if not nodes:
            print("⚠ No nodes to map")
            return False
        
        print(f"Mapping {len(nodes)} nodes to NetOpsForge schema...")
        
        mapped_devices = []
        for node in nodes:
            device = SolarWindsDeviceMapper.map_node_to_device(node)
            mapped_devices.append(device)
        
        print(f"✓ Mapped {len(mapped_devices)} devices")
        
        # Display first few mapped devices
        if mapped_devices:
            print(f"\nFirst 3 mapped devices:")
            for i, device in enumerate(mapped_devices[:3], 1):
                print(f"\n  {i}. {device.get('hostname', 'N/A')}")
                print(f"     Management IP: {device.get('management_ip', 'N/A')}")
                print(f"     Vendor: {device.get('vendor', 'N/A')}")
                print(f"     Platform: {device.get('platform', 'N/A')}")
                print(f"     Device Type: {device.get('device_type', 'N/A')}")
                print(f"     Device Role: {device.get('device_role', 'N/A')}")
                print(f"     Site: {device.get('site', 'N/A')}")
                print(f"     Credential Ref: {device.get('credential_ref', 'N/A')}")
                print(f"     Tags: {device.get('tags', [])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error("device_mapping_test_failed", error=str(e))
        return False


def test_cmdb_integration(hostname: str, username: str, password: str, verify_ssl: bool = True):
    """Test CMDB integration with SolarWinds source"""
    print("\n" + "="*80)
    print("TEST 3: CMDB Integration")
    print("="*80)
    
    try:
        print(f"Initializing CMDB with SolarWinds source...")
        
        cmdb = CMDB(
            source='solarwinds',
            hostname=hostname,
            username=username,
            password=password,
            verify_ssl=verify_ssl
        )
        
        print(f"✓ CMDB initialized with {len(cmdb.devices)} devices")
        
        # Test queries
        print(f"\nTesting CMDB queries...")
        
        # Query by vendor
        cisco_devices = cmdb.query_devices(vendor='cisco')
        print(f"  - Cisco devices: {len(cisco_devices)}")
        
        # Query by platform
        ios_devices = cmdb.query_devices(platform='ios')
        print(f"  - IOS devices: {len(ios_devices)}")

        # List all devices
        all_devices = cmdb.list_devices()
        print(f"  - Total devices: {len(all_devices)}")

        # Get specific device
        if all_devices:
            first_device = all_devices[0]
            found_device = cmdb.get_device(first_device.hostname)
            if found_device:
                print(f"  - Successfully retrieved device: {found_device.hostname}")

        print(f"✓ CMDB integration working correctly")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error("cmdb_integration_test_failed", error=str(e))
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    parser = argparse.ArgumentParser(description='Test SolarWinds CMDB integration')
    parser.add_argument('--hostname', help='SolarWinds hostname')
    parser.add_argument('--username', help='SolarWinds username')
    parser.add_argument('--password', help='SolarWinds password')
    parser.add_argument('--credential-ref', default='solarwinds_api', help='Windows Credential Manager reference (default: solarwinds_api)')
    parser.add_argument('--no-verify-ssl', action='store_true', help='Disable SSL verification')

    args = parser.parse_args()

    # Get hostname from args or environment
    hostname = args.hostname or os.getenv('SOLARWINDS_HOSTNAME')

    # Get credentials - try in this order:
    # 1. Command line arguments
    # 2. Windows Credential Manager
    # 3. Environment variables
    username = args.username
    password = args.password

    if not (username and password):
        # Try Windows Credential Manager
        try:
            from netopsforge.integrations.solarwinds import get_solarwinds_credentials
            cred_username, cred_password = get_solarwinds_credentials(args.credential_ref)
            if cred_username and cred_password:
                username = cred_username
                password = cred_password
                print(f"✓ Using credentials from Windows Credential Manager: {args.credential_ref}")
        except Exception as e:
            print(f"⚠ Could not retrieve credentials from Windows Credential Manager: {e}")

    if not (username and password):
        # Fall back to environment variables
        username = os.getenv('SOLARWINDS_USERNAME')
        password = os.getenv('SOLARWINDS_PASSWORD')
        if username and password:
            print("✓ Using credentials from environment variables")

    # SSL verification: command line flag takes precedence, then environment variable
    if args.no_verify_ssl:
        verify_ssl = False
    else:
        verify_ssl = os.getenv('SOLARWINDS_VERIFY_SSL', 'true').lower() == 'true'

    if not all([hostname, username, password]):
        print("ERROR: Missing SolarWinds credentials!")
        print("\nProvide credentials via:")
        print("  1. Windows Credential Manager (recommended):")
        print("     .\\scripts\\setup-solarwinds-creds.ps1")
        print("\n  2. Command line: --hostname <host> --username <user> --password <pass>")
        print("\n  3. Environment variables: SOLARWINDS_HOSTNAME, SOLARWINDS_USERNAME, SOLARWINDS_PASSWORD")
        print("\nExample:")
        print("  python test_solarwinds.py")
        print("  python test_solarwinds.py --hostname orion --no-verify-ssl")
        sys.exit(1)

    print("\n" + "="*80)
    print("SolarWinds CMDB Integration Test Suite")
    print("="*80)
    print(f"Hostname: {hostname}")
    print(f"Username: {username}")
    print(f"SSL Verification: {verify_ssl}")

    # Run tests
    results = []

    # Test 1: SolarWinds Client
    success, nodes = test_solarwinds_client(hostname, username, password, verify_ssl)
    results.append(("SolarWinds Client Connection", success))

    if success and nodes:
        # Test 2: Device Mapping
        success = test_device_mapping(nodes)
        results.append(("Device Mapping", success))

        # Test 3: CMDB Integration
        success = test_cmdb_integration(hostname, username, password, verify_ssl)
        results.append(("CMDB Integration", success))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(success for _, success in results)

    if all_passed:
        print("\n🎉 All tests passed! SolarWinds integration is working correctly.")
        return 0
    else:
        print("\n⚠ Some tests failed. Check the output above for details.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

