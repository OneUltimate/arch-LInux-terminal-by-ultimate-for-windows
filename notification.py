from winotify import Notification

def show_notification(used_percent):
    toast = Notification(
        app_id="System Monitor",  
        title=f'Critical memory: {used_percent}%',
        msg='Free virtual memory is critically low!',
        duration="short"
    )
    toast.show()

