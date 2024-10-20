def reverse_string(current_str: str) -> str:
    if current_str.isspace() or len(current_str) == 0:
        return current_str
    words_splited = current_str.split()
    result = []
    for word in words_splited:
        letters = [char for char in word if char.isalpha()]
        new_word = []
        for char in word:
            if char.isalpha():
                new_word.append(letters.pop())
            else:
                new_word.append(char)
        result.append(''.join(new_word))
    return ' '.join(result)
