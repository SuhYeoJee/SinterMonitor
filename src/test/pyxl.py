# import openpyxl

# def save_dict_to_excel(data, filename):
#     wb, ws = openpyxl.Workbook(), openpyxl.Workbook().active
#     ws.append(list(data.keys()))
#     for row in data.values():
#         ws.append(row)
#     wb.save(filename)

# data = {
#     "customer":[
#         {"Name":"Alice","Age":25,"City":"New York"},
#         {"Name":"Bob","Age":30,"City":"Los Angeles"},
#         {"Name":"Charlie","Age":35,"City":"Chicago"},
#     ]
# }

# save_dict_to_excel(data, "output.xlsx")

import pandas as pd

data = {
    "customer":[
        {"Name":"Alice","Age":25,"City":"New York"},
        {"Name":"Bob","Age":30,"City":"Los Angeles"},
        {"Name":"Charlie","Age":35,"City":"Chicago"},
    ],
    "sheet2":[
        {"col1":"val1-1","col2":"val1-2"},
        {"col1":"val2-1","col2":"val2-2"},
        {"col1":"val3-1","col2":"val3-2"},
    ]
}

# ExcelWriter 객체 생성
with pd.ExcelWriter("data.xlsx") as writer:
    # 각 시트별로 데이터프레임 생성하여 엑셀에 저장
    for sheet_name, sheet_data in data.items():
        df = pd.DataFrame(sheet_data)
        df.to_excel(writer, sheet_name=sheet_name, index=False)