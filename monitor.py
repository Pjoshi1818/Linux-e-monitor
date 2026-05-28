import psutil
import os
import time


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_system_info():

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    print("=" * 40)
    print(" LINUX SYSTEM RESOURCE MONITOR ")
    print("=" * 40)

    print(f"CPU Usage:    {cpu}%")
    print(f"Memory Usage: {memory}%")
    print(f"Disk Usage:   {disk}%")

    print("\nTop Processes:")
    print("-" * 40)

    processes = []

    for proc in psutil.process_iter(
        ['pid', 'name', 'cpu_percent']
    ):
        try:
            processes.append(proc.info)
        except:
            pass

    processes = sorted(
        processes,
        key=lambda x: x['cpu_percent'],
        reverse=True
    )

    for proc in processes[:10]:
        print(
            f"{proc['pid']}   "
            f"{proc['name']}   "
            f"{proc['cpu_percent']}%"
        )


def kill_process():

    try:
        pid = int(input("\nEnter PID to kill: "))
        os.kill(pid, 9)
        print("Process killed successfully.")

    except Exception as e:
        print("Error:", e)


while True:

    clear_screen()

    show_system_info()

    print("\nOptions:")
    print("k = kill process")
    print("q = quit")
    print("Enter = refresh")

    choice = input("\nChoose: ")

    if choice == "k":
        kill_process()
        input("Press Enter...")

    elif choice == "q":
        break

    else:
        time.sleep(2)