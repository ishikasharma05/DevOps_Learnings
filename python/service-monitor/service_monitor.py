import subprocess

services = ["ssh", "nginx"]

for service in services:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True
        )

        status = result.stdout.strip()

        if status == "active":
            print(f"{service}: Running")
        else:
            print(f"{service}: Stopped")

    except Exception as error:
        print(f"Error checking {service}: {error}")
