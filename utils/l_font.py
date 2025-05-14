font_list = [
    "1943", "3-d", "3d_diagonal", "3x5", "4max",
    "4x4_offr", "5lineoblique", "5x7", "64f1",
    "6x10", "6x9", "a_zooloo", "alligator", "alligator2",
    "alligator3", "alphabet", "amc3line", "amcun1", "aquaplan",
    "arrows", "asc", "ascii", "assalt_m", "asslt_m",
    "banner", "banner3", "banner3-d", "banner4", "barbwire",
    "basic", "beer_pub", "bell", "big", "bigchief",
    "block", "bolger", "braced", "bright", "bubble",
    "c1", "c2", "c_ascii", "cards", "catwalk",
    "char1", "char2", "char3", "char4", "charact1",
    "charact2", "charact3", "charact4", "charact5", "charact6",
    "characte", "chartr", "chartri", "chunky", "clb6x10",
    "clb8x10", "clb8x8", "cli8x8", "clr4x6", "clr5x10",
    "clr5x6", "clr5x8", "clr6x10", "clr6x6", "clr6x8",
    "clr7x8", "clr8x10", "clr8x8", "coinstak", "colossal",
    "com_sen", "computer", "contessa", "contrast", "cricket",
    "cygnet", "digital", "doh", "doom", "dotmatrix",
    "drpepper", "druid", "e_fist", "ebbs_1", "ebbs_2",
    "eca", "eftifont", "eftitalic", "epic", "faces_of",
    "fairligh", "fantasy1", "fbr1", "fbr12", "fbr2",
    "fbr_stri", "fbr_tilt", "finalass", "fireing", "fourtops",
    "fp1", "fp2", "funky_dr", "future_1", "future_2",
    "future_3", "future_4", "future_5", "future_6", "future_7",
    "future_8", "fuzzy", "georgi16", "georgia11", "ghost",
    "ghost_bo", "ghoulish", "glenyn", "goofy", "gothic",
    "green_be", "heartleft", "heartright", "henry3d", "hollywood",
    "home_pak", "hyper", "impossible", "inc_raw", "jacky",
    "jazmine", "keyboard", "kik_star", "larry3d", "lcd",
    "lean", "letters", "marquee", "maxfour", "merlin1",
    "modular", "moscow", "nancyj", "nancyj-underlined", "nipples",
    "nscript", "o8", "ogre", "oldbanner", "os2",
    "pawp", "peaks", "pebbles", "poison", "puffy",
    "puzzle", "pyramid", "red_phoenix", "rev", "roman",
    "rounded", "rozzo", "santaclara", "sblood", "script",
    "shimrod", "slant", "slide", "slscript", "small",
    "smkeyboard", "smpoison", "smslant", "soft", "standard",
    "starwars", "stellar", "stforek", "stop", "straight",
    "swampland", "swan", "sweet", "tanja", "thick",
    "thin", "threepoint", "tiles", "tinker-toy", "tombstone",
    "tubular", "type_set", "ucf_fan", "unarmed", "usa",
    "usa_pq", "usaflag", "utopia", "utopiab", "utopiabi",
    "utopiai", "varsity", "vortron", "war_of_w", "xbrite",
    "xbriteb", "xbritebi", "xbritei", "xchartr", "xchartri",
    "xcour", "xcourb", "xcourbi", "xcouri", "xhelv",
    "xhelvb", "xhelvbi", "xhelvi", "xsans", "xsansb",
    "xsansbi", "xsansi", "xtimes", "xtty", "xttyb",
    "yie-ar", "yie_ar_k", "zig_zag", "zone7"
]

font_in_reg_dataset = [
    'thin', 'maxfour', 'arrows', 'catwalk', 'alphabet', 
    'varsity', 'banner3-d', '4x4_offr', 'barbwire', 'basic'
]

font_class = {
    'Symbol_with_specific_letter': [  ## 只會出現相同
        'bubble', 'cards', 'digital', 'heartleft', 'heartright', 
        'keyboard', 'puzzle', 'pyramid', 'smkeyboard'
    ],
    'hybrid': [  
        'basic', 'bolger', 'colossal', 'computer', 
        'georgi16', 'georgia11', 'henry3d', 'jazmine', 'nancyj', 
        'nancyj-underlined', 'nscript', 'o8', 'pebbles', 'roman', 
        'rozzo' , 'thick', '4max'
    ],
    'letter': [   # same-letter-outline
        'alphabet', 'doh', 'letters', 'tanja'
    ],
    'multi-symbol': [ # cricket eftifont ghost larry3d soft  tinker-toy
        '3d_diagonal', '5lineoblique', 'alligator', 'alligator2', 
        'alligator3', 'amc3line', 'amcun1', 'bell', 'big', 'bigchief', 
        'block', 'braced', 'chunky', 'contessa', 'cricket', 'cygnet', 
        'doom', 'drpepper', 'eftifont', 'epic', 'fourtops', 'fuzzy', 
        'ghost', 'ghoulish', 'glenyn', 'goofy', 'gothic', 'hollywood', 
        'impossible', 'jacky', 'larry3d', 'lcd', 'maxfour', 'merlin1', 
        'modular', 'ogre', 'pawp', 'poison', 'puffy', 'red_phoenix', 
        'rounded', 'santaclara', 'sblood', 'script', 'shimrod', 'slant', 
        'slscript', 'small', 'smpoison', 'smslant', 'soft', 'standard', 
        'starwars', 'stforek', 'stop', 'straight', 'swampland', 'swan', 
        'sweet', 'thin', 'threepoint', 'tinker-toy', 'tombstone', 
        'usaflag', 'varsity', 'slide', 'eftitalic', 
    ],
    'single-symbol': [# os2, rev  #　bright banner4 banner3-d
        '1943', '3x5','4x4_offr', '5x7', '64f1', '6x10', 
        '6x9', 'a_zooloo', 'aquaplan', 'asc', 'ascii', 'assalt_m', 
        'asslt_m', 'banner', 'banner3', 'banner3-d', 'banner4', 'beer_pub', 
        'bright', 'c1', 'c2', 'c_ascii', 'char1', 'char2', 'char3', 'char4', 
        'charact1', 'charact2', 'charact3', 'charact4', 'charact5', 
        'charact6', 'characte', 'chartr', 'chartri', 'clb6x10', 'clb8x10', 
        'clb8x8', 'cli8x8', 'clr4x6', 'clr5x10', 'clr5x6', 'clr5x8', 
        'clr6x10', 'clr6x6', 'clr6x8', 'clr7x8', 'clr8x10', 'clr8x8', 
        'com_sen', 'contrast', 'druid', 'e_fist', 'ebbs_1', 'ebbs_2', 'eca', 
        'faces_of', 'fairligh', 'fantasy1', 'fbr1', 'fbr12', 'fbr2', 
        'fbr_stri', 'fbr_tilt', 'finalass', 'fireing', 'fp1', 'fp2', 
        'funky_dr', 'future_1', 'future_2', 'future_3', 'future_4', 
        'future_5', 'future_6', 'future_7', 'future_8', 'ghost_bo', 
        'green_be', 'home_pak', 'hyper', 'inc_raw', 'kik_star', 'moscow', 
        'oldbanner', 'os2', 'rev', 'type_set', 'ucf_fan', 'unarmed', 'usa', 
        'usa_pq', 'utopia', 'utopiab', 'utopiabi', 'utopiai', 'vortron', 
        'war_of_w', 'xbrite', 'xbriteb', 'xbritebi', 'xbritei', 'xchartr', 
        'xchartri', 'xcour', 'xcourb', 'xcourbi', 'xcouri', 'xhelv', 
        'xhelvb', 'xhelvbi', 'xhelvi', 'xsans', 'xsansb', 'xsansbi', 
        'xsansi', 'xtimes', 'xtty', 'xttyb', 'yie-ar', 'yie_ar_k', 
        'zig_zag', 'zone7'
    ],
    'single-combined-symbol': [
        'arrows', 'barbwire', 'catwalk', 'coinstak', 'dotmatrix', 'lean', 
        'marquee', 'nipples', 'peaks', 'stellar', 'tiles', 'tubular','3-d'
    ]
}

font_for_dataset = [
    'cards', 'digital', 'keyboard',  # Symbol_with_specific_letter
    'henry3d', 'basic', 'georgia11', # hybrid
    'doh', 'letters', 'tanja',       # letter
    'maxfour', 'varsity', 'thin', 'slide',   # multi-symbol
    'banner3-d', '4x4_offr', 'rev', 'os2',  # single-symbol
    'arrows', 'catwalk', 'barbwire', # single-combined-symbol
]

font_class_for_dataset =[
    'SSL', 'SSL', 'SSL',
    'hybrid', 'hybrid', 'hybrid',
    'letter', 'letter', 'letter',
    'MS', 'MS', 'MS', 'MS', 
    'SS', 'SS', 'SS', 'SS',
    'SCS', 'SCS', 'SCS'
]


font_class_reg = {
    'Symbol_with_specific_letter': [  ## 只會出現相同
        'cards', 'digital', 'keyboard',
    ],
    'hybrid': [  
        'henry3d', 'basic', 'georgia11',
    ],
    'letter': [   # same-letter-outline
        'doh', 'letters', 'tanja',
    ],
    'multi-symbol': [ 
        'maxfour', 'varsity', 'thin', 'slide',
    ],
    'single-symbol': [# os2, rev  #　bright banner4 banner3-d
        'banner3-d', '4x4_offr', 'rev', 'os2'
    ],
    'single-combined-symbol': [
        'arrows', 'catwalk', 'barbwire'
    ]
}