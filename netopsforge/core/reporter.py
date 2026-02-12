"""
Output Handler - Generate reports in various formats
"""

import json
import yaml
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path
from tabulate import tabulate
from ..utils.logging import get_logger

logger = get_logger(__name__)


class Reporter:
    """Generate output reports in various formats"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize reporter
        
        Args:
            output_dir: Directory for output files
        """
        self.output_dir = output_dir or Path("output")
        self.output_dir.mkdir(exist_ok=True)
        logger.info("reporter_initialized", output_dir=str(self.output_dir))
    
    def generate_report(self, data: Dict[str, Any], format: str = 'json',
                       output_file: Optional[Path] = None) -> str:
        """
        Generate report in specified format
        
        Args:
            data: Report data
            format: Output format (json, yaml, csv, markdown)
            output_file: Optional output file path
            
        Returns:
            Report content as string
        """
        if format == 'json':
            content = self.to_json(data)
        elif format == 'yaml':
            content = self.to_yaml(data)
        elif format == 'markdown':
            content = self.to_markdown(data)
        elif format == 'csv':
            content = self.to_csv(data)
        else:
            logger.error("unknown_format", format=format)
            raise ValueError(f"Unknown format: {format}")
        
        # Save to file if specified
        if output_file:
            output_path = self.output_dir / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(content)
            logger.info("report_saved", format=format, path=str(output_path))
        
        return content
    
    def to_json(self, data: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert data to JSON
        
        Args:
            data: Data to convert
            pretty: Pretty print with indentation
            
        Returns:
            JSON string
        """
        if pretty:
            return json.dumps(data, indent=2, default=str)
        else:
            return json.dumps(data, default=str)
    
    def to_yaml(self, data: Dict[str, Any]) -> str:
        """
        Convert data to YAML
        
        Args:
            data: Data to convert
            
        Returns:
            YAML string
        """
        return yaml.dump(data, default_flow_style=False, sort_keys=False)
    
    def to_markdown(self, data: Dict[str, Any]) -> str:
        """
        Convert data to Markdown report
        
        Args:
            data: Data to convert
            
        Returns:
            Markdown string
        """
        lines = []
        
        # Header
        lines.append(f"# NetOpsForge Report")
        lines.append(f"")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"")
        
        # Pack info
        if 'pack' in data:
            lines.append(f"## Pack: {data['pack'].get('name', 'Unknown')}")
            lines.append(f"")
        
        # Device info
        if 'device' in data:
            device = data['device']
            lines.append(f"## Device: {device.get('hostname', 'Unknown')}")
            lines.append(f"")
            lines.append(f"- **IP:** {device.get('management_ip', 'N/A')}")
            lines.append(f"- **Platform:** {device.get('platform', 'N/A')}")
            lines.append(f"- **Vendor:** {device.get('vendor', 'N/A')}")
            lines.append(f"")
        
        # Execution results
        if 'results' in data:
            lines.append(f"## Execution Results")
            lines.append(f"")
            
            for cmd_name, cmd_result in data['results'].items():
                lines.append(f"### {cmd_name}")
                lines.append(f"")
                
                if isinstance(cmd_result, list) and len(cmd_result) > 0:
                    # Table format for list of dicts
                    if isinstance(cmd_result[0], dict):
                        table_data = [[k for k in cmd_result[0].keys()]]
                        for row in cmd_result:
                            table_data.append([str(v) for v in row.values()])
                        lines.append(tabulate(table_data[1:], headers=table_data[0], tablefmt='github'))
                    else:
                        lines.append(str(cmd_result))
                elif isinstance(cmd_result, dict):
                    for key, value in cmd_result.items():
                        lines.append(f"- **{key}:** {value}")
                else:
                    lines.append(f"```")
                    lines.append(str(cmd_result))
                    lines.append(f"```")
                
                lines.append(f"")
        
        # Validation results
        if 'validations' in data:
            lines.append(f"## Validation Results")
            lines.append(f"")
            
            validations = data['validations']
            passed = sum(1 for v in validations if v.get('passed', False))
            failed = len(validations) - passed
            
            lines.append(f"**Summary:** {passed} passed, {failed} failed")
            lines.append(f"")
            
            # Table of validations
            table_data = []
            for val in validations:
                status = "✅ PASS" if val.get('passed') else "❌ FAIL"
                table_data.append([
                    val.get('validation_name', 'N/A'),
                    val.get('field', 'N/A'),
                    val.get('expected', 'N/A'),
                    str(val.get('actual', 'N/A')),
                    status,
                    val.get('severity', 'N/A')
                ])
            
            lines.append(tabulate(table_data, 
                                headers=['Validation', 'Field', 'Expected', 'Actual', 'Status', 'Severity'],
                                tablefmt='github'))
            lines.append(f"")
        
        return '\n'.join(lines)
    
    def to_csv(self, data: Dict[str, Any]) -> str:
        """
        Convert data to CSV (simplified)
        
        Args:
            data: Data to convert
            
        Returns:
            CSV string
        """
        # This is a simplified CSV export
        # For full CSV support, use pandas
        lines = []
        
        if 'validations' in data:
            # Export validations as CSV
            lines.append("Validation,Field,Expected,Actual,Passed,Severity")
            for val in data['validations']:
                lines.append(f"{val.get('validation_name', '')},{val.get('field', '')},"
                           f"{val.get('expected', '')},{val.get('actual', '')},"
                           f"{val.get('passed', False)},{val.get('severity', '')}")
        
        return '\n'.join(lines)

