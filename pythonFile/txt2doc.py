import re
import pickle
from extract_file import ExtractFile


with open(
    "/media/aaronpham5504/New Volume/Project/OCR/ocr_result/doc_list.pkl", "rb"
) as f:
    ocr_list = pickle.load(f)

ocr_list = "".join(ocr_list)
ocr_list = ocr_list.splitlines()
ocr_list = ocr_list[1:]

finalContext = ExtractFile.concatenate_paragraph(ocr_list)
ExtractFile.writeFile("txt/format.txt", finalContext)

ocr_text = ExtractFile.format_to_paragraph(finalContext)
ExtractFile.writeFile("txt/preprocess.txt", ocr_text)

# Get the structured result
structured_data = ExtractFile.extract_questions_and_answers(ocr_text)
structured_data = ExtractFile.fixIncorrectLetter(structured_data)

# Define the path for the output txt file
output_file = "txt/questions_and_answers.txt"
ExtractFile.writeResult(output_file, structured_data)
