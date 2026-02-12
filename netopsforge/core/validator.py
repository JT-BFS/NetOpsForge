"""
Validation Engine - Execute health checks and threshold validations
"""

import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from ..core.pack_loader import PackValidation
from ..core.parser import ParserEngine
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation check"""
    validation_name: str
    field: str
    expected: str
    actual: Any
    passed: bool
    severity: str
    message: str


class ValidationEngine:
    """Execute validation checks on parsed data"""
    
    def __init__(self, parser_engine: Optional[ParserEngine] = None):
        """
        Initialize validation engine
        
        Args:
            parser_engine: Parser engine instance
        """
        self.parser_engine = parser_engine or ParserEngine()
        logger.info("validation_engine_initialized")
    
    def validate(self, validations: List[PackValidation], 
                 parsed_data: Dict[str, Any]) -> List[ValidationResult]:
        """
        Execute all validations
        
        Args:
            validations: List of validation checks
            parsed_data: Parsed command output data (dict of command_name -> parsed_output)
            
        Returns:
            List of validation results
        """
        results = []
        
        for validation in validations:
            result = self._execute_validation(validation, parsed_data)
            results.append(result)
        
        # Log summary
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        logger.info("validations_executed", 
                   total=len(results), 
                   passed=passed, 
                   failed=failed)
        
        return results
    
    def _execute_validation(self, validation: PackValidation, 
                           parsed_data: Dict[str, Any]) -> ValidationResult:
        """
        Execute a single validation check
        
        Args:
            validation: Validation check definition
            parsed_data: Parsed command output data
            
        Returns:
            ValidationResult
        """
        # Extract the actual value from parsed data
        actual_value = self._extract_field_value(validation.field, parsed_data)
        
        # Evaluate the condition
        passed = self._evaluate_condition(actual_value, validation.condition)
        
        # Build message
        if validation.message:
            message = validation.message
        else:
            status = "PASS" if passed else "FAIL"
            message = f"{status}: {validation.field} {validation.condition} (actual: {actual_value})"
        
        result = ValidationResult(
            validation_name=validation.name,
            field=validation.field,
            expected=validation.condition,
            actual=actual_value,
            passed=passed,
            severity=validation.severity,
            message=message
        )
        
        log_level = "info" if passed else "warning"
        logger.log(log_level, "validation_result",
                  validation=validation.name,
                  field=validation.field,
                  passed=passed,
                  severity=validation.severity,
                  actual=actual_value)
        
        return result
    
    def _extract_field_value(self, field: str, parsed_data: Dict[str, Any]) -> Any:
        """
        Extract field value from parsed data
        
        Args:
            field: Field name (can be simple or dotted path)
            parsed_data: Parsed command output data
            
        Returns:
            Field value or None if not found
        """
        # Try to find the field in any of the parsed command outputs
        for cmd_name, cmd_data in parsed_data.items():
            value = self.parser_engine.extract_value(cmd_data, field)
            if value is not None:
                return value
        
        logger.warning("field_not_found", field=field)
        return None
    
    def _evaluate_condition(self, actual_value: Any, condition: str) -> bool:
        """
        Evaluate a condition against an actual value
        
        Args:
            actual_value: Actual value from parsed data
            condition: Condition string (e.g., "< 95", "== 'up'", "> 0")
            
        Returns:
            True if condition passes, False otherwise
        """
        if actual_value is None:
            return False
        
        try:
            # Parse condition
            condition = condition.strip()
            
            # Handle numeric comparisons
            if re.match(r'^[<>=!]+\s*-?\d+\.?\d*$', condition):
                # Extract operator and value
                match = re.match(r'^([<>=!]+)\s*(-?\d+\.?\d*)$', condition)
                if match:
                    operator = match.group(1)
                    expected_value = float(match.group(2))
                    actual_numeric = float(actual_value)
                    
                    if operator == '<':
                        return actual_numeric < expected_value
                    elif operator == '<=':
                        return actual_numeric <= expected_value
                    elif operator == '>':
                        return actual_numeric > expected_value
                    elif operator == '>=':
                        return actual_numeric >= expected_value
                    elif operator == '==' or operator == '=':
                        return actual_numeric == expected_value
                    elif operator == '!=':
                        return actual_numeric != expected_value
            
            # Handle string comparisons
            elif re.match(r'^[=!]+\s*["\'].*["\']$', condition):
                match = re.match(r'^([=!]+)\s*["\'](.*)["\']\s*$', condition)
                if match:
                    operator = match.group(1)
                    expected_value = match.group(2)
                    actual_str = str(actual_value)
                    
                    if operator == '==' or operator == '=':
                        return actual_str == expected_value
                    elif operator == '!=':
                        return actual_str != expected_value
            
            # Default: try direct evaluation (be careful with this)
            logger.warning("condition_evaluation_fallback", condition=condition)
            return False
            
        except Exception as e:
            logger.error("condition_evaluation_error", 
                        condition=condition, 
                        actual_value=actual_value,
                        error=str(e))
            return False

