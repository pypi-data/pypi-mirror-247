# uniqueWordList
Creates an object with a list of each unique word in a plaintext document.

Install with ```pip install uniqueWordList```

Takes the file path as its input. ```var.wordCount``` returns the list's length, ```var.wordList``` returns the list itself.

```python
import uniqueWordList

test_text = uniqueWordList.getList('someBook.txt', alphanumeric = True)

print(test_text.wordCount)

with open('asdf.txt', 'w') as output:
  output.write(str(test_text.wordList))
  ```

## Strengths, weaknesses, and things to consider
Setting alphanumeric to ```True``` will count any number or alphanumeric combo (ex: 1b, 1e5). Some of these will probably not be real words. It is set to ```False``` by default.

Speaking of things that aren't real words: if there are any typos or deliberate misspellings they will be counted as separate words. Similarily, the plural versions of words will be counted as their own words as well. 

Same goes for people being cut off mid-word. "You stu-" will be counted as ```['you', 'stu']```

Because of how the list is made you might also find an entry like ```['a', 'b', 'c']``` when an author spells out "now I know my A,B,Cs" or similar text. 

Legalese is also common. ```['trademarkcopyright', 'wwwgutenbergorg']``` were both common in lists during tests. The easiest way to avoid these types of words may be to just delete those segments from your text docs manually. 

Overall the accuracy of the lists generated depends entirely on the author's writing style and the quality of the document. Your mileage may vary.

