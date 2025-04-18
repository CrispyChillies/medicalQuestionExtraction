from ocr_pdf import OCR
from extract_file import ExtractFile
from txt2list import ExcelConverter

pdf_link = "/media/aaronpham5504/New Volume/Project/OCR/data/pdf/Module GPDC-1.pdf"
ocr = OCR(pdf_link)
doc_list = ocr.pdf_to_string()

doc_list = "".join(doc_list)
doc_list = doc_list.splitlines()
doc_list = doc_list[1:]

Paragraph = ExtractFile.concatenate_paragraph(doc_list)
block_question = ExtractFile.format_to_paragraph(Paragraph)

structured_data = ExtractFile.extract_questions_and_answers(block_question)
structured_data = ExtractFile.fixIncorrectLetter(structured_data)

output_file = "txt/questions_and_answers.txt"
excel_file = "excelQuestions/questions_and_answers.xlsx"
ExtractFile.writeResult(output_file, structured_data)

excel = ExcelConverter(output_file, excel_file)
excel.export_to_excel()
