import time
from openpyxl import Workbook

def update_excel_with_list(data_list, file_name="updated_data.xlsx"):
    workbook = Workbook()
    sheet = workbook.active

    # 리스트의 각 튜플 항목을 엑셀의 행으로 추가
    for item in data_list:
        sheet.append(item)

    # 엑셀 파일 저장
    workbook.save(file_name)
    print(f"Excel file '{file_name}' updated with {len(data_list)} items.")

def main():
    data_list = []
    file_name = "updated_data.xlsx"

    try:
        while True:
            # 리스트에 새 항목 추가 (여러 개의 데이터로 구성된 튜플)
            new_item = (len(data_list) + 1, f"Item_{len(data_list) + 1}", time.strftime("%Y-%m-%d %H:%M:%S"))
            data_list.append(new_item)
            print(f"New item added: {new_item}")

            # 엑셀 파일 갱신
            update_excel_with_list(data_list, file_name)

            # 1초 대기
            time.sleep(1)
    except KeyboardInterrupt:
        print("Process interrupted. Final Excel file saved.")
        update_excel_with_list(data_list, file_name)

if __name__ == "__main__":
    main()
