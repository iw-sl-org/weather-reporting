import sys
import json

from helpers import *

#Arguments send by position:
    # 0.script_name
    # 1.pete_email
    # 2.pete_pw
    # 3.pete_key
    # 4.sl_target_org
    # 5.sl_target_pspace
    # 6.sl_project
    # 7.pete_target_system
    # 8.pete_main_page

if __name__ == "__main__":
   
    # Capture arguments
    pete_email = sys.argv[1]
    pete_pw = sys.argv[2]
    pete_key = sys.argv[3]
    sl_org = sys.argv[4]
    sl_pspace = sys.argv[5]
    sl_project = sys.argv[6]


    # Print arguments
    print(f"""-- Command line arguments --
        pete_email: {pete_email}
        pete_pw: {pete_pw}
        pete_key: {pete_key}
        sl_org: {sl_org}
        sl_project_space: {sl_pspace}
        sl_project: {sl_project}""")
    
    # Authenticate PETE
    pete_token = pete_auth(pete_email, pete_pw, pete_key)

    # Pete Code Review
    code_review_report = pete_code_review(pete_key, pete_token, sl_org, sl_pspace, sl_project)

    report_file_name = "code-review-report.json"

    with open(report_file_name, "w") as file:
        json.dump(code_review_report, file, indent=4)

    print(f"--- Code review report saved to {report_file_name} file.---")