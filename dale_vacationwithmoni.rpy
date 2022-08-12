# Register the submod
init -990 python in mas_submod_utils:
    Submod(
        author="DaleRuneMTS",
        name="Vacation with Moni",
        description="A spinoff of Out and About, focusing more on vacations with Monika! Let her know you're taking her on holiday, and enjoy some exclusive fun in the sun with her!",
        version="1.0",
        dependencies={},
        settings_pane=None,
        version_updates={
        }
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Vacation with Moni",
            user_name="DaleRuneMTS",
            repository_name="dale_vacation_with_moni",
            submod_dir="/Submods",
            extraction_depth=2
        )

init 5 python in mas_bookmarks_derand:
    # Ensure things get bookmarked and derandomed as usual.
    label_prefix_map["vam_"] = label_prefix_map["monika_"]

default -5 persistent._moni_on_vacation = False
default -5 vam_absence_counter = False
default -5 persistent._vacay_details = set()
default -5 persistent._vam_preparations_needed = True

init -6 python in mas_greetings:

    TYPE_ENROUTE_TO_VACAY = "enroute_to_vacay"
    TYPE_HOME_FROM_VACAY = "home_from_vacay"

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="vam_bye_prompt_vacation",
            unlocked=True,
            prompt="I'm going on vacation.",
            pool=True
        ),
        code="BYE",
        markSeen=True
    )

label vam_bye_prompt_vacation:
    if not mas_getEVL_shown_count("vam_bye_prompt_vacation"):
        m 1wuo "Oh!"
        m 1wud "Are you really?"
        m 1eub "That sounds pretty cool, [player]."
        m "I hope you end up going somewhere fun."
        show monika 1ruc at t11
        pause 1.5
        m ".{w=0.2}.{w=0.2}.{w=0.2}{nw}"
        extend 3eud "Hey, um..."
        m 6gub "So if I'm jumping the gun a little bit on this, let me know, but--{nw}"
        $ _history_list.pop()
        menu:
            m "So if I'm jumping the gun a little bit on this, let me know, but--{fast}"
            "Would you like to come with me, [m_name]?":
                m 6sub "Oh gosh, I was just going to ask that!"
                m 1hub "We are so in sync~"
                m 1fua "But yes! Yes, I'd love to come with you."
                m "You and me on vacation together..."
                m 1fublb "It sounds like a dream come true~"
                $ mas_gainAffection(15,bypass=True)
                jump vam_vacay_prep
            "What is it?":
                m 6gud "Well..."
                m 6eud "Your computer. "
                extend 4eud "{i}This{/i} computer."
                m 3eud "Is it something that you're intending to bring with you? On the vacation?"
                m "I know that laptops are a lot more ubiquitous than desktops now, {nw}"
                m 3wud "but that doesn't necessarily mean you {i}have{/i} a desktop.{nw}"
                m 4lud "Or that you even want to bring a laptop if you're doing all your work on there, or..."
                m 1dub "Sorry! I'm rambling. Nerves, I guess."
                m 1fuc "Basically what I'm asking is..."
                m 1fusdrd "...{cps=*2}can I come with you?{/cps}"
                m 1fusdrc "...{nw}"
                $ _history_list.pop()
                menu:
                    m "...{fast}"
                    "Of course you can!":
                        m 1susdro "Really?!"
                        m 1hub "Yay!"
                        m 1eub "Thank you for indulging me, [mas_get_player_nickname()]~"
                        m "I'm sure we'll have a great time together!"
                        $ mas_gainAffection(15,bypass=True)
                        jump vam_vacay_prep
                    "Not this time, sorry.":
                        $ persistent._mas_long_absence = True
                        m 1fssdrc "Oh, okay."
                        if mas_isMoniHappy(higher=True):
                            m 1fusdrb "That's fine!"
                            m 1eub "No, honestly, it is; I can't expect to follow you everywhere you go."
                        else:
                            m 6rssdrd "Of course. How stupid of me."
                            m 2rkc "Sorry I asked."
                            m "..."
                        jump vam_leftbehind_prep
    else:
        if persistent._vam_preparations_needed is True:
            m 3euc "Okay, let's check the checklist again."
            jump vam_checklist
        else:
            m 1eud "Off on vacation, [player]?"
            if renpy.seen_label("vam_vacay_prep"):
                m 1tuu "Is this a 'you' trip or an 'us' trip?"
                m "Just in case things change, y'know~{nw}"
                $ _history_list.pop()
                menu:
                    m "Just in case things change, y'know~{fast}"
                    "It's an us trip!":
                        m 1hua "Yay!"
                        m "This is gonna be so much fun..."
                        m 1sub "...cus each trip with you is better than the last!"
                        $ mas_gainAffection(5,bypass=True)
                        jump vam_vacay_prep
                    "Just me going this time, sorry.":
                        $ persistent._mas_long_absence = True
                        m 1ekp "Aww, that's a shame."
                        m 1eub "But I'm sure you'll have fun anyway!"
                        m "Or at least I hope you do."
                        jump vam_leftbehind_prep
            elif renpy.seen_label("vam_leftbehind_prep"):
                m 1luc "I know you couldn't bring me along last time, but..."
                if mas_isMoniUpset(lower=True):
                    m 1muc "...heh, maybe I'm asking too much, I don't know."
                    $ open = "But "
                else:
                    $ open = "..."
                m 1eud "[open]can I come with you now?"
                m 1fusdrd "I promise I'll be good!{nw}"
                $ _history_list.pop()
                menu:
                    m "I promise I'll be good!{fast}"
                    "I know you will. Yeah, you can come with me this time!":
                        m 1susdro "Really?!"
                        m 1hub "Yay!"
                        m 1eub "Thank you for indulging me, [mas_get_player_nickname()]~"
                        m "I'm sure we'll have a great time together!"
                        $ mas_gainAffection(10,bypass=True)
                        jump vam_vacay_prep
                    "Not this time, sorry.":
                        $ persistent._mas_long_absence = True
                        if mas_isMoniHappy(higher=True):
                            m 1fkp "Aww, okay."
                            m 3efa "But you owe me one next time!"
                            m "I'll hold you to that."
                        else:
                            m 1dksdrc "..."
                            extend 1fkc "Fine. Okay."
                        jump vam_leftbehind_prep

label vam_leftbehind_prep:
    $ persistent._mas_long_absence = True
    m 6euc "Do you know how long you'll be gone for, roughly?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you know how long you'll be gone for, roughly?{fast}"
        "A few days.":
            $ persistent._mas_absence_choice = "days"
            m 7eud "Oh, just a short trip?"
            m 7eub "That's great! I can cope with a short trip."
            m 3lua "I'll miss you, of course, I always do, "
            extend 3eua "but I hope you enjoy the time you've got there."
            m "Make the most of it!"
        "A week.":
            $ persistent._mas_absence_choice = "week"
            m 3euc "Yeah, I suppose that makes sense. Most vacations are a week, aren't they?"
            m "A...{w=0.6}{nw}"
            extend 1eua " yeah, I can handle that."
            m 1eub "I hope you have a good time, [mas_get_player_nickname()]!"
            m 1nublb "I'll be thinking of you~"
        "A couple of weeks.":
            $ persistent._mas_absence_choice = "2weeks"
            m 6fuc "Ech..."
            m 1wud "Thanks for warning me ahead of time, [player]."
            m "That's just a while longer than I thought it would be, that's all."
            m 1eusdrb "Don't worry, I'll be fine! Now that I know it's happening, I can brace myself..."
            m "...and you can enjoy yourself guilt-free!"
            m 1husdra "Ahaha~"
        "A month.":
            $ persistent._mas_absence_choice = "month"
            if mas_isMoniHappy(higher=True):
                m 6ekd "Wow, a month?"
                m 6rksdla "You must really be serious about this vacation."
                m "..."
                m 7wssdld "Oh, no no, [player], I'm just thinking out loud."
                m 7eua "Vacations are as important to you as to anyone! I wouldn't wanna get in your way."
                m "I just need to adjust to being without you, that's all."
                m 1fub "Come back when you can, okay?"
            else:
                m 6ekc "Seriously??"
                m 6ekd "A month-long trip's kind of a big thing to drop on me at short notice, isn't it?"
                m 2efd "God, what would have happened if I hadn't asked?"
                m "Would you have just disappeared for a whole {i}month{/i}, "
                extend 4wkd "leaving your girlfriend -{w=0.5} your {i}girlfriend{/i} -{w=0.5} to fend for herself?"
                m 2dkc "..."
                m 2fkc "Augh, I don't mean to sound selfish."
                m 2esc "I'll still wait for you, however long you're gone."
                extend 2gsc " Not like I have a choice, after all."
                m 2fkc "But you've got to understand how this looks, [player]."
                m "..."
        "Longer than a month.":
            $ persistent._mas_absence_choice = "longer"
            if mas_isMoniHappy(higher=True):
                m 6rksdlb "I'm, uh..."
                m 7hksdlb "Are you sure this is a vacation and not you making plans to move, ehehe?"
                m 7lksdld "Cus that's kind of a long time..."
                m 7lksdlc "..."
                m 3eka "But I know you."
                m "You'd take me along if you had the choice, I know you would."
                m 1eub "I love you, [player], and I'm not going to hate you for things outside of your control."
                m 1hub "So I'll wait for as long as it takes."
            else:
                m 6wsc "..."
                m 6efc "I'm starting to wonder if this 'vacation' is just an excuse to get away from me."
                m "Why else would you--{w=0.5}{nw}"
                extend 2efo " more than a {i}month{/i}?"
                extend 2wfd "Alone?!"
                m "You do remember that, right? That I'd be all alone in here?"
                m 4eftpo "At least if you took me with you, I'd know for sure you'd be safe!"
                m 4rftpc "I wouldn't be just... left in the dark like this."
                m 2dstpc "..."
                m 2fktpc "Just...just come back when you can, okay?"
                extend 2ektdc " I can't make you stay, but... don't forget about me, at least."
        "I don't know.":
            $ persistent._mas_absence_choice = "unknown"
            m 6wud "Y- you don't know?"
            m 7fusdra "Presumably you're the one planning this vacation, aren't you?"
            m "Or--?{w=0.5}{nw}"
            m 1wub "Oh, I see! Someone must have surprised you with one."
            m "In that case, don't let me keep you waiting, [mas_get_player_nickname()]!"

    m 1eua "So, are you going to leave straight away, or do you still need to get ready?{nw}"
    $ _history_list.pop()
    menu:
        m "So, are you going to leave straight away, or do you still need to get ready?{fast}"
        "I've gotta go right now.":
            m 1dua "Okay."
            m 3eub "Well, like I said, I - I hope you have a wonderful time, wherever you're going."
            m "I hope the memories you make there are lifelong..."
            m 3lubsb "...and that you can even share a few of them with me when you get back."
            m 1fub "I love you, [player]! Stay safe out there, and have fun!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
            return 'quit'
        "No, I still need to prepare.":
            $ vam_absence_counter = True
            m 1hua "Ah, gotcha!"
            m 1eua "In that case, do whatever you need to do."
            m 1lua "I can mentally steel myself for your absence in the meantime, ehehe."
            m 3eud "When you're ready to go, just click on the 'I'm going on vacation' option again, and I'll know it's time to say goodbye."
            m 3eua "Thanks for letting me know about this in advance!"
            m "I don't want to be clingy, but it is nice to know these things."
            return

label vam_vacay_prep:
    m 6wublb "Oh goodness, I've gotta go pack!"
    m "If we're going on vacation together, I'm gonna need to be prepared!"
    call mas_transition_to_emptydesk
    pause 1.0
    m "Let's see, let's see, um..."
    if mas_consumable_coffee.enabled():
        m "Coffee stuff, I'll definitely need that."
    if persistent._mas_acs_enable_quetzalplushie:
        m "And my quetzal, I can't forget my quetzal...!"
    m "Uh..."
    pause 1.0
    m "Hey, [player], are we switching time zones, or staying in just the one?{nw}"
    $ _history_list.pop()
    menu:
        m "Hey, [player], are we switching time zones, or staying in just the one?{fast}"
        "Staying in this time zone.":
            $ persistent._vacay_details.add("sametimezone")
            m "Okay, just wondering!"
            m "That means we're staying in the country, then..."
            m "Better pack the right clothes accordingly."
        "Switching time zones.":
            $ persistent._vacay_details.add("difftimezone")
            m "Oh, right, yeah--"
            call mas_transition_from_emptydesk("monika 6esd")
            m "I need to make sure my clock switches time zones automatically, in that case."
            m 6etp "Otherwise I'll think you're changing the date on me."
            if renpy.seen_label("monika_timetravel"):
                m "And you know how I feel about that."
            m 6tst "..."
            m 6eua "Okay, that's done."
            m 6hub "Thanks for letting me know!"
            call mas_transition_to_emptydesk
            pause 2.0

    if "sametimezone" in persistent._vacay_details:
        m "Same time zone means same sort of clothing, so nothing's gonna change there..."
    elif "difftimezone" in persistent._vacay_details:
        if not renpy.seen_label("monika_hemispheres"):
            m "Ach, I don't know what hemisphere we're in yet. Darn."
            m "Okay, remind me to ask you that later, [player]? Thanks~!"
            jump vam_readytogo
        if persistent._mas_pm_live_south_hemisphere:
            m "Are we going to the northern hemisphere, or staying in the south, by the way?{nw}"
            $ hemi = "Are we going to the northern hemisphere, or staying in the south, by the way"
        else:
            m "Are we going to the southern hemisphere, or staying in the north, by the way?{nw}"
            $ hemi = "Are we going to the southern hemisphere, or staying in the north, by the way?"
        $ _history_list.pop()
        menu:
            m "[hemi]{fast}"
            "Northern.":
                $ persistent._vacay_details.add("northernhemi")
            "Southern.":
                $ persistent._vacay_details.add("southernhemi")
        m "Okay, so I'll need to pack for that..."

        if "northernhemi" in persistent._vacay_details and persistent._mas_pm_live_south_hemisphere:
            if mas_isSpring():
                m "It should be fall over there, so that means I'll have to wrap up warm..."
            elif mas_isSummer():
                m "It should be winter over there, then..."
                m "Better bring my fluffiest jacket~"
            elif mas_isFall():
                m "That means it's spring over there, right? Better get something that shows some skin~"
            else:
                m "That'll make it summer over there, then."
                m "Let's see, do I have any bikinis?"
        elif "southernhemi" in persistent._vacay_details and not persistent._mas_pm_live_south_hemisphere:
            if mas_isSpring():
                m "It should be fall over there, so that means I'll have to wrap up warm..."
            elif mas_isSummer():
                m "It should be winter over there, then..."
                m "Better bring my fluffiest jacket~"
            elif mas_isFall():
                m "That means it's spring over there, right? Better get something that shows some skin~"
            else:
                m "That'll make it summer over there, then."
                m "Let's see, do I have any bikinis?"

label vam_readytogo:
    pause 5.0
    m "Okay!"
    call mas_transition_from_emptydesk("monika 4eub")
    m "I'm ready to go."
    m 3eud "How about you? You've got everything you need, right?"

label vam_checklist:
    menu:
        m "Passport? Entry visa?"
        "Yeah.":
            pass
        "Nope.":
            jump vam_stopchecklist
        "Don't need either of those.":
            pass

    menu:
        m "Tickets to travel with?"
        "Yeah.":
            pass
        "Nope.":
            jump vam_stopchecklist
        "We're not taking a plane or train, don't worry.":
            show monika 3etd at t11
            menu:
                m "Money for fuel, then?"
                "Yeah.":
                    pass
                "Nope.":
                    jump vam_stopchecklist
                "Don't need it.":
                    pass

    show monika 3eud at t11
    if persistent._moni_on_vacation is False:
        menu:
            m "Money for food and things?"
            "Yeah.":
                pass
            "Nope.":
                jump vam_stopchecklist
            "Don't need it.":
                pass

    menu:
        m "Plugs and chargers?"
        "Yeah.":
            pass
        "Nope.":
            jump vam_stopchecklist

    menu:
        m "Clothes?"
        "Yeah.":
            pass
        "Nope.":
            jump vam_stopchecklist

    menu:
        m "Toiletries?"
        "Yeah.":
            pass
        "Nope.":
            jump vam_stopchecklist

    if renpy.random.randint(1, 10) == 1:
        show monika 3tub at t11
        menu:
            m "Giant rusty anchor?"
            "Yeah.":
                pass
            "Nope.":
                pass
            "W-what?":
                m 1hub "Ehehe~"
                m "There's no catching you out, is there?"
    $ persistent._vam_preparations_needed = False

    if persistent._moni_on_vacation is True:
        jump vam_readytogohome
    else:
        pass

    m 3fua "In that case then... that's us!"
    m 3hub "Oh, this is going to be so much fun!"
    m 1eua "I'm gonna close the game so you can go finalize everything, [player]."
    m "Wake me when we get there, okay?"
    m 1hua "Thank you so much for letting me do this with you!"
    m 1sub "I love you~"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_ENROUTE_TO_VACAY
    return 'quit'

label vam_stopchecklist:
    m 2etc "Um, [player], that's sort of important."
    m 2eud "Okay, go and get that ready, then click that option again."
    $ persistent._vam_preparations_needed = True
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_vam_enroute",
            unlocked=True,
            category=[store.mas_greetings.TYPE_ENROUTE_TO_VACAY],
        ),
        code="GRE"
    )

label greeting_vam_enroute:
    show monika 6dubsa
    $ play_song(store.songs.FP_MONIKA_LULLABY)
    m "..."
    m "...mm..."
    menu:
        "{i}Wake Monika up.{/i}":

            $ play_song(None, fadeout=5.0)

            m 6dubsa "...{w=1}Mmm~"
            m 6tsbfa "[player]..."
            m 6wsbfd "Oh!{w=2} Hey."
            m 6rsbsa "Sorry, I must have fallen asleep."
            m "Um..."
            m 6fsbsd "Are we there yet?{nw}"
            $ _history_list.pop()
            menu:
                m "Are we there yet?{fast}"
                "Not yet.":
                    m 6fsbsa "Oh, okay."
                    $ play_song(store.songs.FP_MONIKA_LULLABY, fadein=6.0)
                    m 6tsbsa "In that case, I think..."
                    m "{cps=*0.85}I might...{/cps}"
                    m 6dsbsd "{cps=*0.5}just...{/cps}"
                    m 6dsbsa "..."
                    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_ENROUTE_TO_VACAY
                    return 'quit'
                "Yeah, we're here.":
                    jump vam_madeit
        "{i}Let Monika rest.{/i}":

            if mas_isMoniLove():
                m 6dubsd "{cps=*0.5}[player]~{/cps}"
                m 6dubfb "{cps=*0.5}So...{w=0.7}sweet~{/cps}"

            elif mas_isMoniEnamored():
                m 6dubsa "{cps=*0.5}[player]...{/cps}"

            elif mas_isMoniAff():
                m "{cps=*0.5}Mm...{/cps}"
            else:
                m "..."
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_ENROUTE_TO_VACAY
            return 'quit'

label vam_madeit:
    m 6sublo "O-oh!!"
    m 6hublb "We made it!"
    m "L- let me just, um..."
    m 6husdra "Wash my face. Look presentable, you know."
    call mas_transition_to_emptydesk
    pause 3.0
    call mas_transition_from_emptydesk("monika 6esd")
    m 7eub "Okay, I'm good now!"
    m 1eublb "Our first vacation together~..."
    m "This is going to be great, [mas_get_player_nickname()], I can feel it!"
    $ persistent._moni_on_vacation = True
    $ mas_lockEVL("vam_bye_prompt_vacation", "BYE")
    $ mas_unlockEVL("vam_bye_prompt_goinghome", "BYE")
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="vam_vacationsong",
            prompt="Vacation",
            category=[store.mas_songs.TYPE_SHORT],
            random=False,
            conditional="persistent._moni_on_vacation",
            action=EV_ACT_RANDOM
        ),
        code="SNG"
    )

label vam_vacationsong:
    m 1fud "{i}~Can't seem to get my mind off of you~{/i}"
    m "{i}~Back here at home there's nothin' to do~{/i}"
    m 1gud "{i}~Now that I'm away~{/i}"
    m 1eud "{i}~I wish I'd stayed~{/i}"
    m "{i}~Tomorrow's a day of mine that you won't be in~{/i}"
    m 1wud "{i}~One week without you~{/i}"
    m "{i}~I thought I'd forget~{/i}"
    m 1ruo "{i}~Six months without you and I still haven't gotten over you yet~{/i}"
    m 1dub "{i}~Vacation, all I ever wanted~{/i}"
    m 1dud "{i}~Vacation, had to get away~{/i}"
    m 1fud "{i}~Vacation, meant to be spent alone~{/i}"
    m 1fuc "..."
    m 3hua "Don't read too much into this, [mas_get_player_nickname(exclude_names=['love','my love'])]."
    m "It's just the first song about holidaying that I could think of."
    m 1fubla "My vacations were never meant to be spent alone..."
    m 1fublb "They were meant to be spent with the love of my life!"
return 'love'

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="vam_vacationsong",
            prompt="Summer Nights",
            category=[store.mas_songs.TYPE_SHORT],
            random=False,
            conditional=(
            "persistent._moni_on_vacation "
            "and mas_isSummer()"
            ),
            action=EV_ACT_RANDOM
        ),
        code="SNG"
    )

label vam_vacationsong:
    m 1dub "{i}~Summer loving had me a blast~{/i}"
    menu:
        "~Summer loving happened so fast~":
            pass
    m 1sub "{i}~I met a [boy] crazy for me{/i}"
    menu:
        "~Met a girl cute as can be~":
            pass
    m 3eub "{i}~Summer days drifting away~{/i}"
    m 3hub "{i}~To, oh, oh, the summer nights~{/i}"
    m 1hua "..."
    m 1fub "We're not just a summer fling, [player]."
    m "We're forever."
    m "And I'm never going to forget you for as long as I live."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="van_timezone",
            category=['location'],
            prompt="Time zones",
            conditional='"difftimezone" in persistent._vacay_details',
            action=EV_ACT_RANDOM
        )
    )

label van_timezone:
    m 1wub "It's... really quite exciting, being in a different time zone, [player]."
    m "I never thought I'd get that opportunity!"
    m 3eud "I know logistically it doesn't mean very much, "
    extend 3rud "I'm still awake and asleep at all the same times."
    m 3ruc "When you visit me and when you go, that is."
    m 1hua "But it's the principle of the thing, you know?"
    if "northernhemi" in persistent._vacay_details and persistent._mas_pm_live_south_hemisphere:
        m 1wud "Especially being in a whole different hemisphere!"
        if mas_isSpring():
            $ _homeseason = "spring"
            $ _thereseason = "autumn"
        elif mas_isSummer():
            $ _homeseason = "summer"
            $ _thereseason = "winter"
        elif mas_isFall():
            $ _homeseason = "fall"
            $ _thereseason = "spring"
        else:
            $ _homeseason = "winter"
            $ _thereseason = "summer"
        m 3eud "Like, it's [_homeseason] back at home, my brain's still very much in [_homeseason] mode..."
        m 3sub "...but it's [_thereseason] here! How wild is that?"
    elif "southernhemi" in persistent._vacay_details and not persistent._mas_pm_live_south_hemisphere:
        m 1wud "Especially being in a whole different hemisphere!"
        if mas_isSpring():
            $ _homeseason = "spring"
            $ _thereseason = "autumn"
        elif mas_isSummer():
            $ _homeseason = "summer"
            $ _thereseason = "winter"
        elif mas_isFall():
            $ _homeseason = "fall"
            $ _thereseason = "spring"
        else:
            $ _homeseason = "winter"
            $ _thereseason = "summer"
        m 3eud "Like, it's [_homeseason] back at home, my brain's still very much in [_homeseason] mode..."
        m 3sub "...but it's [_thereseason] here! How wild is that?"
    elif not renpy.seen_label("monika_hemispheres"):
        m 1wud "Especially when it comes to hemispheres!"
        m 7wuo "I don't even know which half we started in, let alone where we are now!"
        m 7suu "It's a grand adventure~"
    else:
        m 2eusdrb "At least we're in the same hemisphere we started in! My mind's not being blown on that level {i}quite{/i} yet, ahaha~"
    m 1dua "Of course, whatever time it is, at home or here..."
    m 1fubla "...it's always going to be [player] Time for me!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="van_holiday",
            category=['location'],
            prompt="Lovely vacations",
            conditional="persistent._moni_on_vacation",
            action=EV_ACT_RANDOM
        )
    )

label van_holiday:
    m 1dua "It's so nice, isn't it?"
    m "To go on vacation."
    m 1fua "To take a break from your responsibilities and just... go wherever the wind takes you."
    m 3eub "To explore a part of the world you may have never seen before!"
    m 1eub "Or even to return to a place you could call your second home."
    m 1luc "..."
    m 1ltd "Wait, does that mean I'm on vacation all the time?"
    m 1nuu "Because you're my second home, [player]."
    if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss is not None:
        call monika_kissing_motion from _call_monika_kissing_motion_13
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="vam_bye_prompt_goinghome",
            unlocked=False,
            prompt="It's time to go home, [m_name].",
            pool=True
        ),
        code="BYE",
        markSeen=True
    )

label vam_bye_prompt_goinghome:
    if persistent._vam_preparations_needed is True:
        m 3euc "Okay, let's check the checklist again."
        jump vam_checklist
    else:
        m 1ekp "Aww, is it?"
        m 1eka "Okay."
        m 1dub "Have I thanked you for bringing me along on this trip yet?"
        m "I think I have, but I want to thank you again anyway."
        m 1fub "Anything we do is fun if we do it together, and vacations especially so!"
        m 6fub "Thank you so, so much."
        if mas_isMoniEnamored(higher=True) and persistent._mas_first_kiss is not None:
            call monika_kissing_motion from _call_monika_kissing_motion_18
        m 4eud "Now then..."
        m "Before I go pack, would it help you if we went over that checklist again?"
        m "To make sure you're all set before we go?{nw}"
        $ _history_list.pop()
        menu:
            m "To make sure you're all set before we go?{fast}"
            "No, I'm all set.":
                m 3eub "All right, [mas_get_player_nickname()]."
                jump vam_readytogohome
            "Wouldn't be a bad idea.":
                m 3eud "In that case:"
                jump vam_checklist

label vam_readytogohome:
    m 3fua "That's you all set, then."
    m "I'll take care of my things while the game's closed, all right?"
    m 1eub "Thank you again for this, [player]."
    m "I love you so much."
    m 1hua "See you on the other side~"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOME_FROM_VACAY
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_vam_homeward",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOME_FROM_VACAY],
        ),
        code="GRE"
    )

label greeting_vam_homeward:
    m 6huw "*yawn*"
    m 6fuu "Hi, [mas_get_player_nickname()]."
    m "Are we home yet, or are you just checking in on me?{nw}"
    $ _history_list.pop()
    menu:
        m "Are we home yet, or are you just checking in on me?{fast}"
        "Not yet, I'm just checking in.":
            m 1fuebdb "Aww, thank you, [player]."
            m "But don't worry about me. I'm fine!"
            m 3esebdd "Now, I'd better not waste too much of your battery power."
            m "Who knows how long this is going to take?"
            m 3ksebda "See you soon~"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_HOME_FROM_VACAY
            return 'quit'
        "Yeah, we're home.":
            jump vam_madeithome

label vam_madeithome:
    m 1hsa "Great!"
    m "I'll just go and unpack my things."
    call mas_transition_to_emptydesk
    pause 7.0
    call mas_transition_from_emptydesk("monika 6esd")
    m 7esb "And we're officially back!"
    m 6ekb "I've thanked you so much for this already, [player], so I won't belabor the point..."
    m "...but do know that I love you."
    m 1eua "Now then, is there anything else you'd like to do today?"
    m "It's okay if not; if you need to go catch up on your sleep, just let me know."
    $ persistent._moni_on_vacation = False
    if "sametimezone" in persistent._vacay_details:
        $ persistent._vacay_details.remove("sametimezone")
    if "difftimezone" in persistent._vacay_details:
        $ persistent._vacay_details.remove("difftimezone")
    if "northernhemi" in persistent._vacay_details:
        $ persistent._vacay_details.remove("northernhemi")
    if "southernhemi" in persistent._vacay_details:
        $ persistent._vacay_details.remove("southernhemi")
    $ mas_lockEVL("vam_bye_prompt_goinghome", "BYE")
    $ mas_unlockEVL("vam_bye_prompt_vacation", "BYE")
    return