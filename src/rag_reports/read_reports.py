import os

def read_reports(report_file=None):
    reports = {}
    report_types = ['goodreads', 'reddit']
    
    if report_file:
        # Read the single report file
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if content:
                reports['combined'] = content
            else:
                print(f"Warning: {report_file} is empty.")
        else:
            print(f"Warning: {report_file} not found.")
    else:
        # Read separate report files
        for report_type in report_types:
            filename = f"{report_type}_report.txt"
            filepath = os.path.join('tmp_reports', filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if content:
                    reports[report_type] = content
                else:
                    print(f"Warning: {filename} is empty.")
            else:
                print(f"Warning: {filename} not found.")
    return reports