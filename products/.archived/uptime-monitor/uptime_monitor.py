#!/usr/bin/env python3
"""
Website Uptime Monitor with Multi-Channel Alerts
Production-ready script for monitoring website availability

Author: UniverseCreator
License: See README.md for licensing options
"""

import json
import time
import logging
import smtplib
import requests
from datetime import datetime
from urllib.parse import urlparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('uptime_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class UptimeMonitor:
    """Monitor websites and send alerts when they're down."""
    
    def __init__(self, config_path='config.json'):
        self.config = self._load_config(config_path)
        self.status_history = {}
        self.load_history()
        
    def _load_config(self, path):
        """Load configuration from JSON file."""
        with open(path, 'r') as f:
            return json.load(f)
    
    def load_history(self):
        """Load status history from file."""
        history_path = Path('status_history.json')
        if history_path.exists():
            with open(history_path, 'r') as f:
                self.status_history = json.load(f)
    
    def save_history(self):
        """Save status history to file."""
        with open('status_history.json', 'w') as f:
            json.dump(self.status_history, f, indent=2)
    
    def check_website(self, url, timeout=30):
        """Check if a website is up."""
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout, headers={
                'User-Agent': 'UptimeMonitor/1.0'
            })
            response_time = (time.time() - start_time) * 1000  # ms
            
            is_up = response.status_code < 400
            status = {
                'url': url,
                'status_code': response.status_code,
                'response_time_ms': round(response_time, 2),
                'is_up': is_up,
                'checked_at': datetime.now().isoformat(),
                'error': None
            }
            
            if not is_up:
                status['error'] = f'HTTP {response.status_code}'
            
            return status
            
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'status_code': None,
                'response_time_ms': None,
                'is_up': False,
                'checked_at': datetime.now().isoformat(),
                'error': 'Timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'status_code': None,
                'response_time_ms': None,
                'is_up': False,
                'checked_at': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def send_discord_alert(self, webhook_url, site, status):
        """Send alert to Discord webhook."""
        emoji = "🟢" if status['is_up'] else "🔴"
        color = 0x00ff00 if status['is_up'] else 0xff0000
        
        embed = {
            "title": f"{emoji} {site['name']} - {'UP' if status['is_up'] else 'DOWN'}",
            "description": f"**URL:** {status['url']}\n**Time:** {status['checked_at']}",
            "color": color,
            "fields": []
        }
        
        if status['is_up']:
            embed['fields'].append({
                "name": "Response Time",
                "value": f"{status['response_time_ms']}ms",
                "inline": True
            })
        else:
            embed['fields'].append({
                "name": "Error",
                "value": status['error'],
                "inline": True
            })
        
        payload = {"embeds": [embed]}
        
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Discord alert sent for {site['name']}")
        except Exception as e:
            logger.error(f"Failed to send Discord alert: {e}")
    
    def send_slack_alert(self, webhook_url, site, status):
        """Send alert to Slack webhook."""
        emoji = ":white_check_mark:" if status['is_up'] else ":x:"
        color = "#00ff00" if status['is_up'] else "#ff0000"
        
        text = f"{emoji} *{site['name']}* is {'UP' if status['is_up'] else 'DOWN'}\n"
        text += f"URL: {status['url']}\n"
        text += f"Time: {status['checked_at']}\n"
        
        if status['is_up']:
            text += f"Response Time: {status['response_time_ms']}ms"
        else:
            text += f"Error: {status['error']}"
        
        payload = {
            "text": text,
            "attachments": [{"color": color, "text": text}]
        }
        
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Slack alert sent for {site['name']}")
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
    
    def send_telegram_alert(self, bot_token, chat_id, site, status):
        """Send alert to Telegram."""
        emoji = "✅" if status['is_up'] else "❌"
        
        message = f"{emoji} *{site['name']}* is {'UP' if status['is_up'] else 'DOWN'}\n\n"
        message += f"🔗 URL: {status['url']}\n"
        message += f"🕐 Time: {status['checked_at']}\n"
        
        if status['is_up']:
            message += f"⚡ Response: {status['response_time_ms']}ms"
        else:
            message += f"❗ Error: {status['error']}"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Telegram alert sent for {site['name']}")
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
    
    def send_email_alert(self, email_config, site, status):
        """Send alert via email."""
        emoji = "✅" if status['is_up'] else "❌"
        subject = f"{emoji} {site['name']} - {'UP' if status['is_up'] else 'DOWN'}"
        
        body = f"""
Website Status Alert

Site: {site['name']}
URL: {status['url']}
Status: {'UP' if status['is_up'] else 'DOWN'}
Time: {status['checked_at']}
"""
        
        if status['is_up']:
            body += f"Response Time: {status['response_time_ms']}ms\n"
        else:
            body += f"Error: {status['error']}\n"
        
        msg = MIMEMultipart()
        msg['From'] = email_config['from_email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(email_config['server'], email_config['port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            
            for to_email in email_config['to_emails']:
                msg['To'] = to_email
                server.send_message(msg)
            
            server.quit()
            logger.info(f"Email alert sent for {site['name']}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    def send_alerts(self, site, status):
        """Send alerts to all configured channels."""
        alerts = self.config.get('alerts', {})
        
        if 'discord' in alerts and alerts['discord'] and 'YOUR_' not in alerts['discord']:
            self.send_discord_alert(alerts['discord'], site, status)
        
        if 'slack' in alerts and alerts['slack'] and 'YOUR_' not in alerts['slack']:
            self.send_slack_alert(alerts['slack'], site, status)
        
        if 'telegram' in alerts:
            tg = alerts['telegram']
            if tg.get('bot_token') and 'YOUR_' not in tg['bot_token']:
                self.send_telegram_alert(tg['bot_token'], tg['chat_id'], site, status)
        
        if 'email' in alerts:
            email = alerts['email']
            if email.get('username') and 'YOUR_' not in email['username']:
                self.send_email_alert(email, site, status)
    
    def run_check(self):
        """Run a single check cycle for all sites."""
        for site in self.config['sites']:
            logger.info(f"Checking {site['name']} ({site['url']})...")
            
            # Check with retry logic
            status = None
            for attempt in range(self.config.get('retry_count', 2) + 1):
                status = self.check_website(site['url'])
                if status['is_up']:
                    break
                if attempt < self.config.get('retry_count', 2):
                    logger.warning(f"Retry {attempt + 1} for {site['name']}...")
                    time.sleep(5)
            
            # Update history
            url = site['url']
            if url not in self.status_history:
                self.status_history[url] = []
            self.status_history[url].append(status)
            
            # Keep only last 1000 checks per site
            self.status_history[url] = self.status_history[url][-1000:]
            
            # Send alerts if status changed
            previous_checks = self.status_history[url][-2:]
            if len(previous_checks) >= 2:
                prev_status = previous_checks[0]['is_up']
                curr_status = previous_checks[1]['is_up']
                
                if prev_status != curr_status:
                    logger.info(f"Status changed for {site['name']}: {prev_status} -> {curr_status}")
                    self.send_alerts(site, status)
            elif not status['is_up']:
                # First check and site is down
                self.send_alerts(site, status)
            
            if status['is_up']:
                logger.info(f"{site['name']} is UP ({status['response_time_ms']}ms)")
            else:
                logger.warning(f"{site['name']} is DOWN: {status['error']}")
        
        self.save_history()
    
    def generate_report(self, days=7):
        """Generate uptime report for the last N days."""
        report = []
        
        for url, checks in self.status_history.items():
            # Filter to last N days
            cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
            recent_checks = [c for c in checks if 
                           datetime.fromisoformat(c['checked_at']).timestamp() > cutoff]
            
            if not recent_checks:
                continue
            
            total = len(recent_checks)
            up = sum(1 for c in recent_checks if c['is_up'])
            uptime_pct = (up / total * 100) if total > 0 else 0
            
            response_times = [c['response_time_ms'] for c in recent_checks if c['is_up']]
            avg_response = sum(response_times) / len(response_times) if response_times else 0
            
            report.append({
                'url': url,
                'total_checks': total,
                'up_count': up,
                'down_count': total - up,
                'uptime_percentage': round(uptime_pct, 2),
                'avg_response_ms': round(avg_response, 2)
            })
        
        return report
    
    def export_report(self, format='json', days=7):
        """Export report to file."""
        report = self.generate_report(days)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f'uptime_report_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
        elif format == 'csv':
            import csv
            filename = f'uptime_report_{timestamp}.csv'
            with open(filename, 'w', newline='') as f:
                if report:
                    writer = csv.DictWriter(f, fieldnames=report[0].keys())
                    writer.writeheader()
                    writer.writerows(report)
        
        logger.info(f"Report exported to {filename}")
        return filename
    
    def run(self):
        """Run the monitor continuously."""
        logger.info("Starting Uptime Monitor...")
        logger.info(f"Monitoring {len(self.config['sites'])} sites")
        logger.info(f"Check interval: {self.config['check_interval']} seconds")
        
        try:
            while True:
                self.run_check()
                logger.info(f"Sleeping for {self.config['check_interval']} seconds...")
                time.sleep(self.config['check_interval'])
        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
            self.save_history()


def main():
    """Main entry point."""
    import sys
    
    monitor = UptimeMonitor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'report':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            format = sys.argv[3] if len(sys.argv) > 3 else 'json'
            monitor.export_report(format, days)
        elif sys.argv[1] == 'check':
            monitor.run_check()
            print(json.dumps(monitor.generate_report(), indent=2))
    else:
        monitor.run()


if __name__ == '__main__':
    main()