import string

with open("bible.txt", 'r') as bible:
  word_list = {}
  for line in bible:
    for word in line.split(' '):
      word = word.translate(str.maketrans('', '', string.punctuation)).strip('\n[]()').lower()
      if word and not word.isnumeric() and word not in word_list:
        word_list[word] = True

with open("wordlist.txt", "w") as output:
  for word in word_list:
    output.write(word)
    output.write('\n')

