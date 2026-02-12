"""
Parser Engine - Parse command output using TextFSM, regex, or raw
"""

import re
from typing import Any, Dict, List, Optional
from pathlib import Path
from ..utils.config import Config
from ..utils.logging import get_logger

logger = get_logger(__name__)

# TextFSM will be imported when needed
try:
    import textfsm
    TEXTFSM_AVAILABLE = True
except ImportError:
    TEXTFSM_AVAILABLE = False
    logger.warning("textfsm_not_available", message="TextFSM parsing unavailable")


class ParserEngine:
    """Parse network device command output"""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize parser engine
        
        Args:
            templates_dir: Directory containing TextFSM templates
        """
        self.templates_dir = templates_dir or (Config.BASE_DIR / "templates")
        logger.info("parser_engine_initialized", templates_dir=str(self.templates_dir))
    
    def parse(self, output: str, parser_type: str, 
              template: Optional[str] = None,
              pattern: Optional[str] = None) -> Any:
        """
        Parse command output
        
        Args:
            output: Raw command output
            parser_type: Parser type (textfsm, regex, raw)
            template: TextFSM template name (for textfsm parser)
            pattern: Regex pattern (for regex parser)
            
        Returns:
            Parsed data (format depends on parser type)
        """
        if parser_type == 'textfsm':
            return self.parse_textfsm(output, template)
        elif parser_type == 'regex':
            return self.parse_regex(output, pattern)
        elif parser_type == 'raw':
            return self.parse_raw(output)
        else:
            logger.error("unknown_parser_type", parser_type=parser_type)
            raise ValueError(f"Unknown parser type: {parser_type}")
    
    def parse_textfsm(self, output: str, template_name: str) -> List[Dict[str, Any]]:
        """
        Parse output using TextFSM template
        
        Args:
            output: Raw command output
            template_name: TextFSM template filename
            
        Returns:
            List of dictionaries with parsed data
        """
        if not TEXTFSM_AVAILABLE:
            logger.error("textfsm_unavailable")
            raise RuntimeError("TextFSM is not available")
        
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            logger.error("template_not_found", template=template_name, path=str(template_path))
            raise FileNotFoundError(f"TextFSM template not found: {template_path}")
        
        try:
            with open(template_path, 'r') as f:
                fsm = textfsm.TextFSM(f)
            
            parsed = fsm.ParseText(output)
            
            # Convert to list of dictionaries
            results = []
            for row in parsed:
                result = {}
                for i, value in enumerate(row):
                    result[fsm.header[i].lower()] = value
                results.append(result)
            
            logger.info("textfsm_parse_success", template=template_name, results_count=len(results))
            return results
            
        except Exception as e:
            logger.error("textfsm_parse_error", template=template_name, error=str(e))
            raise
    
    def parse_regex(self, output: str, pattern: str) -> Dict[str, Any]:
        """
        Parse output using regex pattern
        
        Args:
            output: Raw command output
            pattern: Regex pattern with named groups
            
        Returns:
            Dictionary with matched groups
        """
        try:
            match = re.search(pattern, output, re.MULTILINE | re.DOTALL)
            
            if match:
                result = match.groupdict()
                logger.info("regex_parse_success", groups_count=len(result))
                return result
            else:
                logger.warning("regex_no_match", pattern=pattern)
                return {}
                
        except Exception as e:
            logger.error("regex_parse_error", pattern=pattern, error=str(e))
            raise
    
    def parse_raw(self, output: str) -> str:
        """
        Return raw output (no parsing)
        
        Args:
            output: Raw command output
            
        Returns:
            Raw output string
        """
        logger.debug("raw_parse", output_length=len(output))
        return output
    
    def extract_value(self, parsed_data: Any, field_path: str) -> Any:
        """
        Extract a value from parsed data using dot notation
        
        Args:
            parsed_data: Parsed data (dict, list, or string)
            field_path: Field path (e.g., "cpu_5min" or "interfaces[0].status")
            
        Returns:
            Extracted value or None if not found
        """
        try:
            # Handle simple field names
            if '.' not in field_path and '[' not in field_path:
                if isinstance(parsed_data, dict):
                    return parsed_data.get(field_path)
                elif isinstance(parsed_data, list) and len(parsed_data) > 0:
                    return parsed_data[0].get(field_path)
                else:
                    return None
            
            # Handle complex paths (future enhancement)
            # For now, just try simple dict access
            if isinstance(parsed_data, dict):
                return parsed_data.get(field_path)
            elif isinstance(parsed_data, list) and len(parsed_data) > 0:
                return parsed_data[0].get(field_path)
            
            return None
            
        except Exception as e:
            logger.warning("value_extraction_error", field_path=field_path, error=str(e))
            return None

