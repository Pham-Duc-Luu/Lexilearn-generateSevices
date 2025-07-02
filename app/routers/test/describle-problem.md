## TODO

This will be a api route to sovle the following problem:

Input is a paragraph (many sentences), your job is

1. verify the input, paragraph should have <= 10 sentences and <= 200 characters. the input should be english

2. extract the reasonable quality of number

- the reasonable quality is when it not too much and too many, it should be caculate base on the number of sentences and meaningful characters.
- please provide the caculator of this quality.

3. After the extraction, the world have to be reference to a record of vocabulary in the database

- you can return the new paragraph that extend from the input with the following pattern

" ... word word ..." -> " ... **{vocabulary_id}[extracted_word]** ... "

\*\* for every data tranfers in the process should be descrilbe by using a BaseModel class
