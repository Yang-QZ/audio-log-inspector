#!/usr/bin/env python3
"""
Audio Log Inspector for MTK8676 Platform
This tool analyzes audio HAL logs from MediaTek MTK8676 chipset.
"""

import re
import sys
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple


class AudioLogInspector:
    """Main class for inspecting and analyzing audio HAL logs."""
    
    # Display constants
    MAX_ERRORS_DISPLAYED = 10
    MAX_WARNINGS_DISPLAYED = 10
    MAX_MESSAGE_LENGTH = 100
    MAX_DEVICE_CHANGES_DISPLAYED = 5
    
    def __init__(self):
        self.log_entries = []
        self.errors = []
        self.warnings = []
        self.audio_streams = defaultdict(list)
        self.device_changes = []
        
    def parse_log_line(self, line: str) -> Dict:
        """Parse a single log line and extract relevant information."""
        # Common MTK audio HAL log patterns
        patterns = {
            'timestamp': r'(\d{1,2}-\d{1,2}\s+\d{2}:\d{2}:\d{2}\.\d+)',
            'pid_tid': r'(\d+)\s+(\d+)',
            'level': r'[VDIWEF]',
            'tag': r'([A-Za-z0-9_]+)',
            'message': r':\s+(.*)',
        }
        
        entry = {
            'raw': line,
            'timestamp': None,
            'pid': None,
            'tid': None,
            'level': None,
            'tag': None,
            'message': None,
        }
        
        # Extract timestamp
        ts_match = re.search(patterns['timestamp'], line)
        if ts_match:
            entry['timestamp'] = ts_match.group(1)
        
        # Extract log level
        level_match = re.search(r'\s([VDIWEF])\s', line)
        if level_match:
            entry['level'] = level_match.group(1)
        
        # Extract tag (audio HAL related)
        tag_match = re.search(r'([A-Za-z0-9_]*[Aa]udio[A-Za-z0-9_]*)', line)
        if tag_match:
            entry['tag'] = tag_match.group(1)
        
        # Extract message
        msg_match = re.search(r':\s+(.+)$', line)
        if msg_match:
            entry['message'] = msg_match.group(1).strip()
        
        return entry
    
    def analyze_log_file(self, filepath: str) -> None:
        """Analyze audio log file."""
        print(f"[*] Analyzing log file: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Check if line contains audio-related keywords
                    if self._is_audio_related(line):
                        entry = self.parse_log_line(line)
                        self.log_entries.append(entry)
                        
                        # Categorize entries
                        if entry['level'] == 'E':
                            self.errors.append(entry)
                        elif entry['level'] == 'W':
                            self.warnings.append(entry)
                        
                        # Track audio stream operations
                        if 'stream' in line.lower():
                            self._track_stream(entry)
                        
                        # Track device changes
                        if 'device' in line.lower():
                            self._track_device_change(entry)
        
        except FileNotFoundError:
            print(f"[!] Error: File not found - {filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Error reading file: {e}")
            sys.exit(1)
    
    def _is_audio_related(self, line: str) -> bool:
        """Check if log line is audio related."""
        audio_keywords = [
            'audio', 'Audio', 'AUDIO',
            'AudioFlinger', 'AudioPolicyManager', 'AudioHAL',
            'playback', 'capture', 'record',
            'stream', 'device', 'volume',
            'MTK', 'mtk', 'alsa', 'ALSA',
            'pcm', 'PCM', 'codec', 'dsp', 'DSP'
        ]
        return any(keyword in line for keyword in audio_keywords)
    
    def _track_stream(self, entry: Dict) -> None:
        """Track audio stream operations."""
        message = entry.get('message', '').lower()
        if 'open' in message or 'start' in message:
            self.audio_streams['opened'].append(entry)
        elif 'close' in message or 'stop' in message:
            self.audio_streams['closed'].append(entry)
    
    def _track_device_change(self, entry: Dict) -> None:
        """Track audio device changes."""
        self.device_changes.append(entry)
    
    def generate_report(self) -> str:
        """Generate analysis report."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("Audio Log Inspector Report - MTK8676 Platform")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Summary statistics
        report_lines.append("## Summary Statistics")
        report_lines.append(f"Total audio-related log entries: {len(self.log_entries)}")
        report_lines.append(f"Errors (E): {len(self.errors)}")
        report_lines.append(f"Warnings (W): {len(self.warnings)}")
        report_lines.append(f"Audio stream operations: {len(self.audio_streams['opened']) + len(self.audio_streams['closed'])}")
        report_lines.append(f"Device changes: {len(self.device_changes)}")
        report_lines.append("")
        
        # Error details
        if self.errors:
            report_lines.append("## Errors Detected")
            report_lines.append("-" * 80)
            for i, error in enumerate(self.errors[:self.MAX_ERRORS_DISPLAYED], 1):
                report_lines.append(f"{i}. [{error.get('timestamp', 'N/A')}] {error.get('tag', 'Unknown')}")
                report_lines.append(f"   {error.get('message', 'No message')[:self.MAX_MESSAGE_LENGTH]}")
            if len(self.errors) > self.MAX_ERRORS_DISPLAYED:
                report_lines.append(f"   ... and {len(self.errors) - self.MAX_ERRORS_DISPLAYED} more errors")
            report_lines.append("")
        
        # Warning details
        if self.warnings:
            report_lines.append("## Warnings Detected")
            report_lines.append("-" * 80)
            for i, warning in enumerate(self.warnings[:self.MAX_WARNINGS_DISPLAYED], 1):
                report_lines.append(f"{i}. [{warning.get('timestamp', 'N/A')}] {warning.get('tag', 'Unknown')}")
                report_lines.append(f"   {warning.get('message', 'No message')[:self.MAX_MESSAGE_LENGTH]}")
            if len(self.warnings) > self.MAX_WARNINGS_DISPLAYED:
                report_lines.append(f"   ... and {len(self.warnings) - self.MAX_WARNINGS_DISPLAYED} more warnings")
            report_lines.append("")
        
        # Stream operations
        report_lines.append("## Audio Stream Operations")
        report_lines.append("-" * 80)
        report_lines.append(f"Streams opened: {len(self.audio_streams['opened'])}")
        report_lines.append(f"Streams closed: {len(self.audio_streams['closed'])}")
        report_lines.append("")
        
        # Device changes
        if self.device_changes:
            report_lines.append("## Audio Device Changes")
            report_lines.append("-" * 80)
            for i, change in enumerate(self.device_changes[:self.MAX_DEVICE_CHANGES_DISPLAYED], 1):
                report_lines.append(f"{i}. [{change.get('timestamp', 'N/A')}] {change.get('message', 'No message')[:80]}")
            if len(self.device_changes) > self.MAX_DEVICE_CHANGES_DISPLAYED:
                report_lines.append(f"   ... and {len(self.device_changes) - self.MAX_DEVICE_CHANGES_DISPLAYED} more changes")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        report_lines.append("End of Report")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def save_report(self, output_file: str) -> None:
        """Save analysis report to file."""
        report = self.generate_report()
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"[+] Report saved to: {output_file}")
        except Exception as e:
            print(f"[!] Error saving report: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 audio_log_inspector.py <log_file> [output_report]")
        print("\nExample:")
        print("  python3 audio_log_inspector.py logcat.txt")
        print("  python3 audio_log_inspector.py logcat.txt report.txt")
        sys.exit(1)
    
    log_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create inspector instance
    inspector = AudioLogInspector()
    
    # Analyze log file
    inspector.analyze_log_file(log_file)
    
    # Generate and display report
    report = inspector.generate_report()
    print(report)
    
    # Save report if output file specified
    if output_file:
        inspector.save_report(output_file)


if __name__ == "__main__":
    main()
