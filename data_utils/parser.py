def print_lines(file, n=10):
    with open(file, 'rb') as datafile:
        lines = datafile.readlines()
    for line in lines[:n]:
        print(line)


# Splits each line of the file into a dictionary of fields
def load_lines(file_name, fields):
    lines = {}
    with open(file_name, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            line_obj = {}
            for i, field in enumerate(fields):
                line_obj[field] = values[i]
            lines[line_obj['lineID']] = line_obj
    return lines


# Groups fields of lines from `loadLines` into conversations based on *movie_conversations.txt*
def load_conversations(file_name, lines, fields):
    conversations = []
    with open(file_name, 'r', encoding='iso-8859-1') as f:
        for line in f:
            values = line.split(" +++$+++ ")
            # Extract fields
            conv_obj = {}
            for i, field in enumerate(fields):
                conv_obj[field] = values[i]
            # Convert string to list (conv_obj["utteranceIDs"] == "['L598485', 'L598486', ...]")
            line_ids = eval(conv_obj["utteranceIDs"])
            # Reassemble lines
            conv_obj["lines"] = []
            for lineId in line_ids:
                conv_obj["lines"].append(lines[lineId])
            conversations.append(conv_obj)
    return conversations


# Extracts pairs of sentences from conversations
def extract_sentence_pairs(conversations):
    qa_pairs = []
    for conversation in conversations:
        # Iterate over all the lines of the conversation
        for i in range(len(conversation["lines"]) - 1):  # We ignore the last line (no answer for it)
            input_line = conversation["lines"][i]["text"].strip()
            target_line = conversation["lines"][i+1]["text"].strip()
            # Filter wrong samples (if one of the lists is empty)
            if input_line and target_line:
                qa_pairs.append([input_line, target_line])
    return qa_pairs



