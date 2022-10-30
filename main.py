import csv, string, os, time, psutil

def elapsed_since(start):
    return time.time() - start

def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss

def track(func):
    def wrapper(*args, **kwargs):
        mem_before = get_process_memory()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = elapsed_since(start)
        mem_after = get_process_memory()
        print("{}: memory before: {}, after: {}, consumed: {}; exec time: {}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before,
            elapsed_time))
        return result
    return wrapper

@track
def main():
    french_dictionary = 'french_dictionary.csv'
    find_words = 'find_words.txt'
    input_file = 't8.shakespeare.txt'
    output = ""
    punctuation = string.punctuation
    frequency = "frequency.csv"

    file = open(french_dictionary, "r")
    reader = csv.reader(file)
    mydict = dict((rows[0],rows[1]) for rows in reader)
    file.close()

    new_dict = {}
    file = open(find_words, "r")
    for word in file:
        temp = word.rstrip('\n')
        if temp in mydict:
            new_dict[temp] = mydict[temp]
    file.close()

    unique_dict = {}
    file = open(input_file, "r")
    for line in file:
        words = line.split()
        for i in range(len(words)):
            key = words[i].lower()
            if key[-1] in punctuation:
                key = key[:-1] 
            if key in new_dict:
                if key not in unique_dict:
                    unique_dict[key] = 0
                else:
                    unique_dict[key] +=1
                word = list(words[i])
                translation = list(new_dict[key])
                if word[0].isupper():
                    translation[0] = translation[0].upper()
                if words[i].isupper():
                    for j in range(len(translation)):
                        translation[j] = translation[j].upper()
                words[i] = "".join(translation)
        line = " ".join(words)
        output += line+"\n"
    file.close()

    output_file = 't8.shakespeare.translated.txt'
    file = open(output_file, "w")
    file.write(output)
    file.close()

    file = open(frequency, "w", newline='')
    writer = csv.writer(file)
    for row in unique_dict.items():
        writer.writerow(row)
    file.close()

if __name__ == "__main__":
    main()