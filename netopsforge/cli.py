"""
NetOpsForge CLI - Command-line interface for network automation
"""

import click
import sys
from pathlib import Path
from typing import Optional
from .core.pack_loader import PackLoader
from .core.cmdb import CMDB
from .core.runner import PackRunner
from .core.reporter import Reporter
from .integrations.credentials import CredentialManager
from .utils.config import Config
from .utils.logging import setup_logging, get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    NetOpsForge - Network Operations Automation Platform
    
    A governance-first automation platform for network operations.
    """
    # Ensure required directories exist
    Config.ensure_directories()


@cli.command()
@click.argument('pack_name')
@click.argument('device_hostname')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'markdown', 'csv']), 
              default='markdown', help='Output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--dry-run', is_flag=True, help='Validate without executing')
def run(pack_name: str, device_hostname: str, format: str, 
        output: Optional[str], dry_run: bool):
    """
    Run an automation pack against a device
    
    Examples:
    
        netopsforge run cisco-ios-health-check core-rtr-01
        
        netopsforge run cisco-ios-health-check core-rtr-01 --format json --output report.json
        
        netopsforge run cisco-ios-health-check core-rtr-01 --dry-run
    """
    try:
        click.echo(f"🚀 Running pack '{pack_name}' on device '{device_hostname}'...")
        
        if dry_run:
            click.echo("⚠️  DRY RUN MODE - No commands will be executed")
        
        # Initialize runner
        runner = PackRunner()
        
        # Execute pack
        result = runner.run_pack(pack_name, device_hostname, dry_run=dry_run)
        
        # Check result
        if not result.success:
            click.echo(f"❌ Execution failed: {result.error}", err=True)
            sys.exit(1)
        
        # Generate report
        report_data = {
            'pack': {'name': result.pack_name},
            'device': {'hostname': result.device_hostname},
            'execution': {
                'start_time': result.start_time.isoformat(),
                'end_time': result.end_time.isoformat(),
                'duration_seconds': result.duration_seconds,
                'commands_executed': result.commands_executed
            },
            'results': result.command_results,
            'validations': [
                {
                    'validation_name': v.validation_name,
                    'field': v.field,
                    'expected': v.expected,
                    'actual': v.actual,
                    'passed': v.passed,
                    'severity': v.severity,
                    'message': v.message
                }
                for v in result.validation_results
            ]
        }
        
        reporter = Reporter()
        report_content = reporter.generate_report(
            report_data,
            format=format,
            output_file=Path(output) if output else None
        )
        
        # Print summary
        click.echo(f"\n✅ Execution completed in {result.duration_seconds:.2f}s")
        click.echo(f"   Commands executed: {result.commands_executed}")
        click.echo(f"   Validations: {result.validations_passed} passed, {result.validations_failed} failed")
        
        if output:
            click.echo(f"   Report saved to: {output}")
        else:
            click.echo(f"\n{report_content}")
        
    except Exception as e:
        logger.error("cli_run_error", error=str(e), error_type=type(e).__name__)
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def list():
    """List available resources"""
    pass


@list.command(name='packs')
def list_packs():
    """List all available automation packs"""
    try:
        pack_loader = PackLoader()
        packs = pack_loader.list_packs()
        
        if not packs:
            click.echo("No packs found")
            return
        
        click.echo(f"📦 Available Packs ({len(packs)}):\n")
        for pack_name in packs:
            try:
                pack = pack_loader.load_pack(pack_name)
                click.echo(f"  • {pack.metadata.display_name}")
                click.echo(f"    Name: {pack.metadata.name}")
                click.echo(f"    Version: {pack.metadata.version}")
                click.echo(f"    Platform: {', '.join(pack.metadata.platforms)}")
                click.echo(f"    Type: {pack.metadata.operation_type}")
                click.echo()
            except Exception as e:
                click.echo(f"  • {pack_name} (error loading: {str(e)})")
                click.echo()
        
    except Exception as e:
        logger.error("cli_list_packs_error", error=str(e))
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@list.command(name='devices')
@click.option('--vendor', help='Filter by vendor')
@click.option('--platform', help='Filter by platform')
@click.option('--tag', help='Filter by tag')
def list_devices(vendor: Optional[str], platform: Optional[str], tag: Optional[str]):
    """List devices from CMDB"""
    try:
        cmdb = CMDB()
        
        # Build filters
        filters = {}
        if vendor:
            filters['vendor'] = vendor
        if platform:
            filters['platform'] = platform
        if tag:
            filters['tags'] = tag
        
        # Query devices
        if filters:
            devices = cmdb.query_devices(**filters)
        else:
            devices = cmdb.list_devices()

        if not devices:
            click.echo("No devices found")
            return

        click.echo(f"🖥️  Devices ({len(devices)}):\n")
        for device in devices:
            click.echo(f"  • {device.hostname}")
            click.echo(f"    IP: {device.management_ip}")
            click.echo(f"    Platform: {device.vendor} {device.platform}")
            click.echo(f"    Role: {device.device_role}")
            if device.tags:
                click.echo(f"    Tags: {', '.join(device.tags)}")
            click.echo()

    except Exception as e:
        logger.error("cli_list_devices_error", error=str(e))
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('pack_name')
def validate(pack_name: str):
    """Validate an automation pack"""
    try:
        click.echo(f"🔍 Validating pack '{pack_name}'...")

        pack_loader = PackLoader()
        pack = pack_loader.load_pack(pack_name)

        errors = pack_loader.validate_pack(pack)

        if errors:
            click.echo(f"\n❌ Validation failed with {len(errors)} error(s):\n")
            for error in errors:
                click.echo(f"  • {error}")
            sys.exit(1)
        else:
            click.echo(f"\n✅ Pack is valid!")
            click.echo(f"   Name: {pack.metadata.display_name}")
            click.echo(f"   Version: {pack.metadata.version}")
            click.echo(f"   Commands: {len(pack.commands)}")
            click.echo(f"   Validations: {len(pack.validations)}")

    except FileNotFoundError:
        click.echo(f"❌ Pack not found: {pack_name}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error("cli_validate_error", error=str(e))
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def creds():
    """Manage credentials in Windows Credential Manager"""
    pass


@creds.command(name='list')
def creds_list():
    """List all NetOpsForge credentials"""
    try:
        cred_manager = CredentialManager()
        credentials = cred_manager.list_credentials()

        if not credentials:
            click.echo("No credentials found")
            return

        click.echo(f"🔑 Credentials ({len(credentials)}):\n")
        for cred_ref in credentials:
            click.echo(f"  • {cred_ref}")

    except Exception as e:
        logger.error("cli_creds_list_error", error=str(e))
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@creds.command(name='add')
@click.argument('credential_ref')
@click.option('--username', '-u', prompt=True, help='Username')
@click.option('--password', '-p', prompt=True, hide_input=True,
              confirmation_prompt=True, help='Password')
def creds_add(credential_ref: str, username: str, password: str):
    """Add a new credential"""
    try:
        cred_manager = CredentialManager()
        cred_manager.store_credential(credential_ref, username, password)
        click.echo(f"✅ Credential '{credential_ref}' stored successfully")

    except Exception as e:
        logger.error("cli_creds_add_error", error=str(e))
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@creds.command(name='delete')
@click.argument('credential_ref')
@click.confirmation_option(prompt='Are you sure you want to delete this credential?')
def creds_delete(credential_ref: str):
    """Delete a credential"""
    try:
        cred_manager = CredentialManager()
        if cred_manager.delete_credential(credential_ref):
            click.echo(f"✅ Credential '{credential_ref}' deleted successfully")
        else:
            click.echo(f"⚠️  Credential '{credential_ref}' not found")

    except Exception as e:
        logger.error("cli_creds_delete_error", error=str(e))
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()

