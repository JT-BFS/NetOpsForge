"""
Pack Loader - Load and validate automation pack definitions
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PackMetadata:
    """Pack metadata"""
    name: str
    display_name: str
    description: str
    version: str
    category: str
    vendor: str
    platforms: List[str]
    operation_type: str  # read | write
    requires_ticket: bool
    tags: List[str] = field(default_factory=list)


@dataclass
class PackExecution:
    """Pack execution parameters"""
    mode: str  # observe | execute
    timeout_seconds: int = 60
    retry_count: int = 2
    retry_delay_seconds: int = 5
    parallel_execution: bool = False


@dataclass
class PackAuthentication:
    """Pack authentication configuration"""
    credential_ref: str
    connection_type: str  # ssh | telnet | api
    port: Optional[int] = None
    enable_mode: bool = False
    enable_credential_ref: Optional[str] = None


@dataclass
class PackCommand:
    """Pack command definition"""
    name: str
    command: str
    parser: str  # textfsm | regex | raw
    parser_template: Optional[str] = None
    parser_pattern: Optional[str] = None
    timeout_seconds: Optional[int] = None
    expect_string: Optional[str] = None


@dataclass
class PackValidation:
    """Pack validation check"""
    name: str
    field: str
    condition: str
    severity: str  # info | warning | critical
    message: Optional[str] = None


@dataclass
class Pack:
    """Complete automation pack"""
    metadata: PackMetadata
    execution: PackExecution
    authentication: PackAuthentication
    commands: List[PackCommand]
    validations: List[PackValidation] = field(default_factory=list)
    targets: Optional[Dict[str, Any]] = None
    pre_checks: Optional[List[Dict[str, Any]]] = None
    output: Optional[Dict[str, Any]] = None
    linear_integration: Optional[Dict[str, Any]] = None
    cmdb_update: Optional[Dict[str, Any]] = None
    logging: Optional[Dict[str, Any]] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def pack_name(self) -> str:
        """Get pack name"""
        return self.metadata.name


class PackLoader:
    """Load and validate automation packs"""
    
    def __init__(self, packs_dir: Optional[Path] = None):
        """
        Initialize pack loader
        
        Args:
            packs_dir: Directory containing pack files (default: from config)
        """
        self.packs_dir = packs_dir or Config.PACKS_PATH
        logger.info("pack_loader_initialized", packs_dir=str(self.packs_dir))
    
    def load_pack(self, pack_name: str) -> Pack:
        """
        Load a pack by name
        
        Args:
            pack_name: Name of the pack (without .yml extension)
            
        Returns:
            Pack object
            
        Raises:
            FileNotFoundError: If pack file doesn't exist
            ValueError: If pack is invalid
        """
        pack_path = self.packs_dir / f"{pack_name}.yml"
        
        if not pack_path.exists():
            raise FileNotFoundError(f"Pack not found: {pack_path}")
        
        logger.info("loading_pack", pack_name=pack_name, path=str(pack_path))
        
        with open(pack_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return self._parse_pack(data)
    
    def _parse_pack(self, data: Dict[str, Any]) -> Pack:
        """Parse pack data into Pack object"""
        # Parse metadata
        metadata_data = data.get('metadata', {})
        metadata = PackMetadata(
            name=metadata_data['name'],
            display_name=metadata_data['display_name'],
            description=metadata_data['description'],
            version=metadata_data['version'],
            category=metadata_data['category'],
            vendor=metadata_data['vendor'],
            platforms=metadata_data['platforms'],
            operation_type=metadata_data['operation_type'],
            requires_ticket=metadata_data['requires_ticket'],
            tags=metadata_data.get('tags', [])
        )
        
        # Parse execution
        exec_data = data.get('execution', {})
        execution = PackExecution(
            mode=exec_data.get('mode', 'observe'),
            timeout_seconds=exec_data.get('timeout_seconds', 60),
            retry_count=exec_data.get('retry_count', 2),
            retry_delay_seconds=exec_data.get('retry_delay_seconds', 5),
            parallel_execution=exec_data.get('parallel_execution', False)
        )
        
        # Parse authentication
        auth_data = data.get('authentication', {})
        authentication = PackAuthentication(
            credential_ref=auth_data['credential_ref'],
            connection_type=auth_data['connection_type'],
            port=auth_data.get('port'),
            enable_mode=auth_data.get('enable_mode', False),
            enable_credential_ref=auth_data.get('enable_credential_ref')
        )

        # Parse commands
        commands_data = data.get('commands', [])
        commands = [
            PackCommand(
                name=cmd['name'],
                command=cmd['command'],
                parser=cmd['parser'],
                parser_template=cmd.get('parser_template'),
                parser_pattern=cmd.get('parser_pattern'),
                timeout_seconds=cmd.get('timeout_seconds'),
                expect_string=cmd.get('expect_string')
            )
            for cmd in commands_data
        ]

        # Parse validations
        validations_data = data.get('validation', {}).get('checks', [])
        validations = [
            PackValidation(
                name=val['name'],
                field=val['field'],
                condition=val['condition'],
                severity=val['severity'],
                message=val.get('message')
            )
            for val in validations_data
        ]

        # Create pack
        pack = Pack(
            metadata=metadata,
            execution=execution,
            authentication=authentication,
            commands=commands,
            validations=validations,
            targets=data.get('targets'),
            pre_checks=data.get('pre_checks'),
            output=data.get('output'),
            linear_integration=data.get('linear_integration'),
            cmdb_update=data.get('cmdb_update'),
            logging=data.get('logging'),
            raw_data=data
        )

        logger.info("pack_loaded", pack_name=pack.pack_name, version=pack.metadata.version)
        return pack

    def list_packs(self) -> List[str]:
        """
        List all available packs

        Returns:
            List of pack names
        """
        if not self.packs_dir.exists():
            return []

        packs = [
            p.stem for p in self.packs_dir.glob("*.yml")
            if not p.name.startswith("_") and p.name != "README.md"
        ]

        logger.info("packs_listed", count=len(packs), packs=packs)
        return sorted(packs)

    def validate_pack(self, pack: Pack) -> List[str]:
        """
        Validate a pack for common issues

        Args:
            pack: Pack to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        if not pack.metadata.name:
            errors.append("Pack name is required")

        if not pack.commands:
            errors.append("Pack must have at least one command")

        # Check operation type
        if pack.metadata.operation_type not in ['read', 'write']:
            errors.append(f"Invalid operation_type: {pack.metadata.operation_type}")

        # Check execution mode
        if pack.execution.mode not in ['observe', 'execute']:
            errors.append(f"Invalid execution mode: {pack.execution.mode}")

        # Check connection type
        if pack.authentication.connection_type not in ['ssh', 'telnet', 'api']:
            errors.append(f"Invalid connection_type: {pack.authentication.connection_type}")

        # Check parser types
        for cmd in pack.commands:
            if cmd.parser not in ['textfsm', 'regex', 'raw']:
                errors.append(f"Invalid parser for command '{cmd.name}': {cmd.parser}")

            if cmd.parser == 'textfsm' and not cmd.parser_template:
                errors.append(f"Command '{cmd.name}' uses textfsm but no parser_template specified")

            if cmd.parser == 'regex' and not cmd.parser_pattern:
                errors.append(f"Command '{cmd.name}' uses regex but no parser_pattern specified")

        # Check validation severities
        for val in pack.validations:
            if val.severity not in ['info', 'warning', 'critical']:
                errors.append(f"Invalid severity for validation '{val.name}': {val.severity}")

        if errors:
            logger.warning("pack_validation_failed", pack_name=pack.pack_name, errors=errors)
        else:
            logger.info("pack_validation_passed", pack_name=pack.pack_name)

        return errors

