# Read the file
with open('emote_names.txt', 'r') as file:
    lines = file.readlines()

print(f"Read {len(lines)} lines")

# Process each line to keep only the first word
cleaned_lines = []
seen_words = set()  # Keep track of words we've already seen

for line in lines:
    if line.strip():  # if line is not empty
        words = line.split()
        if words:  # if there are any words
            first_word = words[0]
            if first_word not in seen_words:  # only add if we haven't seen this word before
                cleaned_lines.append(first_word + '\n')
                seen_words.add(first_word)
                print(f"Original: '{line.strip()}' -> Cleaned: '{first_word}'")
            else:
                print(f"Skipping duplicate: '{first_word}'")
    else:
        cleaned_lines.append(line)

print(f"Processed {len(cleaned_lines)} lines")
print(f"Removed {len(lines) - len(cleaned_lines)} duplicates")

# Write back to the file
with open('emote_names.txt', 'w') as file:
    file.writelines(cleaned_lines)

print("File has been written")