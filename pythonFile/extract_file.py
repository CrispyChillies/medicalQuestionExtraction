import re


class ExtractFile:
    def concatenate_paragraph(lines):
        formatted_content = ""
        # Preprocessing step to filter out unwanted patterns like "..1..."
        preprocessed_lines = []
        unwanted_pattern = r"\.\.\d+\.\."  # Matches patterns like "..1..."
        for line in lines:
            # Remove unwanted patterns from each line
            cleaned_line = re.sub(unwanted_pattern, "", line)
            preprocessed_lines.append(cleaned_line)

        # Pattern to identify questions (e.g., "1. ", "2. ")
        question_pattern = r"(?:^|[^.])(?:[^.]{2}|\.[^.])\d+\.|[%\$§]\.|[%\$§]\d\.|\d[%\$§]\.|[a-zA-Z]\d\.|\d[a-zA-Z]\.|s\.|s9"

        # Process lines to concatenate them into paragraphs
        for i, line in enumerate(preprocessed_lines):
            if re.match(question_pattern, line):  # If the line is a new question
                if i > 0:  # Add a space before new questions, except the first one
                    formatted_content += " "
            formatted_content += (
                line.strip()
            )  # Add the current line, removing extra spaces

        return formatted_content

    def writeFile(path, content):
        with open(path, "w") as f:
            f.write(content)
        print(f"Data has been written to {path}")

    # Function to extract questions and answers
    def extract_questions_and_answers(ocr_text):
        # Split into question blocks
        question_blocks = re.split(
            r"\d+\.|[%\$§]\.|[%\$§]\d\.|\d[%\$§]\.|[a-zA-Z]\d\.|\d[a-zA-Z]\.|s\.|s9",
            ocr_text,
        )[
            1:
        ]  # Skip the first empty block before the first question

        # Prepare the output content
        output_content = ""

        for i, block in enumerate(question_blocks):
            # Extract the question and answers
            parts = re.split(
                r"(?=[A-EĐÐ]\.)", block.strip()
            )  # Split before A., B., C., D.
            question = parts[0].strip()  # First part is the question
            answers = [
                part.strip() for part in parts[1:] if part.strip()
            ]  # Remaining parts are answers

            # Format the question and answers
            output_content += f"Question {i+1}: {question}\n"
            for answer in answers:
                output_content += f"{answer}\n"
            output_content += "\n"  # Add a blank line between questions

        return output_content

    def format_to_paragraph(final_context):

        def ensure_all_choices(parts):
            # Extract choices (e.g., A., B., C., D.)
            choice_pattern = r"[A-D]\."
            existing_choices = [
                part for part in parts if re.match(choice_pattern, part.strip())
            ]

            # Create a dictionary of detected choices
            choice_dict = {choice[0]: choice for choice in existing_choices}

            # Add missing choices with placeholders
            for choice in "ABCD":
                if choice not in choice_dict:
                    choice_dict[choice] = f"{choice}. Choice not available"

            # Return sorted choices
            return [choice_dict[choice] for choice in "ABCD"]

        # Split by number pattern to identify questions
        questions = re.split(
            r"\d+\.|[%\$§]\.|[%\$§]\d\.|\d[%\$§]\.|[a-zA-Z]\d\.|\d[a-zA-Z]\.|s\.|s9.",
            final_context,
        )

        # Remove empty strings and strip whitespace
        questions = [q.strip() for q in questions if q.strip()]

        # Format each question with proper spacing
        formatted_questions = []
        for i, question in enumerate(questions, 1):
            # Split question and answers
            parts = re.split(r"([A-EĐÐ]\.)", question)

            # First part is the question
            question_text = parts[0].strip()

            # Ensure all choices exist
            answers = ensure_all_choices(parts[1:])

            # Format answers on separate lines
            answers = []
            choices_found = set()  # To track existing choices

            # Iterate through parts and collect answers
            for j in range(1, len(parts), 2):
                if j + 1 < len(parts):
                    choice = parts[j].strip()  # Choice label (e.g., "A.", "B.")
                    answer_text = parts[j + 1].strip()  # Answer text
                    answers.append(f"{choice} {answer_text}")
                    choices_found.add(choice[0])  # Add the choice letter to the set

            # Add missing choices with placeholders
            for choice in "ABCD":
                if choice not in choices_found:
                    answers.append(f"{choice}. Choice not available")

            # Sort answers to maintain order of A, B, C, D
            answers.sort(key=lambda x: x[0])

            # Combine question and answers
            formatted_q = f"{i}. {question_text}\n" + "\n".join(answers)
            formatted_questions.append(formatted_q)

        # Join with double newlines to create final paragraph
        final_text = "\n\n".join(formatted_questions)

        return final_text

    def writeResult(output_file, structured_data):
        # Open the file in write mode
        with open(output_file, "w") as file:
            file.write(structured_data)
        print(f"Data written to {output_file} successfully!")

    def fixIncorrectLetter(ocr_text):
        corrected_text = re.sub(r"E.", "B.", ocr_text)
        corrected_text = re.sub(r"Ð\.", "D.", corrected_text)
        return corrected_text
