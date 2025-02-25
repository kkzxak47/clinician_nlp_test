import os
import re
import csv


def clean_transcript(file_path):
    print(f'processing {file_path}')
    """Clean medical transcript files by removing headers, footers and formatting"""
    filename = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    in_footer = False

    for line in lines:
        # Skip header lines
        if line.startswith('Date of Encounter') or line.startswith('Time of Encounter'):
            continue
        if line.startswith(f'DOCTOR {filename}') or line.startswith(f'PATIENT {filename}'):
            continue
        if line.startswith("SECOND PERSON"):
            continue

        # Detect footer section
        if 'PATIENT LEAVES:' in line or 'INFOPRO/' in line:
            in_footer = True
            continue
        if in_footer:
            continue

        # Clean remaining content
        line = line.replace('@', '').replace('DOCTOR', '').replace('PATIENT', '')
        cleaned_lines.append(line.strip())

    return ' '.join(cleaned_lines), filename


def clean_transcripts_in_folder(folder_path):
    """Process all .txt files in a folder and return cleaned content"""
    cleaned_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            cleaned_content = clean_transcript(file_path)
            cleaned_data.append(cleaned_content)
    return cleaned_data


def medical():

    pattern = r'^[.? ]*'
    with open('processed_data/medical/processed_data.txt', 'w', encoding='utf-8') as file:
        for text, filename in clean_transcripts_in_folder('.\data\medical\Transcripts'):

            text = re.sub(pattern, '', text)

            file.write(text)
            file.write('\n')



def non_medical():
    count = 0
    results = []
    # in data/non_medical/train.csv
    # read csv file
    with open('data/non_medical/train.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        for row in reader:
            count += 1
            # print(row[0], type(row[0]))
            dialog = row[0][1:-1]
            processed_dialog = []
            for line in dialog.split('\n'):
                line = line.strip()
                line = line[1:-1]
                if line.startswith(' '):
                    line = line[1:]
                processed_dialog.append(line)
            result = ''.join(processed_dialog)
            results.append(result.strip())
    import random
    # randomly choose 405 items from results
    random.shuffle(results)
    with open('processed_data/non_medical/results.txt', 'w', encoding='utf-8') as file:
        for text in results[:405]:
            file.write(text)
            file.write('\n')


if __name__ == '__main__':
    medical()
    non_medical()
