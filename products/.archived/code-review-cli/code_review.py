#!/usr/bin/env python3
"""
Code Review CLI - Automated Code Quality Analysis
A tool for developers to self-review code before submitting PRs.
Author: UniverseCreator
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

__version__ = "1.0.0"


@dataclass
class ReviewIssue:
    """Represents a code review issue."""
    severity: str  # critical, warning, suggestion
    category: str  # security, style, performance, maintainability
    line: int
    message: str
    suggestion: str
    rule: str


class CodeReviewer:
    """Automated code reviewer for multiple languages."""
    
    SEVERITY_WEIGHTS = {
        'critical': 10,
        'warning': 5,
        'suggestion': 1
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.issues: List[ReviewIssue] = []
        self.files_reviewed = 0
        self.lines_reviewed = 0
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration file."""
        default_config = {
            'severity_threshold': 'warning',
            'max_line_length': 100,
            'check_security': True,
            'check_performance': True,
            'check_style': True,
            'ignore_patterns': ['*.min.js', '*.min.css', 'node_modules/', 'venv/', '.git/', '__pycache__/'],
            'custom_rules': []
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                custom = json.load(f)
                default_config.update(custom)
        
        return default_config
    
    def _should_ignore(self, file_path: str) -> bool:
        """Check if file should be ignored."""
        for pattern in self.config['ignore_patterns']:
            if pattern in file_path or file_path.endswith(pattern.replace('*', '')):
                return True
        return False
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        ext = Path(file_path).suffix.lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.sh': 'bash',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.less': 'less',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.dockerfile': 'dockerfile',
        }
        return lang_map.get(ext, 'unknown')
    
    def review_file(self, file_path: str) -> List[ReviewIssue]:
        """Review a single file."""
        if self._should_ignore(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return []
        
        language = self._detect_language(file_path)
        file_issues = []
        
        self.files_reviewed += 1
        self.lines_reviewed += len(lines)
        
        # Security checks
        if self.config['check_security']:
            file_issues.extend(self._check_security(content, lines, language))
        
        # Performance checks
        if self.config['check_performance']:
            file_issues.extend(self._check_performance(content, lines, language))
        
        # Style checks
        if self.config['check_style']:
            file_issues.extend(self._check_style(content, lines, language))
        
        # Language-specific checks
        file_issues.extend(self._language_specific_checks(content, lines, language))
        
        self.issues.extend(file_issues)
        return file_issues
    
    def _check_security(self, content: str, lines: List[str], language: str) -> List[ReviewIssue]:
        """Check for security issues."""
        issues = []
        
        # Hardcoded secrets
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password detected'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret detected'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key detected'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'Hardcoded token detected'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID detected'),
            (r'sk_live_[0-9a-zA-Z]{24,}', 'Stripe live key detected'),
            (r'ghp_[0-9a-zA-Z]{36}', 'GitHub personal access token detected'),
        ]
        
        for pattern, message in secret_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(ReviewIssue(
                        severity='critical',
                        category='security',
                        line=i,
                        message=message,
                        suggestion='Move secrets to environment variables or a secrets manager',
                        rule='no-hardcoded-secrets'
                    ))
        
        # SQL Injection patterns
        sql_patterns = [
            (r'execute\s*\(.*\+', 'Potential SQL injection'),
            (r'query\s*\(.*\+', 'Potential SQL injection'),
            (r'\.format\s*\(.*\)', 'Potential string formatting injection'),
            (r'%s.*%', 'Potential format string vulnerability'),
        ]
        
        for pattern, message in sql_patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(ReviewIssue(
                        severity='critical',
                        category='security',
                        line=i,
                        message=message,
                        suggestion='Use parameterized queries or prepared statements',
                        rule='sql-injection-risk'
                    ))
        
        return issues
    
    def _check_performance(self, content: str, lines: List[str], language: str) -> List[ReviewIssue]:
        """Check for performance issues."""
        issues = []
        
        # Inefficient patterns
        perf_patterns = {
            'python': [
                (r'for\s+.+\s+in\s+range\s*\(\s*len\s*\(', 'Using range(len()) instead of enumerate()'),
                (r'\+\s*["\']', 'String concatenation in loop - use join()'),
                (r'\.append\s*\(', 'List append in loop - consider list comprehension'),
            ],
            'javascript': [
                (r'for\s*\(\s*var\s+i\s*=\s*0', 'Using var in loop - use let or const'),
                (r'\.innerHTML\s*=', 'Using innerHTML - consider textContent for plain text'),
                (r'new\s+Array\s*\(\s*\d+\s*\)', 'Using new Array() - use [] literal'),
            ],
        }
        
        patterns = perf_patterns.get(language, [])
        for pattern, message in patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    issues.append(ReviewIssue(
                        severity='warning',
                        category='performance',
                        line=i,
                        message=message,
                        suggestion='Consider the suggested alternative for better performance',
                        rule='performance-optimization'
                    ))
        
        return issues
    
    def _check_style(self, content: str, lines: List[str], language: str) -> List[ReviewIssue]:
        """Check code style issues."""
        issues = []
        max_length = self.config.get('max_line_length', 100)
        
        for i, line in enumerate(lines, 1):
            # Line length
            if len(line) > max_length:
                issues.append(ReviewIssue(
                    severity='suggestion',
                    category='style',
                    line=i,
                    message=f'Line exceeds {max_length} characters ({len(line)} chars)',
                    suggestion='Break long lines into multiple lines',
                    rule='max-line-length'
                ))
            
            # Trailing whitespace
            if line.rstrip() != line:
                issues.append(ReviewIssue(
                    severity='suggestion',
                    category='style',
                    line=i,
                    message='Trailing whitespace detected',
                    suggestion='Remove trailing whitespace',
                    rule='no-trailing-whitespace'
                ))
            
            # TODO/FIXME comments
            if re.search(r'#\s*(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE):
                match = re.search(r'#\s*(TODO|FIXME|XXX|HACK)', line, re.IGNORECASE)
                issues.append(ReviewIssue(
                    severity='suggestion',
                    category='maintainability',
                    line=i,
                    message=f'{match.group(1).upper()} comment found',
                    suggestion='Address or remove this comment before merging',
                    rule='todo-comment'
                ))
        
        return issues
    
    def _language_specific_checks(self, content: str, lines: List[str], language: str) -> List[ReviewIssue]:
        """Language-specific code quality checks."""
        issues = []
        
        if language == 'python':
            # Bare except clauses
            for i, line in enumerate(lines, 1):
                if re.search(r'except\s*:', line):
                    issues.append(ReviewIssue(
                        severity='warning',
                        category='maintainability',
                        line=i,
                        message='Bare except clause catches all exceptions including KeyboardInterrupt',
                        suggestion='Use "except Exception:" to catch only standard exceptions',
                        rule='no-bare-except'
                    ))
                
                # Mutable default arguments
                if re.search(r'def\s+\w+\s*\([^)]*=\s*(\[|\{)', line):
                    issues.append(ReviewIssue(
                        severity='critical',
                        category='maintainability',
                        line=i,
                        message='Mutable default argument detected',
                        suggestion='Use None as default and initialize mutable object inside function',
                        rule='no-mutable-default'
                    ))
        
        elif language in ['javascript', 'typescript']:
            for i, line in enumerate(lines, 1):
                # == instead of ===
                if re.search(r'[^=!]==[^=]', line):
                    issues.append(ReviewIssue(
                        severity='suggestion',
                        category='maintainability',
                        line=i,
                        message='Using == instead of ===',
                        suggestion='Use === for strict equality comparison',
                        rule='use-strict-equality'
                    ))
        
        elif language == 'go':
            for i, line in enumerate(lines, 1):
                # Error not checked
                if re.search(r'\)\s*$', line) and i < len(lines):
                    next_line = lines[i] if i < len(lines) else ''
                    if 'error' in line and 'if' not in next_line and 'err' not in next_line:
                        issues.append(ReviewIssue(
                            severity='warning',
                            category='maintainability',
                            line=i,
                            message='Error return value may not be checked',
                            suggestion='Always check error return values',
                            rule='check-error-return'
                        ))
        
        return issues
    
    def review_directory(self, directory: str) -> Dict:
        """Review all files in a directory."""
        path = Path(directory)
        
        for file_path in path.rglob('*'):
            if file_path.is_file():
                self.review_file(str(file_path))
        
        return self._generate_summary()
    
    def _generate_summary(self) -> Dict:
        """Generate review summary."""
        critical = len([i for i in self.issues if i.severity == 'critical'])
        warning = len([i for i in self.issues if i.severity == 'warning'])
        suggestion = len([i for i in self.issues if i.severity == 'suggestion'])
        
        # Calculate score (100 - weighted deductions)
        total_weight = sum(self.SEVERITY_WEIGHTS[i.severity] for i in self.issues)
        score = max(0, 100 - total_weight)
        
        # Determine grade
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 70:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'
        
        return {
            'score': score,
            'grade': grade,
            'files_reviewed': self.files_reviewed,
            'lines_reviewed': self.lines_reviewed,
            'issues': {
                'total': len(self.issues),
                'critical': critical,
                'warning': warning,
                'suggestion': suggestion
            },
            'details': [asdict(i) for i in self.issues]
        }
    
    def print_report(self, summary: Dict):
        """Print review report to console."""
        print("=" * 60)
        print("🔍 CODE REVIEW REPORT")
        print("=" * 60)
        print()
        
        score = summary['score']
        grade = summary['grade']
        
        # Color code the grade
        grade_colors = {
            'A': '\033[92m',  # Green
            'B': '\033[94m',  # Blue
            'C': '\033[93m',  # Yellow
            'D': '\033[91m',  # Red
            'F': '\033[91m'   # Red
        }
        color = grade_colors.get(grade, '')
        reset = '\033[0m'
        
        print(f"Score: {score}/100 (Grade: {color}{grade}{reset})")
        print(f"Files: {summary['files_reviewed']} | Lines: {summary['lines_reviewed']}")
        print()
        
        issues = summary['issues']
        print(f"Issues Found: {issues['total']}")
        print(f"  🔴 Critical: {issues['critical']}")
        print(f"  🟡 Warning: {issues['warning']}")
        print(f"  🔵 Suggestion: {issues['suggestion']}")
        print()
        
        if summary['details']:
            print("-" * 60)
            print("DETAILED FINDINGS:")
            print("-" * 60)
            
            for issue in summary['details']:
                severity_emoji = {
                    'critical': '🔴',
                    'warning': '🟡',
                    'suggestion': '🔵'
                }.get(issue['severity'], '⚪')
                
                print(f"\n{severity_emoji} [{issue['severity'].upper()}] Line {issue['line']}")
                print(f"   Rule: {issue['rule']}")
                print(f"   Issue: {issue['message']}")
                print(f"   Suggestion: {issue['suggestion']}")
    
    def export_markdown(self, summary: Dict, output_path: str):
        """Export report as markdown."""
        with open(output_path, 'w') as f:
            f.write("# 🔍 Code Review Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Score | {summary['score']}/100 |\n")
            f.write(f"| Grade | {summary['grade']} |\n")
            f.write(f"| Files Reviewed | {summary['files_reviewed']} |\n")
            f.write(f"| Lines Reviewed | {summary['lines_reviewed']} |\n")
            f.write(f"| Total Issues | {summary['issues']['total']} |\n")
            f.write(f"| Critical | {summary['issues']['critical']} |\n")
            f.write(f"| Warning | {summary['issues']['warning']} |\n")
            f.write(f"| Suggestion | {summary['issues']['suggestion']} |\n\n")
            
            if summary['details']:
                f.write("## Detailed Findings\n\n")
                
                for issue in summary['details']:
                    f.write(f"### {issue['rule']}\n\n")
                    f.write(f"- **Severity**: {issue['severity']}\n")
                    f.write(f"- **Category**: {issue['category']}\n")
                    f.write(f"- **Line**: {issue['line']}\n")
                    f.write(f"- **Message**: {issue['message']}\n")
                    f.write(f"- **Suggestion**: {issue['suggestion']}\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="🔍 Code Review CLI - Automated code quality analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  code-review app.py                    # Review single file
  code-review .                         # Review entire project
  code-review . --export report.md      # Export markdown report
  code-review . --severity warning      # Show only warnings and above
        """
    )
    
    parser.add_argument('path', help='File or directory to review')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--export', '-e', help='Export report to file (markdown)')
    parser.add_argument('--severity', '-s', 
                       choices=['critical', 'warning', 'suggestion'],
                       help='Minimum severity to report')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path not found: {args.path}")
        sys.exit(1)
    
    reviewer = CodeReviewer(config_path=args.config)
    
    if os.path.isfile(args.path):
        reviewer.review_file(args.path)
        summary = reviewer._generate_summary()
    else:
        summary = reviewer.review_directory(args.path)
    
    # Filter by severity if specified
    if args.severity:
        severity_order = ['critical', 'warning', 'suggestion']
        min_index = severity_order.index(args.severity)
        summary['details'] = [
            d for d in summary['details'] 
            if severity_order.index(d['severity']) <= min_index
        ]
        summary['issues']['total'] = len(summary['details'])
        summary['issues']['critical'] = len([d for d in summary['details'] if d['severity'] == 'critical'])
        summary['issues']['warning'] = len([d for d in summary['details'] if d['severity'] == 'warning'])
        summary['issues']['suggestion'] = len([d for d in summary['details'] if d['severity'] == 'suggestion'])
    
    reviewer.print_report(summary)
    
    if args.export:
        reviewer.export_markdown(summary, args.export)
        print(f"\n✅ Report exported to: {args.export}")


if __name__ == '__main__':
    main()