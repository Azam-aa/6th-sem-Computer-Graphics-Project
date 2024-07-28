import os
import csv
from collections import defaultdict

# Function to read attendance from CSV files in a specified folder
def read_attendance_files(folder_path):
    attendance_data = defaultdict(int)
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            with open(os.path.join(folder_path, file_name), 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 1:
                        attendance_data[row[0]] += 1
    return attendance_data

# Function to write monthly attendance stats to "month.csv"
def write_monthly_attendance(attendance_data):
    sorted_attendance = sorted(attendance_data.items(), key=lambda x: x[1], reverse=True)
    with open("month.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Attendance Count'])
        for name, count in sorted_attendance:
            writer.writerow([name, count])

if __name__ == "__main__":
    folder_path = "csv"  # Assuming "csv" folder is in the same directory as this script
    attendance_data = read_attendance_files(folder_path)
    write_monthly_attendance(attendance_data)
    print("Monthly attendance report generated.")
