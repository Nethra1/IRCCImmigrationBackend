from flask import jsonify
import pandas as pd
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta
from dateutil import parser
import requests
import json

class Algorithm:
    def algo(self):
        l = []
        k = []
        f = []
        q = []
        respose = requests.get("https://ircc-prod.herokuapp.com/ircc/alldata")
        content = json.loads(respose.text)
        df = pd.DataFrame(content)
        print(df.head())
        visa_data = df
        today = date.today()

        if(9 <= today.month <= 12):
            d1 = date(today.year+1, 1, 6)
        elif(1 <= today.month <= 4):
            d1 = date(today.year, 5, 6)
        elif(5 <= today.month <= 8):
            d1 = date(today.year, 9, 6)

        for j in visa_data['application_date']:
            z = parser.parse(j)
            d0 = date(z.year, z.month, z.day)
            delta = d1 - d0
            l.append(delta.days)

        for j in visa_data['biometric_date']:
            z = parser.parse(j)
            d0 = date(z.year, z.month, z.day)
            delta = d1 - d0
            k.append(delta.days)

        for j in visa_data['medical_update_date']:
            z = parser.parse(j)
            d0 = date(z.year, z.month, z.day)
            delta = d1 - d0
            f.append(delta.days)

        for i in range(0,len(visa_data)):
            q.append(min([l[i],k[i],f[i]]))

        visa_data["visa_applied_days"] = l
        visa_data["biometric_days"] = k
        visa_data["medical_days"] = f
        visa_data["file_submit_days"] = q

        w = []
        for i in range(0,len(visa_data)):
            if(9 <= today.month <= 12):
                if("Winter" in visa_data["intake"][i]):
                    if(visa_data["file_submit_days"][i] >= 120 or visa_data["file_submit_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["file_submit_days"][i] < 120 or visa_data["file_submit_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue

            elif(1 <= today.month <= 4):
                if("Spring" in visa_data["intake"][i]):
                    if(visa_data["file_submit_days"][i] >= 120 or visa_data["file_submit_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["file_submit_days"][i] < 120 or visa_data["file_submit_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue

            elif(5 <= today.month <= 8):
                if("Fall" in visa_data["intake"][i]):
                    if(visa_data["file_submit_days"][i] >= 120 or visa_data["file_submit_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["file_submit_days"][i] < 120 or visa_data["file_submit_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue
        visa_data["file_submit_priority"] = w
        
        w = []
        for i in range(0,len(visa_data)):
            if(9 <= today.month <= 12):
                if("Winter" in visa_data["intake"][i]):
                    if(visa_data["biometric_days"][i] >= 120 or visa_data["biometric_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["biometric_days"][i] < 120 or visa_data["biometric_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue

            elif(1 <= today.month <= 4):
                if("Spring" in visa_data["intake"][i]):
                    if(visa_data["biometric_days"][i] >= 120 or visa_data["biometric_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["biometric_days"][i] < 120 or visa_data["biometric_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue

            elif(5 <= today.month <= 8):
                if("Fall" in visa_data["intake"][i]):
                    if(visa_data["biometric_days"][i] >= 120 or visa_data["biometric_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["biometric_days"][i] < 120 or visa_data["biometric_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue
        visa_data["biometric_days_priority"] = w
        
        w = []
        for i in range(0,len(visa_data)):
            if(9 <= today.month <= 12):
                if("Winter" in visa_data["intake"][i]):
                    if(visa_data["medical_days"][i] >= 120 or visa_data["medical_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["medical_days"][i] < 120 or visa_data["medical_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue

            elif(1 <= today.month <= 4):
                if("Spring" in visa_data["intake"][i]):
                    if(visa_data["medical_days"][i] >= 120 or visa_data["medical_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["medical_days"][i] < 120 or visa_data["medical_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue

            elif(5 <= today.month <= 8):
                if("Fall" in visa_data["intake"][i]):
                    if(visa_data["medical_days"][i] >= 120 or visa_data["medical_days"][i] <= 45):
                        w.append(1)
                    elif(visa_data["medical_days"][i] < 120 or visa_data["medical_days"][i] > 45):
                        w.append(2)
                    else:
                        w.append(4)
                else:
                    w.append(3)
                    continue
        visa_data["medical_updated_priority"] = w
        # print(visa_data.to_json(orient="records"))
        return(visa_data.to_json(orient="records"))

