import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from songs import songs

import random

def get_name():
    return "Spotify"

def get_commands():
    return """
spotify.play_song("query")
spotify.set_volume(percentage)
spotify.get_volume()
spotify.control_playback("option") # "PLAY", "PAUSE", "NEXT", "BACK"
spotify.get_current_playing()
"""

song_descriptors = [
    "song",
    "track",
    "tune",
    "music",
]

def get_utterence():
    pick = random.randint(0, 3)
    if pick == 0:
        return get_song_utterence()
    if pick == 1:
        pick = random.randint(0, 2)
        if pick == 0:
            return get_volume_utterence()
        if pick == 1:
            return get_volume_increment_utterence()
        if pick == 2:
            return get_volume_decrement_utterence()
    if pick == 2:
        return get_control_playback_utterence()
    if pick == 3:
        return get_current_playing_utterence()
    
def get_control_playback_utterence():
    option = random.randint(0, 3)
    if option == 0:
        # PLAY
        play = [
            "play",
            "resume",
            "continue",
        ]

        utterence = ""
        
        shouldAddModifier = random.randint(0, 1) == 1
        if shouldAddModifier:
            utterence = random.choice(play) + " the " + random.choice(song_descriptors)
        else:
            utterence = random.choice(play)
        output = "spotify.control_playback(\"PLAY\")"
        return utterence, [output]
    elif option == 1:
        # PAUSE
        pause = [
            "pause",
            "stop",
            "halt",
            "cease",
            "end",
            "finish",
        ]

        utterence = ""

        shouldAddModifier = random.randint(0, 1) == 1
        if shouldAddModifier:
            utterence = random.choice(pause) + " the " + random.choice(song_descriptors)
        else:
            utterence = random.choice(pause)
        output = "spotify.control_playback(\"PAUSE\")"
        return utterence, [output]
    elif option == 2:
        forward = [
            ["go", True],
            ["go forward", False],
            ["skip", False]
        ]

        forward_modifiers = [
            "to the next (SONG_VOCAB_WORD)",
        ]

        forward_modifiers_modifiers = [
            "in the queue",
            "in the playlist",
            "after this one",
            "after"
        ]
    
        forward = random.choice(forward)
        needsForwardModifier = random.randint(0, 1) == 1 or forward[1]
        needsForwardModifierModifier = random.randint(0, 1) == 1
        utterence = forward[0]
        if needsForwardModifier:
            utterence += " " + random.choice(forward_modifiers).replace("(SONG_VOCAB_WORD)", random.choice(song_descriptors))
        if needsForwardModifierModifier:
            utterence += " " + random.choice(forward_modifiers_modifiers)
        output = "spotify.control_playback(\"NEXT\")"
        return utterence, [output]
    elif option == 3:
        # BACK
        back = [
            ["go", True],
            ["go back", False],
            ["go backward", False]
        ]

        back_modifiers = [
            "to the previous (SONG_VOCAB_WORD)",
        ]

        back_modifiers_modifiers = [
            "in the queue",
            "in the playlist",
            "before this one",
            "before"
        ]

        back = random.choice(back)
        needsBackModifier = random.randint(0, 1) == 1 or back[1]
        needsBackModifierModifier = random.randint(0, 1) == 1
        utterence = back[0]
        if needsBackModifier:
            utterence += " " + random.choice(back_modifiers).replace("(SONG_VOCAB_WORD)", random.choice(song_descriptors))
        if needsBackModifierModifier:
            utterence += " " + random.choice(back_modifiers_modifiers)
        output = "spotify.control_playback(\"BACK\")"
        return utterence, [output]

def get_volume_utterence():
    volume = random.randint(0, 100)

    volume_options = [
        "adjust the volume to",
        "change the volume to",
        "make the volume",
        "set volume level to",
        "modify volume to",
        "alter the volume to",
        "set the sound level to",
        "raise the volume to",
        "lower the volume to",
        "set the audio level to"
    ]

    rand_volume_option = random.choice(volume_options)

    utterence = rand_volume_option + " " + str(volume) + "%"    

    output = "spotify.set_volume(" + str(volume) + ")"
    return utterence, [output]

def get_volume_increment_utterence():
    volume_increment_phrases = [
        "Turn it up",
        "Raise the volume",
        "Increase the volume",
        "Make it louder",
        "Turn up the volume",
        "Turn the volume up",
    ]

    modifiers = [
        "a little",
        "a bit",
        "a tad",
        "a smidge",
        "a lot"
    ]

    utterence = ""
    rand_increment_option = random.choice(volume_increment_phrases)
    shouldAddModifier = random.randint(0, 1) == 1
    if shouldAddModifier:
        rand_modifier = random.choice(modifiers)
        rand_increment_option += " " + rand_modifier

    rand_volume = random.randint(0, 100)

    return rand_increment_option, ["spotify.get_volume()", str(rand_volume), "spotify.set_volume(" + str(rand_volume) + " + 15)"]

def get_volume_decrement_utterence():
    volume_decrement_phrases = [
        "Turn it down",
        "Lower the volume",
        "Decrease the volume",
        "Make it quieter",
        "Turn down the volume",
        "Turn the volume down",
    ]

    modifiers = [
        "a little",
        "a bit",
        "a tad",
        "a smidge",
        "a lot"
    ]

    utterence = ""
    rand_decrement_option = random.choice(volume_decrement_phrases)
    shouldAddModifier = random.randint(0, 1) == 1
    if shouldAddModifier:
        rand_modifier = random.choice(modifiers)
        rand_decrement_option += " " + rand_modifier
    
    rand_volume = random.randint(0, 100)

    return rand_decrement_option, ["spotify.get_volume()", str(rand_volume), "spotify.set_volume(" + str(rand_volume) + " - 15)"]

def get_song_utterence():
    starters = [
        "play",
        "put on",
        "start",
    ]

    by = [
        "by",
        "written by",
        "created by"
    ]

    from_array = [
        "from",
    ]

    please = [
        "please",
    ]

    fragments = {
        "START": starters,
        "BY": by,
        "FROM": from_array,
        "PLEASE": please,
        "SONG_VOCAB_WORD": song_descriptors,
    }

    song = random.choice(songs)

    name = song[0].replace("(", "").replace(")", "")
    aritst = song[1].replace("(", "").replace(")", "")
    album = song[2].replace("(", "").replace(")", "")

    parts = []

    # shouldAddStarter = random.randint(0, 1) == 1
    shouldAddStarter = True
    if shouldAddStarter:
        parts.append("START")
        shouldAddSongVocabWord = random.randint(0, 1) == 1
        if shouldAddSongVocabWord:
            parts.append("SONG_VOCAB_WORD")


    shouldAddSongName = random.randint(0, 1) == 1
    shouldAddArtist = random.randint(0, 1) == 1
    shouldAddAlbum = random.randint(0, 1) == 1
    if not shouldAddSongName and not shouldAddArtist and not shouldAddAlbum:
        shouldAddSongName = True

    if shouldAddSongName:
        parts.append("NAME")

    if shouldAddArtist and shouldAddAlbum:
        shouldFlipArtistAndAlbumName = random.randint(0, 1) == 1
        if shouldFlipArtistAndAlbumName:
            parts.append("BY")
            parts.append("ARTIST")
            parts.append("FROM")
            parts.append("ALBUM")
        else:
            parts.append("FROM")
            parts.append("ALBUM")
            parts.append("BY")
            parts.append("ARTIST")
    elif shouldAddArtist:
        parts.append("BY")
        parts.append("ARTIST")
    elif shouldAddAlbum:
        parts.append("FROM")
        parts.append("ALBUM")

    shouldAddPlease = random.randint(0, 1) == 1
    if shouldAddPlease:
        parts.append("PLEASE")

    utterence = ""
    for part in parts:
        if part == "ARTIST":
            utterence += aritst
        elif part == "ALBUM":
            utterence += album
        elif part == "NAME":
            utterence += name
        elif part == "SONG_VOCAB_WORD":
            utterence += "the " + random.choice(song_descriptors)
        else:
            utterence += random.choice(fragments[part])
        utterence += " "

    output = ""

    search_query = ""
    if shouldAddSongName:
        search_query += name
    if shouldAddArtist:
        search_query += " " + aritst
    if shouldAddAlbum:
        search_query += " " + album
    
    output += "spotify.play_song(\"" + search_query.strip() + "\")"
    return utterence[:-1].lower(), [output]

def get_current_playing_utterence():
    verb = [
        "playing",
        "on",
        "currently playing",
        "currently on",
    ]

    options = [
        "what's (VERB)",
        f"what (SONG_VOCAB_WORD) is (VERB)",
    ]

    utterence = random.choice(options)
    utterence = utterence.replace("(VERB)", random.choice(verb))
    utterence = utterence.replace("(SONG_VOCAB_WORD)", random.choice(song_descriptors))
    
    output = ["spotify.get_current_playing()"]

    random_song = random.choice(songs)
    song_name = random_song[0]
    artist_name = random_song[1]
    album_name = random_song[2]

    output.append(song_name + " by " + artist_name + " from " + album_name)
    reply_options = [
        "Currently playing is " + song_name + " by " + artist_name,
        "Right now I'm playing " + song_name + " by " + artist_name,
        "We're listening to " + song_name + " by " + artist_name,
        "I'm playing " + song_name + " by " + artist_name,
        "The current track is " + song_name + " by " + artist_name,
        "This is " + song_name + " by " + artist_name,
        "The song that's currently on is " + song_name + " by " + artist_name,
        "Playing now is " + song_name + " by " + artist_name,
    ]
    output.append("self.say(\"" + random.choice(reply_options) + "\")")
    return utterence, output


if __name__ == "__main__":
    ques, ans = get_current_playing_utterence()
    print("QUESTION: " + ques + "\n")
    for x in ans:
        print("ANSWER: " + x + "\n")