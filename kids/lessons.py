"""USA Kids Channel - lesson library (deterministic, no LLM).

Each lesson = list of beats. Each beat: (say_text, visual dict).
Visual types drawn by kids/scenes.py:
  letter  - big bouncing letter + word (ABC phonics)
  count   - N cheerful objects + numeral (counting)
  color   - color blob + name (colors song)
  shape   - big shape + name (shapes song)
Intro/outro are added by the renderer automatically.
"""

LESSONS = [
    {
        "id": "abc_phonics_1",
        "title": "ABC Song for Kids | Learn Letters A to L with Fun Phonics",
        "tags": ["abc song", "alphabet for kids", "phonics song", "learn abc",
                 "kids learning video", "preschool learning", "toddler learning",
                 "educational video for kids", "abc for toddlers", "letters for children"],
        "desc": ("Learn the alphabet with USA Kids Channel! In this fun ABC song for kids, "
                 "children learn letters A to L with easy phonics and cheerful pictures. "
                 "Sing along and learn: A is for Apple, B is for Ball and more!"),
        "thumb_words": ["ABC", "Learn Letters!", "Fun"],
        "beats": [
            ("A!", {"type": "letter", "char": "A", "word": "Apple", "accent": (255, 80, 80)}),
            ("A is for Apple.", {"type": "letter", "char": "A", "word": "Apple", "accent": (255, 80, 80)}),
            ("B!", {"type": "letter", "char": "B", "word": "Ball", "accent": (70, 130, 255)}),
            ("B is for Ball.", {"type": "letter", "char": "B", "word": "Ball", "accent": (70, 130, 255)}),
            ("C!", {"type": "letter", "char": "C", "word": "Cat", "accent": (255, 170, 40)}),
            ("C is for Cat.", {"type": "letter", "char": "C", "word": "Cat", "accent": (255, 170, 40)}),
            ("D!", {"type": "letter", "char": "D", "word": "Dog", "accent": (120, 200, 90)}),
            ("D is for Dog.", {"type": "letter", "char": "D", "word": "Dog", "accent": (120, 200, 90)}),
            ("E!", {"type": "letter", "char": "E", "word": "Egg", "accent": (240, 130, 200)}),
            ("E is for Egg.", {"type": "letter", "char": "E", "word": "Egg", "accent": (240, 130, 200)}),
            ("F!", {"type": "letter", "char": "F", "word": "Fish", "accent": (80, 200, 210)}),
            ("F is for Fish.", {"type": "letter", "char": "F", "word": "Fish", "accent": (80, 200, 210)}),
            ("G!", {"type": "letter", "char": "G", "word": "Goat", "accent": (190, 140, 255)}),
            ("G is for Goat.", {"type": "letter", "char": "G", "word": "Goat", "accent": (190, 140, 255)}),
            ("H!", {"type": "letter", "char": "H", "word": "Hat", "accent": (255, 120, 120)}),
            ("H is for Hat.", {"type": "letter", "char": "H", "word": "Hat", "accent": (255, 120, 120)}),
            ("I!", {"type": "letter", "char": "I", "word": "Ice cream", "accent": (130, 220, 150)}),
            ("I is for Ice cream.", {"type": "letter", "char": "I", "word": "Ice cream", "accent": (130, 220, 150)}),
            ("J!", {"type": "letter", "char": "J", "word": "Juice", "accent": (255, 200, 90)}),
            ("J is for Juice.", {"type": "letter", "char": "J", "word": "Juice", "accent": (255, 200, 90)}),
            ("K!", {"type": "letter", "char": "K", "word": "Kite", "accent": (110, 170, 255)}),
            ("K is for Kite.", {"type": "letter", "char": "K", "word": "Kite", "accent": (110, 170, 255)}),
            ("L!", {"type": "letter", "char": "L", "word": "Lion", "accent": (255, 170, 60)}),
            ("L is for Lion.", {"type": "letter", "char": "L", "word": "Lion", "accent": (255, 170, 60)}),
        ],
    },
    {
        "id": "counting_1_10",
        "title": "Counting 1 to 10 for Kids | Fun Numbers Song with Colorful Stars",
        "tags": ["counting for kids", "numbers song", "count 1 to 10", "learn numbers",
                 "kids learning video", "preschool math", "toddler counting",
                 "educational video for kids", "numbers for toddlers", "counting song"],
        "desc": ("Learn to count 1 to 10 with USA Kids Channel! A cheerful counting song for kids "
                 "with colorful stars. Toddlers and preschoolers count along: one, two, three... all "
                 "the way to ten!"),
        "thumb_words": ["1 2 3", "Count to 10!", "Fun"],
        "beats": [
            ("One!", {"type": "count", "n": 1, "word": "One", "accent": (255, 90, 90)}),
            ("Two!", {"type": "count", "n": 2, "word": "Two", "accent": (255, 150, 60)}),
            ("Three!", {"type": "count", "n": 3, "word": "Three", "accent": (255, 220, 60)}),
            ("Four!", {"type": "count", "n": 4, "word": "Four", "accent": (110, 200, 100)}),
            ("Five!", {"type": "count", "n": 5, "word": "Five", "accent": (90, 200, 220)}),
            ("Six!", {"type": "count", "n": 6, "word": "Six", "accent": (90, 150, 255)}),
            ("Seven!", {"type": "count", "n": 7, "word": "Seven", "accent": (170, 120, 255)}),
            ("Eight!", {"type": "count", "n": 8, "word": "Eight", "accent": (255, 120, 200)}),
            ("Nine!", {"type": "count", "n": 9, "word": "Nine", "accent": (255, 100, 140)}),
            ("Ten!", {"type": "count", "n": 10, "word": "Ten", "accent": (100, 220, 180)}),
            ("Great job! Let us count together one more time!", {"type": "count", "n": 10, "word": "1 2 3 4 5 6 7 8 9 10", "accent": (255, 190, 60)}),
        ],
    },
    {
        "id": "colors_song",
        "title": "Colors Song for Kids | Learn Red, Blue, Yellow and Green",
        "tags": ["colors for kids", "colors song", "learn colors", "colors for toddlers",
                 "kids learning video", "preschool learning", "educational video for kids",
                 "color song for children", "learning colors for babies", "fun colors"],
        "desc": ("Learn colors with USA Kids Channel! A bright colors song for kids: red, blue, "
                 "yellow, green, orange, purple, pink and brown. Toddlers love learning colors "
                 "with fun, colorful animations!"),
        "thumb_words": ["Colors!", "Red Blue Yellow", "Fun"],
        "beats": [
            ("Red!", {"type": "color", "name": "Red", "fill": (235, 60, 60)}),
            ("The apple is red.", {"type": "color", "name": "Red", "fill": (235, 60, 60)}),
            ("Blue!", {"type": "color", "name": "Blue", "fill": (60, 120, 240)}),
            ("The sky is blue.", {"type": "color", "name": "Blue", "fill": (60, 120, 240)}),
            ("Yellow!", {"type": "color", "name": "Yellow", "fill": (250, 210, 50)}),
            ("The sun is yellow.", {"type": "color", "name": "Yellow", "fill": (250, 210, 50)}),
            ("Green!", {"type": "color", "name": "Green", "fill": (70, 190, 90)}),
            ("The leaf is green.", {"type": "color", "name": "Green", "fill": (70, 190, 90)}),
            ("Orange!", {"type": "color", "name": "Orange", "fill": (255, 140, 40)}),
            ("The orange fruit is orange.", {"type": "color", "name": "Orange", "fill": (255, 140, 40)}),
            ("Purple!", {"type": "color", "name": "Purple", "fill": (160, 80, 220)}),
            ("The grapes are purple.", {"type": "color", "name": "Purple", "fill": (160, 80, 220)}),
            ("Pink!", {"type": "color", "name": "Pink", "fill": (250, 130, 180)}),
            ("The flower is pink.", {"type": "color", "name": "Pink", "fill": (250, 130, 180)}),
            ("Brown!", {"type": "color", "name": "Brown", "fill": (150, 100, 60)}),
            ("The bear is brown.", {"type": "color", "name": "Brown", "fill": (150, 100, 60)}),
        ],
    },
    {
        "id": "shapes_song",
        "title": "Shapes Song for Kids | Learn Circle, Square, Triangle and Star",
        "tags": ["shapes for kids", "shapes song", "learn shapes", "shapes for toddlers",
                 "kids learning video", "preschool learning", "educational video for kids",
                 "circle square triangle", "shapes song for children", "fun shapes"],
        "desc": ("Learn shapes with USA Kids Channel! A fun shapes song for kids: circle, square, "
                 "triangle, star, heart, oval, rectangle and diamond. Watch cheerful shapes dance "
                 "and learn along!"),
        "thumb_words": ["Shapes!", "Circle Square", "Fun"],
        "beats": [
            ("Circle!", {"type": "shape", "name": "Circle", "shape": "circle", "accent": (255, 90, 90)}),
            ("The wheel is a circle.", {"type": "shape", "name": "Circle", "shape": "circle", "accent": (255, 90, 90)}),
            ("Square!", {"type": "shape", "name": "Square", "shape": "square", "accent": (70, 160, 255)}),
            ("The box is a square.", {"type": "shape", "name": "Square", "shape": "square", "accent": (70, 160, 255)}),
            ("Triangle!", {"type": "shape", "name": "Triangle", "shape": "triangle", "accent": (90, 210, 110)}),
            ("The roof is a triangle.", {"type": "shape", "name": "Triangle", "shape": "triangle", "accent": (90, 210, 110)}),
            ("Star!", {"type": "shape", "name": "Star", "shape": "star", "accent": (255, 210, 60)}),
            ("The star in the sky!", {"type": "shape", "name": "Star", "shape": "star", "accent": (255, 210, 60)}),
            ("Heart!", {"type": "shape", "name": "Heart", "shape": "heart", "accent": (250, 110, 150)}),
            ("I love you, from my heart.", {"type": "shape", "name": "Heart", "shape": "heart", "accent": (250, 110, 150)}),
            ("Oval!", {"type": "shape", "name": "Oval", "shape": "oval", "accent": (150, 220, 90)}),
            ("The egg is an oval.", {"type": "shape", "name": "Oval", "shape": "oval", "accent": (150, 220, 90)}),
            ("Rectangle!", {"type": "shape", "name": "Rectangle", "shape": "rect", "accent": (190, 130, 255)}),
            ("The door is a rectangle.", {"type": "shape", "name": "Rectangle", "shape": "rect", "accent": (190, 130, 255)}),
            ("Diamond!", {"type": "shape", "name": "Diamond", "shape": "diamond", "accent": (80, 210, 210)}),
            ("The kite can be a diamond.", {"type": "shape", "name": "Diamond", "shape": "diamond", "accent": (80, 210, 210)}),
        ],
    },
    {
        "id": "abc_phonics_2",
        "title": "ABC Song Part 2 | Learn Letters M to X with Fun Phonics for Kids",
        "tags": ["abc song", "alphabet for kids", "phonics song", "learn letters m to x",
                 "kids learning video", "preschool learning", "toddler learning",
                 "educational video for kids", "abc for toddlers", "letters for children"],
        "desc": ("Continue learning the alphabet with USA Kids Channel! Part 2 of our ABC song "
                 "teaches letters M to X with fun phonics and colorful pictures for toddlers and "
                 "preschoolers!"),
        "thumb_words": ["M to X", "More Letters!", "Fun"],
        "beats": [
            ("M!", {"type": "letter", "char": "M", "word": "Moon", "accent": (255, 170, 60)}),
            ("M is for Moon.", {"type": "letter", "char": "M", "word": "Moon", "accent": (255, 170, 60)}),
            ("N!", {"type": "letter", "char": "N", "word": "Nest", "accent": (110, 190, 255)}),
            ("N is for Nest.", {"type": "letter", "char": "N", "word": "Nest", "accent": (110, 190, 255)}),
            ("O!", {"type": "letter", "char": "O", "word": "Orange", "accent": (255, 140, 50)}),
            ("O is for Orange.", {"type": "letter", "char": "O", "word": "Orange", "accent": (255, 140, 50)}),
            ("P!", {"type": "letter", "char": "P", "word": "Parrot", "accent": (250, 120, 200)}),
            ("P is for Parrot.", {"type": "letter", "char": "P", "word": "Parrot", "accent": (250, 120, 200)}),
            ("Q!", {"type": "letter", "char": "Q", "word": "Queen", "accent": (200, 120, 255)}),
            ("Q is for Queen.", {"type": "letter", "char": "Q", "word": "Queen", "accent": (200, 120, 255)}),
            ("R!", {"type": "letter", "char": "R", "word": "Rain", "accent": (90, 200, 220)}),
            ("R is for Rain.", {"type": "letter", "char": "R", "word": "Rain", "accent": (90, 200, 220)}),
            ("S!", {"type": "letter", "char": "S", "word": "Sun", "accent": (255, 210, 60)}),
            ("S is for Sun.", {"type": "letter", "char": "S", "word": "Sun", "accent": (255, 210, 60)}),
            ("T!", {"type": "letter", "char": "T", "word": "Tree", "accent": (110, 200, 100)}),
            ("T is for Tree.", {"type": "letter", "char": "T", "word": "Tree", "accent": (110, 200, 100)}),
            ("U!", {"type": "letter", "char": "U", "word": "Umbrella", "accent": (255, 110, 120)}),
            ("U is for Umbrella.", {"type": "letter", "char": "U", "word": "Umbrella", "accent": (255, 110, 120)}),
            ("V!", {"type": "letter", "char": "V", "word": "Van", "accent": (120, 160, 255)}),
            ("V is for Van.", {"type": "letter", "char": "V", "word": "Van", "accent": (120, 160, 255)}),
            ("W!", {"type": "letter", "char": "W", "word": "Watch", "accent": (170, 220, 90)}),
            ("W is for Watch.", {"type": "letter", "char": "W", "word": "Watch", "accent": (170, 220, 90)}),
            ("X!", {"type": "letter", "char": "X", "word": "Xylophone", "accent": (255, 160, 200)}),
            ("X is for Xylophone.", {"type": "letter", "char": "X", "word": "Xylophone", "accent": (255, 160, 200)}),
        ],
    },
    {
        "id": "counting_10_20",
        "title": "Counting 10 to 20 for Kids | Numbers Song for Preschoolers",
        "tags": ["counting for kids", "count to 20", "numbers song", "learn numbers 10 to 20",
                 "kids learning video", "preschool math", "toddler counting",
                 "educational video for kids", "numbers for toddlers", "counting song"],
        "desc": ("Learn numbers 10 to 20 with USA Kids Channel! A fun counting song for "
                 "preschoolers. Keep counting after ten: eleven, twelve, thirteen... all the way "
                 "to twenty!"),
        "thumb_words": ["10-20", "Count Up!", "Fun"],
        "beats": [
            ("Eleven!", {"type": "count", "n": 11, "word": "11", "accent": (255, 110, 110)}),
            ("Twelve!", {"type": "count", "n": 12, "word": "12", "accent": (255, 150, 80)}),
            ("Thirteen!", {"type": "count", "n": 13, "word": "13", "accent": (255, 200, 70)}),
            ("Fourteen!", {"type": "count", "n": 14, "word": "14", "accent": (190, 220, 80)}),
            ("Fifteen!", {"type": "count", "n": 15, "word": "15", "accent": (110, 210, 120)}),
            ("Sixteen!", {"type": "count", "n": 16, "word": "16", "accent": (90, 210, 200)}),
            ("Seventeen!", {"type": "count", "n": 17, "word": "17", "accent": (90, 180, 240)}),
            ("Eighteen!", {"type": "count", "n": 18, "word": "18", "accent": (140, 150, 255)}),
            ("Nineteen!", {"type": "count", "n": 19, "word": "19", "accent": (190, 130, 250)}),
            ("Twenty!", {"type": "count", "n": 20, "word": "20", "accent": (255, 140, 200)}),
            ("You counted all the way to twenty. Amazing!", {"type": "count", "n": 20, "word": "10 11 12 ... 20", "accent": (255, 200, 60)}),
        ],
    },
]

INTRO_BEATS = [
    ("Welcome to USA Kids Channel!", {"type": "banner", "word": "USA KIDS", "accent": (255, 190, 60)}),
    ("Let us learn and have fun!", {"type": "banner", "word": "LET'S LEARN!", "accent": (255, 90, 120)}),
]
OUTRO_BEATS = [
    ("Great job today! You learned something new.", {"type": "banner", "word": "GREAT JOB!", "accent": (110, 210, 120)}),
    ("Subscribe for more fun learning!", {"type": "banner", "word": "SUBSCRIBE!", "accent": (255, 90, 90)}),
]
