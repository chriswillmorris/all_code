OT = "Old Testament"
NT = "New Testament"

Testaments = [OT,NT]

# NOTE: Psalms and Proverbs have been intentionally left out
Genesis = 'Genesis'
Exodus = 'Exodus'
Leviticus = 'Leviticus'
Numbers = 'Numbers'
Deuteronomy = 'Deuteronomy'
Joshua = 'Joshua'
Judges = 'Judges'
Ruth = 'Ruth'
FirstSamuel = '1st Samuel'
SecondSamuel = '2nd Samuel'
FirstKings = '1st Kings'
SecondKings = '2nd Kings'
FirstChronicles = '1st Chronicles'
SecondChronicles = '2nd Chronicles'
Ezra = 'Ezra'
Nehemiah = 'Nehemiah'
Esther = 'Esther'
Job = 'Job'
Ecclesiastes = 'Ecclesiastes'
SongOfSolomon = 'Song Of Solomon'
Isaiah = 'Isaiah'
Jeremiah = 'Jeremiah'
Lamentations = 'Lamentations'
Ezekiel = 'Ezekiel'
Daniel = 'Daniel'
Hosea = 'Hosea'
Joel = 'Joel'
Amos = 'Amos'
Obadiah = 'Obadiah'
Jonah = 'Jonah'
Micah = 'Micah'
Nahum = 'Nahum'
Habakkuk = 'Habakkuk'
Zephaniah = 'Zephaniah'
Haggai = 'Haggai'
Zechariah = 'Zechariah'
Malachi = 'Malachi'
Matthew = 'Matthew'
Mark = 'Mark'
Luke = 'Luke'
John = 'John'
Acts = 'Acts'
Romans = 'Romans'
FirstCorinthians = '1st Corinthians'
SecondCorinthians = '2nd Corinthians'
Galatians = 'Galatians'
Ephesians = 'Ephesians'
Philippians = 'Philippians'
Colossians = 'Colossians'
FirstThessalonians = '1st Thessalonians'
SecondThessalonians = '2nd Thessalonians'
FirstTimothy = '1st Timothy'
SecondTimothy = '2nd Timothy'
Titus = 'Titus'
Philemon = 'Philemon'
Hebrews = 'Hebrews'
James = 'James'
FirstPeter = '1st Peter'
SecondPeter = '2nd Peter'
FirstJohn = '1st John'
SecondJohn = '2nd John'
ThirdJohn = '3rd John'
Jude = 'Jude'
Revelation = 'Revelation'
NoBook = 'No Book'

OTBooks = [ Genesis,
Exodus,
Leviticus,
Numbers,
Deuteronomy,
Joshua,
Judges,
Ruth,
FirstSamuel,
SecondSamuel,
FirstKings,
SecondKings,
FirstChronicles,
SecondChronicles,
Ezra,
Nehemiah,
Esther,
Job,
Ecclesiastes,
SongOfSolomon,
Isaiah,
Jeremiah,
Lamentations,
Ezekiel,
Daniel,
Hosea,
Joel,
Amos,
Obadiah,
Jonah,
Micah,
Nahum,
Habakkuk,
Zephaniah,
Haggai,
Zechariah,
Malachi]



NTBooks = [Matthew,
Mark,
Luke,
John,
Acts,
Romans,
FirstCorinthians,
SecondCorinthians,
Galatians,
Ephesians,
Philippians,
Colossians,
FirstThessalonians,
SecondThessalonians,
FirstTimothy,
SecondTimothy,
Titus,
Philemon,
Hebrews,
James,
FirstPeter,
SecondPeter,
FirstJohn,
SecondJohn,
ThirdJohn,
Jude,
Revelation]

TestamentToBookList = {OT:OTBooks, NT:NTBooks}

BookList = OTBooks + NTBooks

NumChaptersList = [ 50,
40,
27,
36,
34,
24,
21,
4,
31,
24,
22,
25,
29,
36,
10,
13,
10,
42,
12,
8,
66,
52,
5,
48,
12,
14,
3,
9,
1,
4,
7,
3,
3,
3,
2,
14,
4,
28,
16,
24,
21,
28,
16,
16,
13,
6,
6,
4,
4,
5,
3,
6,
4,
3,
1,
13,
5,
5,
3,
5,
1,
1,
1,
22]

BooksToChapters = dict(zip(BookList,NumChaptersList))

