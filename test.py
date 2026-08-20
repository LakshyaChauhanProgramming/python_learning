def testPangram(str):
    letters = set()
    for i in str.lower():
        if i.isalpha():
            letters.add(i)

    return len(letters) == 26        

print(testPangram("The quick brown fox  lazy dog"))