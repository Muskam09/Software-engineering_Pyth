def calculate_total_bytes(file_path):
    with open(file_path, 'r', encoding='utf-8') as log_file:
        total_bytes = sum(
            int(line.split()[9])
            for line in log_file
            if line.split()[9].isdigit()
        )
    return total_bytes
