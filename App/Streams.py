class Stream:
    #name of stream
    Name = ""
    #format for Team data used in the Overlay
    Team = [['','','Team 1',''],['','','Team 2','']]
    #format for Schedule data used in the Schedule Overlay
    Schedule = [['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','',''],['','','','','','','']]
    #format for Players data used in the Stats Overlay
    Stats = [['Player 1','',''],['Player 2','','']]
    #format for Caster data used in the 2 Caster Overlay
    CasterGroup1 = [['Caster 1','',''],['Caster 2','','']]
    #format for Caster data used in the 3 Caster Overlay
    CasterGroup2 = [['Caster 1','',''],['Caster 2','',''],['Caster 3','','']]
    #format for matches in the matches tab
    matches = []
    #formate for widget Open/Close status
    Widgets = {"StreamStats":True,
               "Casters":False,
               "PlayerStats":False,
               "Overlay":False,
               "Schedule":False}

    def __init__(self, Name):
        self.Name = Name

class Headings:
    #headings used for the Match page
    MatchHeadings = ("Team 1", "Team 2", "Time","Format","Winner","Loser","Actions")

    #headings used for the Caster page
    CasterHeadings = ("#", "Name", "SubHeading", "Actions")

    #headings used for the Music page
    MusicHeadings = ("#", "Title", "Author","Music", "Actions")

    #headings used for the Team page
    TeamHeadings = ("#", "Name", "Abbreviation","Logo TXT","Logo BL","Logo BR","Logo TOP", "Actions")

    #headings used for the Players page
    PlayerHeadings = ("Name", "Team", "Actions")