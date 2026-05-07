import datetime

class AlertManager():
    def __init__(self, log_path=None):
        self.log_path = log_path

    def send_alert(self, change_type, filepath):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[{timestamp}] ALERT - {change_type.upper()}: {filepath}"
        print(message)
        if self.log_path:
            with open(self.log_path, 'a') as f:
                f.write(message + '\n')

    def process_changes(self, changes):
        for filepath in changes.get('added', {}):
            self.send_alert('added', filepath)
        for filepath in changes.get('removed', {}):
            self.send_alert('removed', filepath)
        for filepath in changes.get('modified', {}):
            self.send_alert('modified', filepath)
