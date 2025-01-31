import datetime
import os
import sys

def parse_timestamp(line):
    # Implement the logic to parse the timestamp from the log line
    # This is a placeholder implementation
    try:
        return datetime.datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def find_log_position(file, target_datetime):
    low, high = 0, file.seek(0, 2)
    result = None
    while low <= high:
        mid = (low + high) // 2
        file.seek(mid)
        if mid != 0:
            file.readline()
        pos = file.tell()
        line = file.readline()
        if not line:
            high = mid - 1
            continue
        line_decoded = line.decode('utf-8', 'ignore')
        line_dt = parse_timestamp(line_decoded)
        print(f"low: {low}, high: {high}, mid: {mid}, pos: {pos}, line_dt: {line_dt}")  # Debug statement
        if line_dt is None:
            high = mid - 1
            continue
        if line_dt < target_datetime:
            low = pos + len(line)
        else:
            result = pos
            high = mid - 1
    if result is not None:
        return result
    else:
        return low

def extract_logs_for_date(file_path, target_date_str, output_dir='output'):
    target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d')
    next_date = target_date + datetime.timedelta(days=1)
    with open(file_path, 'rb') as file:
        start_pos = find_log_position(file, target_date)
        end_pos = find_log_position(file, next_date)
        print(f"Start position: {start_pos}, End position: {end_pos}")  # Debug statement
        if start_pos >= end_pos:
            print(f"No logs found for date {target_date_str}")
            return
        file.seek(start_pos)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = os.path.join(output_dir, f'output_{target_date_str}.txt')
        with open(output_file, 'wb') as out_f:
            while file.tell() < end_pos:
                line = file.readline()
                if not line:
                    break
                out_f.write(line)
        print(f"Logs for date {target_date_str} have been written to {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        return
    target_date_str = sys.argv[1]
    try:
        datetime.datetime.strptime(target_date_str, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Expected YYYY-MM-DD.")
        return
    file_path = 'logs_2024.log'
    if not os.path.exists(file_path):
        print(f"Log file {file_path} does not exist.")
        return
    extract_logs_for_date(file_path, target_date_str)

if __name__ == "__main__":
    main()