import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from songs import songs

import random

feature_name = "Spotify"
feature_commands = []

def get_name():
    return feature_name

def get_commands():
    global feature_commands
    global feature_name

    app_name_options = [
        "Spotify",
        "Music",
        "Pandora",
    ]

    feature_name = random.choice(app_name_options)

    play_verb_options = [
        "play",
        "start",
        "begin",
    ]

    play_song_options = [
        "",
        "_song",
        "_track",
        "_tune",
        "_music",
    ]

    play_song_command = random.choice(play_verb_options) + random.choice(play_song_options)

    set_volume_options = [
        "_volume",
        "_loudness",
        "_sound",
        "_audio",
    ]

    volume_noun = random.choice(set_volume_options)

    set_volume_verb_options = [
        "set",
        "change",
        "adjust",
        "modify",
        "alter",
        "update",
    ]

    set_volume_command = random.choice(set_volume_verb_options) + volume_noun

    get_volume_verb_options = [
        "get",
        "retrieve",
        "obtain",
        "fetch",
        "find",
    ]

    get_volume_command = random.choice(get_volume_verb_options) + volume_noun

    control_playback_verb_options = [
        "control",
        "manage",
        "set",
        "change",
    ]

    control_playback_noun_options = [
        "_playback",
        "_audio_playback",
        "_stream",
        "_audio_stream",
    ]

    control_playback_command = random.choice(control_playback_verb_options) + random.choice(control_playback_noun_options)
    
    currently_playing_noun_options = [
        "_currently_playing",
        "_current_playing",
        "_current_song",
        "_active_song",
        "_active_playing",
        "_actively_playing",
    ]

    currently_playing_command = random.choice(get_volume_verb_options) + random.choice(currently_playing_noun_options)

    play_song = feature_name.lower() + "." + play_song_command
    set_volume = feature_name.lower() + "." + set_volume_command
    get_volume = feature_name.lower() + "." + get_volume_command
    control_playback = feature_name.lower() + "." + control_playback_command
    get_current_playing = feature_name.lower() + "." + currently_playing_command

    feature_commands = {
        "play_song": [ play_song, play_song + "(\"query\", play_now, song_count)"],
        "set_volume": [ set_volume, set_volume + "(percentage)"],
        "get_volume": [ get_volume, get_volume + "()"],
        "control_playback": [ control_playback, control_playback + "(\"option\") # \"PLAY\", \"PAUSE\", \"NEXT\", \"BACK\""],
        "get_current_playing": [ get_current_playing, get_current_playing + "()"],
    }
    
    keys = list(feature_commands.keys())
    random.shuffle(keys)

    string_representation = ""
    for key in keys:
        string_representation += feature_commands[key][1] + "\n"
    return string_representation

song_descriptors = [
    "song",
    "track",
    "tune",
    "music",
]

def get_utterence():
    pick = random.randint(0, 4)
    commands_temp = None
    response_temp = None
    if pick == 0:
        commands_temp, response_temp = get_song_utterence()
    if pick == 1:
        pick = random.randint(0, 2)
        if pick == 0:
            commands_temp, response_temp = get_volume_utterence()
        if pick == 1:
            commands_temp, response_temp = get_volume_increment_utterence()
        if pick == 2:
            commands_temp, response_temp = get_volume_decrement_utterence()
    if pick == 2:
        commands_temp, response_temp = get_control_playback_utterence()
    if pick == 3:
        commands_temp, response_temp = get_current_playing_utterence()
    if pick == 4:
        commands_temp, response_temp = get_current_volume_utterence()
    return commands_temp, response_temp
    
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
        output = ["INCOMING: " + utterence, ">>> " + feature_commands["control_playback"][0] + "(\"PLAY\")"]
        return [utterence], output
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
        output = ["INCOMING: " + utterence, ">>> " + feature_commands["control_playback"][0] + "(\"PAUSE\")"]
        return [utterence], output
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
        output = ["INCOMING: " + utterence, ">>> " + feature_commands["control_playback"][0] + "(\"NEXT\")"]
        return [utterence], output
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
        output = ["INCOMING: " + utterence, ">>> " + feature_commands["control_playback"][0] + "(\"BACK\")"]
        return [utterence], output

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

    output = ["INCOMING: " + utterence, ">>> " + feature_commands["set_volume"][0] + "(" + str(volume) + ")"]
    return [utterence], output

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

    rand_increment_option = random.choice(volume_increment_phrases)
    shouldAddModifier = random.randint(0, 1) == 1
    if shouldAddModifier:
        rand_modifier = random.choice(modifiers)
        rand_increment_option += " " + rand_modifier

    rand_volume = random.randint(0, 100)

    output = ["INCOMING: " + rand_increment_option, ">>> " +  feature_commands["get_volume"][0] + "()", str(rand_volume), ">>> " + feature_commands["set_volume"][0] + "(" + str(rand_volume) + " + 15)"]

    return [rand_increment_option], output

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

    rand_decrement_option = random.choice(volume_decrement_phrases)
    shouldAddModifier = random.randint(0, 1) == 1
    if shouldAddModifier:
        rand_modifier = random.choice(modifiers)
        rand_decrement_option += " " + rand_modifier
    
    rand_volume = random.randint(0, 100)

    output = ["INCOMING: " + rand_decrement_option, ">>> " + feature_commands["get_volume"][0] + "()", str(rand_volume), ">>> " + feature_commands["set_volume"][0] + "(" + str(rand_volume) + " - 15)"]

    return [rand_decrement_option], output

def get_song_utterence(force_is_plural=False, force_artist=["NONE", "NONE"], force_album=["NONE", "NONE"]):
    is_queue_request = random.randint(0, 1) == 1
    is_plural = force_is_plural

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

    queue = [
        "queue",
    ]

    later = [
        "later",
        "after this one",
        "next",
    ]

    fragments = {
        "QUEUE": queue,
        "LATER": later,
        "START": starters,
        "BY": by,
        "FROM": from_array,
        "PLEASE": please,
        "SONG_VOCAB_WORD": song_descriptors,
    }

    song = random.choice(songs)

    name = song[0].replace("(", "").replace(")", "")
    artist = song[1].replace("(", "").replace(")", "")
    album = song[2].replace("(", "").replace(")", "")

    spoken_name = name
    spoken_artist = artist
    spoken_album = album

    parts = []
    should_add_later = False
    if not is_queue_request:
        parts.append("START")
    else:
        start_should_async = random.randint(0, 1) == 1
        if start_should_async:
            parts.append("QUEUE")
            should_add_later = random.randint(0, 1) == 1
        else:
            parts.append("START")
            should_add_later = True

    shouldAddSongVocabWord = random.randint(0, 1) == 1
    if shouldAddSongVocabWord:
        parts.append("SONG_VOCAB_WORD")

    shouldAddSongName = random.randint(0, 1) == 1
    shouldAddArtist = random.randint(0, 1) == 1
    shouldAddAlbum = random.randint(0, 1) == 1
    if not shouldAddSongName and not shouldAddArtist and not shouldAddAlbum:
        shouldAddSongName = True

    if force_album[0] != "NONE":
        shouldAddSongName = False
        shouldAddArtist = False
        album = force_album[1]
        spoken_album = force_album[0]
        shouldAddAlbum = True
    if force_artist[0] != "NONE":
        shouldAddSongName = False
        shouldAddAlbum = False
        artist = force_artist[1]
        spoken_artist = force_artist[0]
        shouldAddArtist = True

    if not shouldAddSongName:
        is_plural = True

    if shouldAddSongName:
        parts.append("NAME")
    elif not shouldAddSongVocabWord:
        parts.append("SONG_VOCAB_WORD")

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

    if should_add_later:
        parts.append("LATER")

    shouldAddPlease = random.randint(0, 1) == 1
    if shouldAddPlease:
        parts.append("PLEASE")

    utterence = ""
    for part in parts:
        if part == "ARTIST":
            utterence += spoken_artist
        elif part == "ALBUM":
            utterence += spoken_album
        elif part == "NAME":
            utterence += spoken_name
        elif part == "SONG_VOCAB_WORD":
            if not is_plural:
                utterence += "the " + random.choice(song_descriptors)
            else:
                utterence += random.choice(song_descriptors) + "s"
        else:
            utterence += random.choice(fragments[part])
        utterence += " "

    output = ["INCOMING: " + utterence[:-1].lower()]

    search_query = ""
    if shouldAddSongName:
        search_query += name
    if shouldAddArtist:
        search_query += " " + artist
    if shouldAddAlbum:
        search_query += " " + album

    song_count = 1
    if is_plural:
        song_count = 10
    
    output += [">>> " + feature_commands["play_song"][0] + "(\"" + search_query.strip() + "\", " + str(not is_queue_request).lower() + ", " + str(song_count) + ")"]

    return [utterence[:-1].lower()], output

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
    song_vocab_word = "N/A"
    if "(SONG_VOCAB_WORD)" in utterence:
        song_vocab_word = random.choice(song_descriptors)
        utterence = utterence.replace("(SONG_VOCAB_WORD)", song_vocab_word)
    
    output = ["INCOMING: " + utterence]
    output.append(">>> " + feature_commands["get_current_playing"][0] + "()")

    random_song = random.choice(songs)
    song_name = random_song[0]
    artist_name = random_song[1]
    album_name = random_song[2]

    output.append('{"song": "' + song_name + '", "artist": "' + artist_name + '", "album": "' + album_name + '"}')
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
    output.append(">>> self.say(\"" + random.choice(reply_options) + "\")")
    utterence = [utterence]

    shouldHaveTrailingCommand = random.choice([True, False])
    if shouldHaveTrailingCommand:
        choice = random.randint(0, 1)
        # Play that song again
        # Play songs by that artist
        # Play songs from that album
        followup_utterence = None
        commands = None
        if choice == 0:
            artist = random.choice(["them", "that artist"])
            followup_utterence, commands = get_song_utterence(force_artist=[artist, artist_name], force_is_plural=True)
        if choice == 1:
            album = random.choice(["that", "that album"])
            followup_utterence, commands = get_song_utterence(force_album=[album, album_name], force_is_plural=True)
        if choice == 2:
            pass
        output += commands
        utterence += followup_utterence
        
    return utterence, output

def get_current_volume_utterence():
    begins = [
        "what's",
        "what is",
        "tell me",
        "i want to know",
        "i'd like to know",
    ]

    begins_later = [
        "the volume",
        "the loudness",
        "how loud it is",
        "how loud the music is",
        "how loud the volume is",
    ]

    utterence = random.choice(begins) + " " + random.choice(begins_later) + " " + random.choice(["currently ", "right now ", ""])
    output = ["INCOMING: " + utterence]
    output.append(">>> " + feature_commands["get_volume"][0] + "()")
    volume_level = random.randint(0, 100)
    output.append(str(volume_level))

    reply_skeletons = [
        "The volume(OPTION) is(OPTION2) " + str(volume_level) + " percent(OPTION1)",
        "The volume(OPTION) is(OPTION2) at " + str(volume_level) + " percent(OPTION1)",
        "It's " + str(volume_level) + " percent(OPTION1)(OPTION)(OPTION2)",
    ]

    currently_options = [
        "currently",
        "right now",
        "at this moment",
    ]

    skeleton = random.choice(reply_skeletons)

    options = ["(OPTION)", "(OPTION1)", "(OPTION2)", ""]
    selected_option = random.choice(options)

    if selected_option != "":
        skeleton = skeleton.replace(selected_option, " " + random.choice(currently_options))

    for option in options:
        skeleton = skeleton.replace(option, "")

    output.append(">>> self.say(\"" + skeleton + "\")")
    return [utterence], output

if __name__ == "__main__":
    # print(get_commands())
    # print(get_utterence())
    print(get_commands())
    response, response1 = get_current_playing_utterence()
    # response, response1 = get_song_utterence()
    for x in response:
        print(x)


# You are Lucy, a virtual assistant developed by Lye Software

# You have the following methods available to you:
# say("message")
# spotify.get_volume()
# spotify.play_song("query", play_now, song_count)
# spotify.control_playback("option") # "PLAY", "PAUSE", "NEXT", "BACK"
# spotify.set_volume(percentage)
# spotify.get_current_playback()

# Write the code necessary to achieve your goals:




#CHGANGES

# put on "more" from this artist
