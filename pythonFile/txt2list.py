# pythonFile/txt2list.py
import pandas as pd
import re

class ExcelConverter:
    def __init__(self, txt_file, excel_file):
        self.txt_file = txt_file
        self.excel_file = excel_file
        # Sử dụng danh sách các dictionary để lưu trữ dữ liệu có cấu trúc
        # Mỗi dictionary đại diện cho một câu hỏi và các đáp án của nó
        self.data_list = []

    def export_to_excel(self):
        try:
            # Mở và đọc file txt với encoding utf-8
            with open(self.txt_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file đầu vào tại {self.txt_file}")
            return
        except Exception as e:
            print(f"Lỗi khi đọc file {self.txt_file}: {e}")
            return

        current_question_data = None 

        for line in lines:
            line = line.strip() # Loại bỏ khoảng trắng thừa ở đầu và cuối dòng
            if not line:
                continue # Bỏ qua các dòng trống

            # --- Nhận diện dòng câu hỏi ---
            # Dùng regex để tìm dòng bắt đầu bằng "Question" theo sau là số và dấu hai chấm
            # Nhóm (.*) sẽ lấy toàn bộ phần text sau dấu hai chấm
            question_match = re.match(r"Question\s*\d+:(.*)", line, re.IGNORECASE)
            if question_match:
                # Nếu đang xử lý một câu hỏi cũ (current_question_data không rỗng), lưu nó vào danh sách
                if current_question_data:
                    self.data_list.append(current_question_data)

                # Bắt đầu một khối câu hỏi mới
                current_question_data = {
                    "Question": question_match.group(1).strip(), # Lấy nội dung câu hỏi
                    "A": "", # Khởi tạo các đáp án là chuỗi rỗng (phòng trường hợp thiếu)
                    "B": "",
                    "C": "",
                    "D": ""
                }
            # --- Nhận diện dòng đáp án (chỉ khi đang trong một khối câu hỏi) ---
            elif current_question_data: # Đảm bảo rằng chúng ta đã xác định được một câu hỏi trước đó
                # Kiểm tra xem dòng có bắt đầu bằng "A.", "B.", "C.", "D." không
                answer_match_a = re.match(r"A\.(.*)", line)
                answer_match_b = re.match(r"B\.(.*)", line)
                answer_match_c = re.match(r"C\.(.*)", line)
                # Lưu ý: dùng [DÐ] để chấp nhận cả "D." hoặc "Ð." (do hàm fixIncorrectLetter có thể chưa hoàn hảo)
                answer_match_d = re.match(r"[DÐ]\.(.*)", line)

                if answer_match_a:
                    # Lấy nội dung sau "A."
                    current_question_data["A"] = answer_match_a.group(1).strip()
                elif answer_match_b:
                     # Lấy nội dung sau "B."
                    current_question_data["B"] = answer_match_b.group(1).strip()
                elif answer_match_c:
                     # Lấy nội dung sau "C."
                    current_question_data["C"] = answer_match_c.group(1).strip()
                elif answer_match_d:
                     # Lấy nội dung sau "D." hoặc "Ð."
                    current_question_data["D"] = answer_match_d.group(1).strip()
                # (Tùy chọn) Xử lý các dòng không phải câu hỏi cũng không phải đáp án A/B/C/D
                # else:
                #     print(f"Cảnh báo: Bỏ qua dòng không mong muốn: {line}")

        # --- Lưu câu hỏi cuối cùng ---
        # Sau khi vòng lặp kết thúc, cần đảm bảo câu hỏi cuối cùng được thêm vào danh sách
        if current_question_data:
            self.data_list.append(current_question_data)

        # --- Tạo DataFrame và Xuất Excel ---
        if not self.data_list:
            print("Không tìm thấy dữ liệu có cấu trúc trong file đầu vào.")
            return

        try:
            # Tạo DataFrame từ danh sách các dictionary
            # Cách này tự động xử lý các giá trị bị thiếu (sẽ là chuỗi rỗng đã khởi tạo)
            df = pd.DataFrame(self.data_list)

            # Đảm bảo đúng thứ tự cột và đổi tên cột cho đẹp
            df = df[["Question", "A", "B", "C", "D"]] # Chọn và sắp xếp cột
            df.rename(columns={
                "Question": "Questions", # Đổi tên cột
                "A": "Answer A",
                "B": "Answer B",
                "C": "Answer C",
                "D": "Answer D"
            }, inplace=True)

        except Exception as e:
            print(f"Lỗi khi tạo DataFrame: {e}")
            return

        try:
            # Xuất DataFrame ra file Excel
            df.to_excel(self.excel_file, index=False) # index=False để không ghi chỉ số dòng của DataFrame vào Excel
            print(f"Dữ liệu đã được ghi thành công vào {self.excel_file}")
        except Exception as e:
            print(f"Lỗi khi ghi file Excel {self.excel_file}: {e}")