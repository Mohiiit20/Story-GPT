from model import generate_story

text='''The India–Pakistan cricket rivalry is one of the most intense sports rivalries in the world.[1][2] Showdowns between the teams are considered some of the biggest matches in the world, and are among the most-viewed sport games.

India has won 11 ICC tournaments compared to Pakistan's 5. At senior level, India has won 6 ICC trophies (2 Cricket World Cup, 2 T20 World Cup, 2 Champions Trophy), while Pakistan has won 3 (1 Cricket World Cup, 1 T20 World Cup, and 1 Champions Trophy). India has overwhelmingly dominated Pakistan in ICC World Cups, winning 14 out of 15 matches, with Pakistan securing only one victory. India also leads 8-0 against Pakistan at the 50-over ODI World Cups.[3]

The tense relations between the two nations, resulting from bitter diplomatic relationships and conflict that originated during the Partition of British India into India and Pakistan in 1947, the Indo-Pakistani Wars, and the Kashmir conflict, laid the foundations for the emergence of a fierce sporting rivalry between the two nations who had shared a common cricketing heritage.[4]

The two sides first played in 1952, when Pakistan toured India. Tests and, later, limited overs series have been played ever since, although a number of planned tours by both sides have been cancelled or aborted due to political factors. No cricket was played between the two countries between 1962 and 1977 due to two major wars in 1965 and 1971, and the 1999 Kargil War and the 2008 Mumbai terrorist attacks have also interrupted cricketing ties between the two nations.[5][6]

The growth of large expatriate populations from both countries across the world led to neutral venues, including the United Arab Emirates and Canada, hosting bilateral and multilateral One Day International (ODI) series involving the two teams and the teams have met during International Cricket Council (ICC) competitions. Tickets for matches in which the two teams play each other at international competitions are in high demand, with over 800,000 applications for tickets made for the 2019 Cricket World Cup meeting between the two sides;[5][6] the television transmission of the match was watched by 273 million viewers.[7]

Players from both teams routinely face extreme pressure to win and are threatened by extreme reactions in defeat. Extreme fan reactions to defeats in key matches have been recorded, with a limited degree of hooliganism.[5] At the same time, India–Pakistan matches have also offered opportunities for cricket diplomacy as a means to improve relations between the two countries by allowing heads of state to exchange visits and cricket followers from either country to travel to the other to watch the matches.[6]'''

story=generate_story(text)

print(story['story'])
