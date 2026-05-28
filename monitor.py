import psutil

cpu = psutil.cpu_percent(interval=1)

print(f"CPU Usage: {cpu}%")