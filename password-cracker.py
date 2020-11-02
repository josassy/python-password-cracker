import hashlib

def main():
  # add all words to python dict
  with open('wordlist.txt', 'r') as wordlist:
    dictionary = {}
    for word in wordlist:
      dictionary[word] = True

  # load in all hashes to dictionary
  saltDict = {}
  noSaltHashes = {}
  with open('hashes.txt', 'r') as hashes:
    for hashLine in hashes:
      [name, salt, hashPassword] = hashLine.split(':')
      hashPassword = hashPassword.strip('\n')
      # if salt is empty, add to dictionary
      if not salt:
        noSaltHashes[hashPassword] = name
      else:
        saltDict[salt] = { hashPassword: name }

  # finally, copy over no salt hashes to empty key
  saltDict[''] = noSaltHashes

  # we are now ready to process everything.
  passwords = {}
  for salt in saltDict:
    if passwords:
      passwords.update(crackPassword(saltDict[salt], salt, dictionary))
    else:
      passwords = crackPassword(saltDict[salt], salt, dictionary)
  # crackedPasswords = crackPassword(noSaltHashes, '', dictionary)

  with open('passwords.txt', 'w') as outfile:
    for name in sorted(passwords.keys()):
      outfile.write(f'{name}:{passwords[name]}\n')

def crackPassword(hashes: dict, salt: str, dictionary: dict) -> dict:
  # first simple pass, plain hash everything
  matches = 0
  crackedPasswords = {}
  for dictWord in dictionary:
    dictWord = dictWord.strip('\n')
    wordsToTry = genModifications(dictWord)
    for word in wordsToTry:
      word = word + salt
      hashedWord = hashlib.md5(word.encode()).hexdigest()
      if hashedWord in hashes:
        word = word.strip(salt)
        print(f"match: {word} -> {hashedWord} ({hashes[hashedWord]})")
        matches = matches + 1
        crackedPasswords[hashes[hashedWord]] = word
  return crackedPasswords     

def genModifications(word: str):
  result = [word.lower(), word.upper(), word.title()]
  for number in range(9):
    result.append(word + str(number))
    result.append(str(number) + word)
  # for symbol in "~`!@#$%^&*()_-+={[}]|<,>.?/":
  for symbol in "1!":
    result.append(word + symbol)
    result.append(symbol + word)

  result.append(word.translate(str.maketrans('eEsSaAoObBtTiI', '33$$@@00887711')))
  result.append(word.translate(str.maketrans('eEsSaAoObBtTiI', '33$$@@008877!!')))
  result.append(word.translate(str.maketrans('aAoO', '@@00')))
  result.append(word.translate(str.maketrans('eE', '33')))
  result.append(word.translate(str.maketrans('sS', '$$')))
  # print(result)
  return result

if __name__ == "__main__":
    main()
