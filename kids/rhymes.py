"""USA Kids Channel - nursery rhyme library (Nunu TV style).

Classic public-domain rhymes, each with: lyric lines, scene keys, a marimba
melody (note names + eighth-note lengths), SEO title/keywords and thumb words.
"""
import datetime as _dt

NOTE = {
    "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.00,
    "A3": 220.00, "B3": 246.94,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.00,
    "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99,
    "A5": 880.00,
    "R": 0.0,   # rest
}

# (note, eighths)
WHEELS_TUNE = [("G4",1),("G4",1),("G4",1),("A4",1),("B4",2),("C5",1),("C5",1),
               ("B4",1),("C5",1),("D5",2),("C5",1),("B4",1),("A4",1),("G4",3)]
TWINKLE_TUNE = [("C4",1),("C4",1),("G4",1),("G4",1),("A4",1),("A4",1),("G4",2),
                ("F4",1),("F4",1),("E4",1),("E4",1),("D4",1),("D4",1),("C4",2),
                ("G4",1),("G4",1),("F4",1),("F4",1),("E4",1),("E4",1),("D4",2)]
MONKEYS_TUNE = [("E4",1),("E4",1),("E4",1),("C4",1),("E4",1),("E4",1),("G4",2),("R",1),
                ("G4",1),("G4",1),("G4",1),("E4",1),("G4",1),("G4",1),("C5",2),("R",1)]
LONDON_TUNE = [("D4",1),("E4",1),("F4",1),("G4",2),("A4",1),("G4",1),("F4",1),
               ("E4",1),("F4",1),("G4",2)]
FINGER_TUNE = [("C4",2),("C4",1),("C4",1),("C4",1),("D4",1),("E4",2),("E4",1),("D4",2),
               ("R",1),("C4",2),("C4",1),("C4",1),("C4",1),("D4",1),("E4",2),("E4",1),("D4",2)]
RAIN_TUNE = [("C4",2),("C4",1),("D4",1),("E4",2),("E4",1),("D4",1),("C4",1),
             ("D4",1),("E4",1),("D4",1),("C4",2)]
SHOULDERS_TUNE = [("C4",1),("C4",1),("C4",1),("C4",1),("D4",2),("E4",2),("D4",2),
                  ("C4",1),("C4",1),("C4",1),("C4",1),("D4",2),("E4",2)]
DUCKS_TUNE = [("G4",2),("E4",1),("E4",1),("D4",2),("G4",2),("E4",1),("E4",1),("D4",2),
              ("G4",2),("A4",1),("A4",1),("G4",2),("E4",2),("D4",2)]

RHYMES = [
    {
        "id": "wheels_bus",
        "title": "Wheels on the Bus",
        "title_full": "Wheels on the Bus | Nursery Rhymes & Kids Songs",
        "thumb_words": ["WHEELS", "ON THE BUS"],
        "tune": WHEELS_TUNE,
        "keywords": ("wheels on the bus, nursery rhymes, kids songs, baby songs, "
                     "wheels on the bus for kids, bus song, children songs, toddler songs"),
        "lines": [
            ("The wheels on the bus go round and round.", "wheels"),
            ("Round and round, round and round.", "wheels_echo"),
            ("The wipers on the bus go swish, swish, swish.", "wipers"),
            ("The horn on the bus goes beep, beep, beep.", "horn"),
            ("The babies on the bus go wa, wa, wa.", "babies"),
            ("The mommies on the bus go shh, shh, shh.", "mommies"),
            ("The animals on the bus go oink, oink, oink.", "animals"),
            ("The wheels on the bus go round and round, all day long!", "finale"),
        ],
    },
    {
        "id": "twinkle",
        "title": "Twinkle Twinkle Little Star",
        "title_full": "Twinkle Twinkle Little Star | Lullaby for Kids",
        "thumb_words": ["TWINKLE", "LITTLE STAR"],
        "tune": TWINKLE_TUNE,
        "keywords": ("twinkle twinkle little star, nursery rhymes, lullaby, kids songs, "
                     "baby lullaby, star song, children songs, bedtime music"),
        "lines": [
            ("Twinkle, twinkle, little star.", "star"),
            ("How I wonder what you are.", "wonder"),
            ("Up above the world so high.", "high"),
            ("Like a diamond in the sky.", "diamond"),
            ("Twinkle, twinkle, little star.", "star"),
            ("How I wonder what you are.", "wonder"),
        ],
    },
    {
        "id": "abc_song",
        "title": "ABC Song",
        "title_full": "ABC Song | Learn the Alphabet for Toddlers",
        "thumb_words": ["ABC", "SONG!"],
        "tune": TWINKLE_TUNE,
        "keywords": ("abc song, alphabet song, learn abc, abc for kids, nursery rhymes, "
                     "phonics song, alphabet for toddlers, kids learning songs"),
        "lines": [
            ("A, B, C, D, E, F, G.", "letters1"),
            ("H, I, J, K. L M N O P.", "letters2"),
            ("Q, R, S. T, U, V.", "letters3"),
            ("W, X, Y and Z.", "letters4"),
            ("Now I know my A B Cs.", "nowknow"),
            ("Next time won't you sing with me?", "nexttime"),
        ],
    },
    {
        "id": "five_monkeys",
        "title": "Five Little Monkeys",
        "title_full": "Five Little Monkeys Jumping on the Bed | Fun Kids Song",
        "thumb_words": ["5 MONKEYS", "JUMPING!"],
        "tune": MONKEYS_TUNE,
        "keywords": ("five little monkeys, monkeys jumping on the bed, nursery rhymes, "
                     "kids songs, counting song, baby songs, funny kids songs"),
        "lines": [
            ("Five little monkeys jumping on the bed.", "jump5"),
            ("One fell off and bumped his head.", "fell"),
            ("Mama called the doctor and the doctor said:", "mama"),
            ("No more monkeys jumping on the bed!", "doctor"),
            ("Four little monkeys jumping on the bed.", "jump4"),
            ("One fell off and bumped his head.", "fell"),
            ("Mama called the doctor and the doctor said:", "mama"),
            ("No more monkeys jumping on the bed!", "doctor"),
        ],
    },
    {
        "id": "five_ducks",
        "title": "Five Little Ducks",
        "title_full": "Five Little Ducks Went Out One Day | Counting Song for Kids",
        "thumb_words": ["5 DUCKS", "COUNT!"],
        "tune": DUCKS_TUNE,
        "keywords": ("five little ducks, duck song, nursery rhymes, counting song, "
                     "kids songs, baby songs, animal songs for children"),
        "lines": [
            ("Five little ducks went out one day.", "ducks"),
            ("Over the hills and far away.", "over"),
            ("Mother duck said, quack, quack, quack.", "quack"),
            ("And all of the five little ducks came back.", "cameback"),
        ],
    },
    {
        "id": "finger_family",
        "title": "Finger Family",
        "title_full": "Finger Family Song | Daddy Finger Nursery Rhyme",
        "thumb_words": ["FINGER", "FAMILY"],
        "tune": FINGER_TUNE,
        "keywords": ("finger family, daddy finger, finger family song, nursery rhymes, "
                     "kids songs, baby songs, family song for children"),
        "lines": [
            ("Daddy finger, daddy finger, where are you?", "daddy"),
            ("Here I am, here I am, how do you do?", "daddy_here"),
            ("Mommy finger, mommy finger, where are you?", "mommy"),
            ("Here I am, here I am, how do you do?", "mommy_here"),
            ("Baby finger, baby finger, where are you?", "babyf"),
            ("Here I am, here I am, how do you do?", "babyf_here"),
        ],
    },
    {
        "id": "london_bridge",
        "title": "London Bridge Is Falling Down",
        "title_full": "London Bridge Is Falling Down | Classic Nursery Rhyme",
        "thumb_words": ["LONDON", "BRIDGE"],
        "tune": LONDON_TUNE,
        "keywords": ("london bridge is falling down, london bridge, nursery rhymes, "
                     "classic kids songs, baby songs, children songs, sing along"),
        "lines": [
            ("London Bridge is falling down.", "bridge"),
            ("Falling down, falling down.", "falling"),
            ("London Bridge is falling down,", "bridge"),
            ("My fair lady.", "lady"),
        ],
    },
    {
        "id": "rain_rain",
        "title": "Rain Rain Go Away",
        "title_full": "Rain Rain Go Away | Kids Song about Weather",
        "thumb_words": ["RAIN RAIN", "GO AWAY"],
        "tune": RAIN_TUNE,
        "keywords": ("rain rain go away, kids songs, weather song, nursery rhymes, "
                     "baby songs, children songs, toddler learning"),
        "lines": [
            ("Rain, rain, go away.", "rain"),
            ("Come again another day.", "another"),
            ("Little baby wants to play.", "play"),
            ("Rain, rain, go away.", "sun"),
        ],
    },
    {
        "id": "head_shoulders",
        "title": "Head, Shoulders, Knees and Toes",
        "title_full": "Head Shoulders Knees and Toes | Exercise Song for Kids",
        "thumb_words": ["HEAD &", "SHOULDERS!"],
        "tune": SHOULDERS_TUNE,
        "keywords": ("head shoulders knees and toes, exercise song for kids, "
                     "body parts song, nursery rhymes, kids songs, toddler dance"),
        "lines": [
            ("Head, shoulders, knees and toes, knees and toes.", "cycle"),
            ("Eyes and ears and mouth and nose.", "face"),
            ("Head, shoulders, knees and toes, knees and toes.", "cycle"),
            ("Eyes and ears and mouth and nose.", "face"),
        ],
    },
]


def day_rhymes(day=None):
    """Pick the 3-rhyme compilation of the day (rotating, never repeating
    the same combination two days in a row)."""
    if day is None:
        day = _dt.date.today().toordinal()
    n = len(RHYMES)
    start = (day * 3) % n
    return [RHYMES[(start + i) % n] for i in range(3)]
