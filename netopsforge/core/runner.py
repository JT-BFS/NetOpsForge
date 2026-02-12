"""
Pack Runner - Execute automation packs against devices
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from ..core.pack_loader import Pack, PackLoader
from ..core.cmdb import CMDB, Device
from ..core.connection import ConnectionManager
from ..core.parser import ParserEngine
from ..core.validator import ValidationEngine, ValidationResult
from ..core.reporter import Reporter
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ExecutionResult:
    """Result of pack execution"""
    pack_name: str
    device_hostname: str
    success: bool
    start_time: datetime
    end_time: datetime
    commands_executed: int = 0
    validations_passed: int = 0
    validations_failed: int = 0
    command_results: Dict[str, Any] = field(default_factory=dict)
    validation_results: List[ValidationResult] = field(default_factory=list)
    error: Optional[str] = None
    
    @property
    def duration_seconds(self) -> float:
        """Get execution duration in seconds"""
        return (self.end_time - self.start_time).total_seconds()


class PackRunner:
    """Execute automation packs against network devices"""
    
    def __init__(self, pack_loader: Optional[PackLoader] = None,
                 cmdb: Optional[CMDB] = None,
                 connection_manager: Optional[ConnectionManager] = None,
                 parser_engine: Optional[ParserEngine] = None,
                 validation_engine: Optional[ValidationEngine] = None,
                 reporter: Optional[Reporter] = None):
        """
        Initialize pack runner
        
        Args:
            pack_loader: Pack loader instance
            cmdb: CMDB instance
            connection_manager: Connection manager instance
            parser_engine: Parser engine instance
            validation_engine: Validation engine instance
            reporter: Reporter instance
        """
        self.pack_loader = pack_loader or PackLoader()
        self.cmdb = cmdb or CMDB()
        self.connection_manager = connection_manager or ConnectionManager()
        self.parser_engine = parser_engine or ParserEngine()
        self.validation_engine = validation_engine or ValidationEngine(self.parser_engine)
        self.reporter = reporter or Reporter()
        logger.info("pack_runner_initialized")
    
    def run_pack(self, pack_name: str, device_hostname: str,
                 dry_run: bool = False) -> ExecutionResult:
        """
        Run a pack against a device
        
        Args:
            pack_name: Name of the pack to run
            device_hostname: Target device hostname
            dry_run: If True, don't actually execute commands
            
        Returns:
            ExecutionResult
        """
        start_time = datetime.now()
        
        logger.info("pack_execution_started",
                   pack_name=pack_name,
                   device=device_hostname,
                   dry_run=dry_run)
        
        try:
            # Load pack
            pack = self.pack_loader.load_pack(pack_name)
            
            # Validate pack
            errors = self.pack_loader.validate_pack(pack)
            if errors:
                return self._create_error_result(
                    pack_name, device_hostname, start_time,
                    f"Pack validation failed: {', '.join(errors)}"
                )
            
            # Get device from CMDB
            device = self.cmdb.get_device(device_hostname)
            if not device:
                return self._create_error_result(
                    pack_name, device_hostname, start_time,
                    f"Device not found in CMDB: {device_hostname}"
                )
            
            # Check if device allows execution
            if pack.execution.mode == 'execute' and not device.allows_execution:
                return self._create_error_result(
                    pack_name, device_hostname, start_time,
                    f"Device {device_hostname} does not allow execution (missing 'allow_execute' tag)"
                )
            
            # Execute pack
            if dry_run:
                logger.info("dry_run_mode", message="Skipping actual execution")
                command_results = {}
            else:
                command_results = self._execute_commands(pack, device)
            
            # Run validations
            validation_results = []
            if pack.validations and command_results:
                validation_results = self.validation_engine.validate(
                    pack.validations,
                    command_results
                )
            
            # Calculate stats
            validations_passed = sum(1 for v in validation_results if v.passed)
            validations_failed = len(validation_results) - validations_passed
            
            end_time = datetime.now()
            
            result = ExecutionResult(
                pack_name=pack_name,
                device_hostname=device_hostname,
                success=True,
                start_time=start_time,
                end_time=end_time,
                commands_executed=len(command_results),
                validations_passed=validations_passed,
                validations_failed=validations_failed,
                command_results=command_results,
                validation_results=validation_results
            )
            
            logger.info("pack_execution_completed",
                       pack_name=pack_name,
                       device=device_hostname,
                       duration=result.duration_seconds,
                       commands=result.commands_executed,
                       validations_passed=validations_passed,
                       validations_failed=validations_failed)
            
            return result
            
        except Exception as e:
            logger.error("pack_execution_error",
                        pack_name=pack_name,
                        device=device_hostname,
                        error=str(e),
                        error_type=type(e).__name__)
            return self._create_error_result(
                pack_name, device_hostname, start_time,
                f"Execution error: {str(e)}"
            )

    def _execute_commands(self, pack: Pack, device: Device) -> Dict[str, Any]:
        """
        Execute all commands in a pack

        Args:
            pack: Pack to execute
            device: Target device

        Returns:
            Dictionary of command results (command_name -> parsed_output)
        """
        results = {}
        connection = None

        try:
            # Connect to device
            conn_result = self.connection_manager.connect(
                device,
                credential_ref=pack.authentication.credential_ref,
                port=pack.authentication.port,
                timeout=pack.execution.timeout_seconds
            )

            if not conn_result.success:
                logger.error("connection_failed",
                           device=device.hostname,
                           error=conn_result.message)
                raise RuntimeError(f"Connection failed: {conn_result.message}")

            connection = conn_result.connection

            # Execute each command
            for cmd in pack.commands:
                logger.info("executing_command",
                           device=device.hostname,
                           command_name=cmd.name,
                           command=cmd.command)

                # Execute command
                output = self.connection_manager.execute_command(
                    connection,
                    cmd.command,
                    timeout=cmd.timeout_seconds or pack.execution.timeout_seconds
                )

                # Parse output
                parsed = self.parser_engine.parse(
                    output,
                    cmd.parser,
                    template=cmd.parser_template,
                    pattern=cmd.parser_pattern
                )

                results[cmd.name] = parsed

                logger.info("command_executed",
                           device=device.hostname,
                           command_name=cmd.name,
                           output_length=len(output))

            return results

        finally:
            # Always disconnect
            if connection:
                self.connection_manager.disconnect(connection)

    def _create_error_result(self, pack_name: str, device_hostname: str,
                            start_time: datetime, error: str) -> ExecutionResult:
        """Create an error result"""
        return ExecutionResult(
            pack_name=pack_name,
            device_hostname=device_hostname,
            success=False,
            start_time=start_time,
            end_time=datetime.now(),
            error=error
        )

