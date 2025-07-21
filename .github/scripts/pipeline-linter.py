# Import libraries
import sys
import json
import csv
from requests.auth import HTTPBasicAuth
from helpers import *

# Arguments send by position:
    # 0.script_name
    # 1.sl_email
    # 2.sl_pw
    # 3.sl_source_org
    # 4.sl_source_pspace
    # 5.sl_source_project

if __name__ == '__main__':

    # Capture arguments
    sl_email = sys.argv[1]
    sl_pw = sys.argv[2]
    sl_org = sys.argv[3]
    sl_pspace = sys.argv[4]
    sl_project = sys.argv[5]
    sl_auth = HTTPBasicAuth(sl_email, sl_pw)

    # Print arguments
    print(f"""-- Command line arguments --
        sl_email: {sl_email}
        sl_pw: {sl_pw}
        sl_org: {sl_org}
        sl_pspace: {sl_pspace}
        sl_project: {sl_project}""")

    # Retrieve and filter tracked only pipelines from the source project
    pipelines = sl_filter_tracked_assets(sl_list_assets(sl_org, sl_pspace, sl_project, sl_auth, "Pipeline"))
    pipelines = [pipeline["name"] for pipeline in pipelines]
    report = {}
    for pipeline in pipelines:
        report[pipeline] = sl_pipeline_linter(sl_org, sl_pspace, sl_project, pipeline, sl_auth)
    
    csv_file = "pipelines-health-report.csv"
    
    # Write to CSV with pipeline name included
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["pipeline", "key", "name", "description", "message_level", "disabled", "score"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for pipeline_name, validations in report.items():
            for row in validations:
                # Add pipeline name to each row
                row_with_pipeline = {"pipeline": pipeline_name, **row}
                writer.writerow(row_with_pipeline)