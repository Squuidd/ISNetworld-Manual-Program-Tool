import glob
import os
import docx

chosen_file = input("Choose file: \n")

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = f"Safety Programs/{chosen_file}"
abs_file_path = os.path.join(script_dir, rel_path)

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

print(getText(abs_file_path))
