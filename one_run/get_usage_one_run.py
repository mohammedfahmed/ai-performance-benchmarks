import psutil
import time
import os
import csv
from datetime import datetime

def get_ollama_processes_usage(csv_writer):
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # Check if the process name contains "ollama"
            if 'ollama' in proc.info['name'].lower():
                config_file_path = "config.txt"
                with open(config_file_path, 'r') as file:
                    for line in file:
                        if line.startswith("model_name="):
                            llm_model = line.split('=')[1].strip()
                            break 
                pid = proc.info['pid']
                name = proc.info['name']
                cpu_percent = proc.info['cpu_percent']
                memory_info = proc.info['memory_info']
                memory_usage = memory_info.rss / (1024 * 1024 * 1024)  # Convert to GB

                # Capture the current timestamp
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Print the data to the console
                print(f"(PID: {pid}) | CPU: {cpu_percent}% | Memory: {memory_usage:.2f} GB | LLM Model: {llm_model} | Timestamp: {timestamp}")

                # Save the results to the CSV file, including the timestamp
                csv_writer.writerow([timestamp, pid, name, cpu_percent, memory_usage, llm_model])

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle processes that might terminate or have restricted access
            continue

# Function to monitor the processes and save them to CSV
def monitor_ollama_usage():

    with open('config.txt', "w") as file:
        file.write(f"model_name= ")

    # Open the CSV file in append mode to save data over time
    with open('ollama_process_usage.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        
        # Write headers if the file is empty
        if file.tell() == 0:
            csv_writer.writerow(['Timestamp', 'PID', 'Name', 'CPU (%)', 'Memory (GB)', 'LLM Model'])
        
        while True:
            get_ollama_processes_usage(csv_writer)
            time.sleep(1)  # Wait for 1 second before checking again

if __name__ == '__main__':
    monitor_ollama_usage()
