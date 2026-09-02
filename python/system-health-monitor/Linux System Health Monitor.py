import psutil
from datetime import datetime


def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as error:
        print(f"Error getting CPU usage: {error}")
        return "N/A"


def get_ram_usage():
    try:
        memory = psutil.virtual_memory()
        return memory.percent
    except Exception as error:
        print(f"Error getting RAM usage: {error}")
        return "N/A"


def get_disk_usage():
    try:
        disk = psutil.disk_usage('/')
        return disk.percent
    except Exception as error:
        print(f"Error getting Disk usage: {error}")
        return "N/A"


def get_processes():
    try:
        process_list = []

        for process in psutil.process_iter(['name']):
            process_name = process.info['name']

            if process_name and process_name not in process_list:
                process_list.append(process_name)

        return process_list[:10]

    except Exception as error:
        print(f"Error getting processes: {error}")
        return []


def generate_report():
    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()
    processes = get_processes()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = "\n===== SYSTEM REPORT =====\n\n"

    report += f"CPU Usage  : {cpu}%\n"
    report += f"RAM Usage  : {ram}%\n"
    report += f"Disk Usage : {disk}%\n\n"

    report += "Top Processes:\n"

    for process in processes:
        report += f"- {process}\n"

    report += f"\nReport Generated: {current_time}\n"

    return report


def save_report(report):
    try:
        with open("system_report.txt", "w") as file:
            file.write(report)

        print("Report saved successfully!")

    except Exception as error:
        print(f"Error saving report: {error}")


def check_alerts(cpu, ram, disk):

    print("\n===== ALERT STATUS =====")

    if cpu != "N/A" and cpu > 80:
        print("WARNING: High CPU Usage!")

    if ram != "N/A" and ram > 80:
        print("WARNING: High RAM Usage!")

    if disk != "N/A" and disk > 90:
        print("WARNING: Disk Space Critical!")

    print("Monitoring Complete.")


def main():

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()

    report = generate_report()

    print(report)

    save_report(report)

    check_alerts(cpu, ram, disk)


main()


<img width="257" height="281" alt="image" src="https://github.com/user-attachments/assets/0562e5cf-1b5b-42d3-8238-0d76388e76dd" />
