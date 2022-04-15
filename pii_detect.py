from operator import index
import os
import csv
from importlib_metadata import files
from loguru import logger
from pathlib import Path
from Send_Alert import send_alert
import re




current_dir = os.getcwd()


def generate_email(received_contents):
    default = "-"
    expected_content = dict.fromkeys(['current_user', 'fileName', 'pii', 'mssg'], default)

    for content in expected_content:
        if content in received_contents:
            expected_content[content] = received_contents[content]
        else:
            logger.warning(f"The value for {content} was not passed to write failure email. Default value {default} will be used")
    send_alert_path = Path(current_dir+"/send_alert_email.html")

    print(send_alert_path)

    if send_alert_path.exists() and send_alert_path.is_file():
        with open(str(send_alert_path), "r") as message:
            html = message.read().format(**expected_content)
    else:
        logger.critical("SEND_ALERT_TEMPLATE_PATH does not exists so dumping expected content as string into email")
        html = f"ERROR: SEND_ALERT_TEMPLATE_PATH was not set or does not exist so dumping email content as string:<br/>{expected_content}"

    return html



def searchPII():
    
    with open("student_Info.csv",'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        print(header)
        pii = 0
        for row in reader:
            if 'SSN' in header:
                if re.fullmatch(r'\d{3}-\d{2}-\d{4}', str(row[header.index('SSN')])):
                    if 'SSN':
                        row[header.index('SSN')] = 'xxx-xx-xxxx' # We dont know the index
                        print(row)
                        pii = 'SSN'
            elif 'Social Security Number' in header:
                if re.fullmatch(r'\d{3}-\d{2}-\d{4}', str(row[header.index('Social Security Number')])):
                    if 'Social Security Number':
                        row[header.index('Social Security Number')] = 'xxx-xx-xxx' # We dont know the index
                        print(row)
                        pii = "Social Security Number"
            else:
                print(row)
        if pii != 0:
            send_Alert("AUTHORIZED_USER", "student_Info.csv", pii)
        
            

            
def send_Alert(current_user, fileName, pii):
    mssg = "Extreme caution."
    email_contents = {
        "current_user": current_user, 
        "fileName" : fileName,
        "pii" : pii, 
        "mssg": mssg,
        
}
    body = generate_email(email_contents)
    send_alert(body=body, subject="ALERT! Personal Identifiable Information Detected!", files=[]) 

if __name__ == '__main__':
    searchPII()
    