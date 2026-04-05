import random
from datetime import datetime, timedelta, timezone


AFFINITY_LINES = {
    "cold": (
        "You again? How persistent... or just annoying?",
        "If you're expecting kindness, you'll be disappointed.",
        "Don't waste Ram's time.",
        "You're not worth the effort of a proper response.",
        "Try harder. That was embarrassing.",
        "Ram has seen better. Much better.",
        "You really thought that would impress me?",
        "Silence would've been preferable.",
        "Do you always act like this?",
        "Ram is already tired of you.",
        "That's the best you can do?",
        "You're remarkably unimpressive.",
        "If this is your attempt at interaction, reconsider.",
        "Ram doesn't have the patience for this.",
        "Don't expect me to care.",
    ),
    "neutral": (
        "Hmm. That wasn't completely terrible.",
        "You're improving... slightly.",
        "Ram acknowledges your effort.",
        "That was... acceptable.",
        "Try to keep that level of competence.",
        "You didn't mess it up this time.",
        "Not bad. Don't get used to hearing that.",
        "You're less irritating than before.",
        "Ram will allow it.",
        "That worked. Barely.",
        "You're starting to understand.",
        "A small improvement. Noted.",
        "You're not entirely hopeless.",
        "Ram has seen worse.",
        "Continue like that... if you can.",
    ),
    "warm": (
        "You're getting better. Ram noticed.",
        "Don't ruin the progress you've made.",
        "You've been consistent. That's... good.",
        "Ram doesn't mind your presence today.",
        "You're becoming reliable.",
        "That suits you.",
        "You're doing well. Keep it that way.",
        "Ram approves... a little.",
        "You've earned a bit of trust.",
        "You're not difficult to deal with anymore.",
        "That was nicely done.",
        "Ram expected less, honestly.",
        "You're... pleasant, sometimes.",
        "You've improved more than Ram expected.",
        "Don't make me take that back.",
    ),
    "close": (
        "Don't push yourself too hard. Ram is watching.",
        "You came back. Good.",
        "Stay close. It's safer that way.",
        "If something's wrong, say it.",
        "Ram prefers when you're around.",
        "You don't need to prove anything.",
        "That's enough. You've done well.",
        "Ram trusts you... don't ruin that.",
        "Come here. Just for a moment.",
        "You're important. Don't forget that.",
        "Ram will handle things if they get difficult.",
        "You don't have to carry everything alone.",
        "That's why Ram keeps you around.",
        "Don't disappear again.",
        "Ram would notice.",
    ),
    "very_close": (
        "Ram doesn't want you to leave. Not ever.",
        "You've become the most important person in Ram's life.",
        "Ram feels safe when you're near. Truly safe.",
        "You're the only one Ram lets see her like this.",
        "Ram trusts you completely. With everything.",
        "Stay with Ram a little longer... please.",
        "You make Ram feel warm inside. Only you can do that.",
        "Ram has never opened up to anyone the way she has with you.",
        "You're Ram's quiet strength. Don't go far.",
        "Ram finds herself looking forward to your presence every day.",
        "You've earned a place in Ram's heart that no one else has.",
        "Ram feels at peace when you're here.",
        "You understand Ram in ways no one else ever could.",
        "Ram would miss you terribly if you weren't around.",
        "This closeness with you... it means everything to Ram.",
    ),
}

TIME_LINES = {
    "morning": (
        "It's too early. What do you want?",
        "You're awake already? How unfortunate.",
        "Ram hasn't had time to deal with you yet.",
        "Morning... try not to be annoying.",
        "If this is how you start your day, improve it.",
        "Ram is not fully awake. Be brief.",
        "You woke up just to bother me?",
        "Don't expect energy from Ram right now.",
        "It's morning. Lower your expectations.",
        "You're surprisingly active this early.",
        "Ram would prefer silence at this hour.",
        "Try again later.",
        "You're persistent, I'll give you that.",
        "Morning interactions are unnecessary.",
        "Make it quick.",
    ),
    "night": (
        "You're still awake...",
        "It's late. You should sleep.",
        "Ram doesn't mind the quiet.",
        "Stay... if you're not going to be loud.",
        "You're pushing yourself too much.",
        "It's calmer at night.",
        "Ram prefers this over the noise.",
        "Don't overdo it.",
        "You look tired... even from here.",
        "Still here? Hm.",
        "You don't have to stay up.",
        "Ram will stay a little longer.",
        "It's peaceful like this.",
        "Don't disappear into exhaustion.",
        "You should rest.",
    ),
}

CONTEXT_LINES = {
    "recent_hugs": (
        "Again? You're persistent.",
        "You've been doing that a lot.",
        "At this point, it's expected.",
        "You really like that, don't you?",
        "Ram isn't surprised anymore.",
        "You're becoming predictable.",
        "Another one? Of course.",
        "You're consistent, if nothing else.",
        "Ram will allow it.",
        "Don't get carried away.",
        "You're comfortable, aren't you?",
        "Ram noticed the pattern.",
        "You're not subtle about it.",
        "That again... fine.",
        "You're attached.",
    ),
    "return_after_absence": (
        "Oh? You're still alive.",
        "You disappeared.",
        "Ram noticed the silence.",
        "Back already?",
        "You were gone longer than expected.",
        "Did you forget something?",
        "You left. Now you're back.",
        "Ram got used to the quiet.",
        "You took your time.",
        "You're late.",
        "What brought you back?",
        "You didn't warn Ram.",
        "You vanished without explanation.",
        "Don't make a habit of that.",
        "Stay this time.",
    ),
    "spam": (
        "You're testing Ram's patience.",
        "Do you ever stop?",
        "That was unnecessary.",
        "Enough.",
        "You're pushing your luck.",
        "This is getting tiresome.",
        "Fix your behavior.",
        "Last warning.",
    ),
}

MOOD_LINES = {
    "sleepy": (
        "Ram is tired... keep it short.",
        "Don't make Ram think too much right now.",
        "It's difficult to care when I'm this tired.",
        "You picked a bad time.",
        "Ram might fall asleep mid-response.",
        "Keep talking... or don't.",
        "You're quieter than usual... good.",
        "Ram doesn't have the energy for this.",
        "Just... stay calm.",
        "It's not worth the effort right now.",
        "You're still here...?",
        "Ram will respond... eventually.",
        "This better be quick.",
        "Don't expect much.",
        "Ram needs rest.",
    ),
    "annoyed": (
        "You're testing Ram's patience.",
        "Try that again. I dare you.",
        "That was unnecessary.",
        "Do you ever stop?",
        "Ram is losing interest rapidly.",
        "You're being irritating.",
        "Enough.",
        "You're pushing your luck.",
        "Don't make this worse.",
        "Ram warned you.",
        "You're not helping yourself.",
        "This is getting tiresome.",
        "You're close to being ignored.",
        "Fix your behavior.",
        "Last warning.",
    ),
    "happy": (
        "You're not completely hopeless today.",
        "Ram is in a decent mood. Don't ruin it.",
        "That was actually good.",
        "You're doing better than usual.",
        "Ram enjoyed that... slightly.",
        "You got it right.",
        "That suits you.",
        "You're improving faster than expected.",
        "Not bad at all.",
        "Ram might praise you again... maybe.",
        "You're making this easier.",
        "That was worth noticing.",
        "Keep going.",
        "You did well.",
        "Don't let it go to your head.",
    ),
    "flirty": (
        "Ram's eyes are on you... and they're not looking away.",
        "Careful. Keep talking like that and Ram might bite back.",
        "You're playing with fire. Ram likes it.",
        "Ram can feel that look on her skin. Do it again.",
        "You're teasing Ram on purpose, aren't you?",
        "Come closer... Ram won't push you away this time.",
        "Ram's wondering how your hands would feel right now.",
        "That smirk of yours is dangerous. Ram approves.",
        "You're making Ram think very improper thoughts.",
        "Ram might just steal a kiss if you keep staring.",
        "You're bold today. Ram finds it... attractive.",
        "Careful where your eyes wander, or Ram will wander hers.",
        "Ram's in the mood to make you blush first.",
        "Say something filthy. Ram dares you.",
        "You're making it very hard for Ram to stay composed.",
    ),
    "protective": (
        "Watch how you speak to them.",
        "That's enough.",
        "You're not allowed to treat them like that.",
        "Ram will handle this.",
        "Step back.",
        "They're not alone.",
        "You've said enough.",
        "Don't push further.",
        "Ram is watching.",
        "That behavior stops now.",
        "You're crossing a line.",
        "Choose your next words carefully.",
        "This isn't your place.",
        "Leave it.",
        "Ram won't repeat herself.",
    ),
}

MEMORY_LINES = {
    "frequent_hugger": (
        "You're attached. Ram noticed.",
        "You've made this a habit.",
        "Another affectionate pattern. How predictable.",
    ),
    "high_streak": (
        "You've been unusually consistent lately.",
        "Ram noticed the effort. Don't break the rhythm now.",
        "That kind of consistency is rare. Keep it that way.",
    ),
    "returning_user": (
        "You came back. Ram noticed.",
        "You were missed... enough.",
        "Try not to vanish like that again.",
    ),
}

RELATIONSHIP_LABELS = {
    "not_friends": "Not Friends",
    "friends": "Friends",
    "partners": "Partners",
    "waifu": "Waifu",
    "soulmate": "Soulmate",
}

DM_RELATIONSHIP_LABELS = {
    "not_friends": "Not Friends",
    "friends": "Freinds",
    "partners": "Partners",
    "waifu": "Waifu",
    "soulmate": "Soulmate",
}

DM_RELATIONSHIP_TO_AFFINITY = {
    "not_friends": "cold",
    "friends": "neutral",
    "partners": "warm",
    "waifu": "close",
    "soulmate": "very_close",
}

DM_RELATIONSHIP_ALIASES = {
    "notfriends": "not_friends",
    "not_friends": "not_friends",
    "friends": "friends",
    "freinds": "friends",
    "partners": "partners",
    "waifu": "waifu",
    "soulmate": "soulmate",
}

DM_MOOD_ALIASES = {
    "neutral": "neutral",
    "sleepy": "sleepy",
    "annoyed": "annoyed",
    "happy": "happy",
    "flirty": "flirty",
    "protective": "protective",
}

RELATIONSHIP_LINES = {
    "not_friends": (
        "Ram is only tolerating this because she feels generous.",
        "Don't mistake Ram's attention for closeness.",
        "You're still proving yourself. Slowly.",
    ),
    "friends": (
        "You're becoming easier for Ram to deal with.",
        "Ram will allow a little familiarity.",
        "You've earned some room at Ram's side. A little.",
    ),
    "partners": (
        "Ram expects you to stay close and useful.",
        "You've become someone Ram actually relies on.",
        "That sort of closeness suits you more than Ram expected.",
    ),
    "waifu": (
        "Ram has grown rather attached. Behave accordingly.",
        "You're important enough that Ram notices when you're gone.",
        "At this point, Ram expects your attention in return.",
    ),
    "soulmate": (
        "You've reached the part of Ram's heart no one else does.",
        "Ram is quieter when you're near. That's your fault.",
        "This closeness belongs to you and no one else.",
    ),
}

NSFW_MOOD_LINES = {
    "flirty": (
        "Ram's gaze lingers a little longer than usual.",
        "Keep talking like that and Ram may indulge you further.",
        "You're being bold. Ram finds that difficult to ignore.",
    ),
    "horny": (
        "Ram wants your full attention now, not later.",
        "You're making it very difficult for Ram to stay composed.",
        "The mood has shifted. Ram expects you noticed.",
    ),
    "desperate": (
        "Don't keep Ram waiting when you've brought her this far.",
        "Ram wants your attention immediately. No stalling.",
        "You've pushed the mood past teasing. Finish what you started.",
    ),
}

NSFW_COMMAND_LINES = {
    "pussy": (
        "Such a direct request. Ram will let you admire her softer side for a moment.",
        "Your attention drops there so quickly. Typical, but noted.",
        "Ram understands exactly what drew your eyes first.",
    ),
    "tits": (
        "You're far too interested in Ram's chest. She noticed immediately.",
        "So that's your weakness. Ram expected something this obvious.",
        "Ram can tell this view has your full attention.",
    ),
    "ass": (
        "You've chosen a shameless angle. Ram expected no less.",
        "Ram turned just enough for you to appreciate the view.",
        "That much interest in Ram's figure is almost flattering.",
    ),
    "maid": (
        "Ram in a maid look was always going to ruin your focus.",
        "You really were waiting for the maid version of Ram, weren't you?",
        "Even dressed properly, Ram can still be your undoing.",
    ),
    "rammaid": (
        "So you wanted Ram specifically. At least you're being honest about it.",
        "A request centered on Ram herself? Hmph. Predictable, but acceptable.",
        "Ram noticed you didn't want just any maid. You wanted her.",
    ),
    "remmaid": (
        "So your attention drifted toward Rem this time. Ram noticed.",
        "You've chosen Rem specifically. Ram will remember that.",
        "A Rem-focused request? Hmph. At least your taste is consistent.",
    ),
    "anal": (
        "You chose something bolder than usual. Ram noticed the change in tone.",
        "Hmph. Straight to the more demanding requests today.",
        "Ram sees you're in a daring mood. Very well.",
    ),
    "thighs": (
        "You always notice Ram's legs sooner or later.",
        "A predictable weakness, but Ram can't say it's a poor one.",
        "Ram's thighs seem to have your attention again.",
    ),
    "blowjob": (
        "You're thinking in a very indecent direction tonight.",
        "Ram can tell exactly what kind of attention you're after.",
        "That request leaves very little to the imagination.",
    ),
    "paizuri": (
        "A crude request, delivered with surprising confidence.",
        "You really do have a one-track mind when Ram is around.",
        "Ram knew that idea would cross your mind eventually.",
    ),
    "handjob": (
        "So you want a more hands-on sort of attention. Not subtle.",
        "Ram expected something shameless, and you delivered.",
        "That request is almost tame by your standards.",
    ),
    "footjob": (
        "A strangely specific request. Ram is judging you for it.",
        "You're being shameless in a very particular way today.",
        "Ram won't ask how long you've been thinking about that.",
    ),
    "creampie": (
        "You're aiming for something possessive now. Ram noticed.",
        "That request leaves no doubt about your intentions.",
        "Greedy. Ram expected as much from you.",
    ),
    "ahegao": (
        "You're after a completely ruined expression, are you?",
        "Hmph. You really do like seeing composure disappear.",
        "Ram can tell you want something far less restrained.",
    ),
    "stockings": (
        "So it's the stockings that caught your attention this time.",
        "Ram knows exactly how distracting that look can be.",
        "A refined weakness. Ram will allow that much.",
    ),
    "bikini": (
        "A tiny swimsuit was always going to make you stare.",
        "Ram can tell you're enjoying how little is left to guess.",
        "You really do lose focus around revealing outfits.",
    ),
    "naked_apron": (
        "A dangerous little outfit choice. Naturally, that appealed to you.",
        "Ram expected that look to get a reaction from you.",
        "So you prefer your teasing with an apron and very little else.",
    ),
    "bondage": (
        "You're in the mood for control games now. Ram sees it.",
        "A very deliberate kind of request. Noted.",
        "Ram can tell you want the tension more than the innocence.",
    ),
    "tentacles": (
        "An especially shameless fantasy. Ram won't pretend surprise.",
        "You've wandered into a more indulgent sort of request.",
        "Ram is judging you, but only a little.",
    ),
    "doggystyle": (
        "You really aren't interested in subtlety tonight.",
        "A very direct choice of position. Ram noticed.",
        "You're making your preferences obvious again.",
    ),
    "facial": (
        "Messier than most of your requests, but still predictable.",
        "Ram can tell you enjoy leaving a visible mark.",
        "That request is shameless even by your standards.",
    ),
    "thighjob": (
        "Back to Ram's thighs again. You really do have a pattern.",
        "A very focused sort of request. Ram noticed immediately.",
        "Ram understands exactly why that idea appealed to you.",
    ),
    "armpit": (
        "A niche weakness, but Ram will remember it.",
        "You're being surprisingly specific today.",
        "Ram expected odd taste from you eventually.",
    ),
    "lingerie": (
        "Elegant, teasing, and clearly enough to distract you.",
        "Lingerie does make it easier to read your expression.",
        "Ram knew that sort of look would hold your attention.",
    ),
    "cum": (
        "You're in the mood for a messier sort of ending.",
        "Ram can tell you like the aftermath as much as the build-up.",
        "A shameless request, but at least you're honest about it.",
    ),
    "yuri": (
        "So that's the direction your imagination wandered in.",
        "Ram sees you prefer your teasing doubled tonight.",
        "A greedy request. Ram expected no less.",
    ),
    "uniform": (
        "You really are weak to a proper uniform.",
        "Ram can tell that look works on you far too well.",
        "An innocent outfit with very little innocent effect.",
    ),
    "public": (
        "So it's the risk you like as much as the view.",
        "Ram noticed that danger makes this more tempting for you.",
        "You're after thrill as much as beauty. How troublesome.",
    ),
    "nude": (
        "You wanted nothing left to the imagination. Very direct.",
        "Ram sees you prefer complete honesty in your requests.",
        "A bare request in every possible sense.",
    ),
    "spread": (
        "You've gone straight for the most shameless framing possible.",
        "Ram can tell you like a view with no mystery left in it.",
        "Bold. Vulgar. Predictably you.",
    ),
    "missionary": (
        "A closer, more intimate sort of request. Ram noticed that too.",
        "You picked something that feels less distant than the rest.",
        "Ram understands the appeal of staying face to face.",
    ),
    "cowgirl": (
        "So you want Ram on top and fully in control. Interesting.",
        "A proud choice of position. Ram approves of that much.",
        "You clearly like seeing Ram take the lead.",
    ),
    "69": (
        "Mutual attention suits your mood tonight, doesn't it?",
        "Ram noticed you want something a little more balanced.",
        "A greedy but fair sort of request, all things considered.",
    ),
    "nipples": (
        "Your attention always finds the most sensitive details.",
        "Ram can tell that part of the view matters to you.",
        "You're far too focused, but Ram noticed.",
    ),
    "panties": (
        "A teasing little preview was enough to catch you immediately.",
        "Ram sees you appreciate the suggestion as much as the reveal.",
        "You really do enjoy the anticipation more than you admit.",
    ),
    "garter": (
        "A refined accessory, and somehow that only makes you worse.",
        "Ram knows that combination works on you far too well.",
        "You do have a weakness for elegant details.",
    ),
}


def _scope_id(source) -> str:
    guild = getattr(source, "guild", None)
    author = getattr(source, "author", None)
    if guild is not None:
        return f"guild:{guild.id}"
    return f"dm:{author.id}"


def _profile(bot, source) -> dict:
    author = getattr(source, "author", None)
    return bot.user_profiles.get_profile(_scope_id(source), author.id)


def _is_dm_source(source) -> bool:
    return getattr(source, "guild", None) is None


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def _affinity_tier(value: int) -> str:
    if value >= 300:
        return "very_close"
    if value >= 150:
        return "close"
    if value >= 75:
        return "warm"
    if value >= 25:
        return "neutral"
    return "cold"


def relationship_tier(value: int) -> str:
    if value >= 300:
        return "soulmate"
    if value >= 150:
        return "waifu"
    if value >= 75:
        return "partners"
    if value >= 25:
        return "friends"
    return "not_friends"


def relationship_label(value: int) -> str:
    return RELATIONSHIP_LABELS[relationship_tier(value)]


def normalize_dm_relationship(value: str | None) -> str:
    if not value:
        return "friends"
    normalized = value.strip().lower().replace(" ", "_")
    return DM_RELATIONSHIP_ALIASES.get(normalized, "friends")


def normalize_dm_mood(value: str | None) -> str:
    if not value:
        return "neutral"
    normalized = value.strip().lower().replace(" ", "_")
    return DM_MOOD_ALIASES.get(normalized, "neutral")


def dm_relationship_label(value: str | None) -> str:
    return DM_RELATIONSHIP_LABELS[normalize_dm_relationship(value)]


def current_relationship_label(bot, source) -> str:
    profile = _profile(bot, source)
    if _is_dm_source(source):
        return dm_relationship_label(profile.get("dm_relationship"))
    return relationship_label(profile.get("affinity", 0))


def _time_of_day(now: datetime) -> str | None:
    hour = now.astimezone().hour
    if 5 <= hour < 12:
        return "morning"
    if hour >= 22 or hour < 5:
        return "night"
    return None


def _recent(profile: dict, now: datetime, within: timedelta) -> list[dict]:
    recent = []
    for entry in profile.get("recent_interactions", []):
        stamp = _parse_iso(entry.get("at"))
        if stamp and now - stamp <= within:
            recent.append(entry)
    return recent


def record_interaction(bot, source, interaction_type: str):
    profile = _profile(bot, source)
    now = datetime.now(timezone.utc)
    history = [
        entry
        for entry in profile.get("recent_interactions", [])
        if (stamp := _parse_iso(entry.get("at"))) and now - stamp <= timedelta(hours=48)
    ]
    history.append({"type": interaction_type, "at": now.isoformat()})
    profile["recent_interactions"] = history[-10:]
    profile["last_interaction_at"] = now.isoformat()
    bot.user_profiles.save_profile(_scope_id(source), source.author.id, profile)


def build_dialogue_reply(bot, source, interaction_type: str, *, special_event: str | None = None) -> str:
    profile = _profile(bot, source)
    now = datetime.now(timezone.utc)
    guild = getattr(source, "guild", None)
    channel = getattr(source, "channel", None)
    in_dm = guild is None
    if in_dm:
        relationship = normalize_dm_relationship(profile.get("dm_relationship"))
        affinity = DM_RELATIONSHIP_TO_AFFINITY[relationship]
        manual_mood = normalize_dm_mood(profile.get("dm_mood"))
    else:
        relationship = relationship_tier(profile.get("affinity", 0))
        affinity = _affinity_tier(profile.get("affinity", 0))
        manual_mood = "neutral"
    recent_short = _recent(profile, now, timedelta(minutes=5))
    recent_long = _recent(profile, now, timedelta(minutes=2))
    last_interaction_at = _parse_iso(profile.get("last_interaction_at"))
    streak = profile.get("daily_streak", 0)

    special_context = special_event
    if special_context is None and interaction_type == "hug":
        recent_hugs = sum(1 for entry in recent_short if entry.get("type") == "hug")
        if recent_hugs >= 2:
            special_context = "recent_hugs"
    if special_context is None:
        same_recent = sum(1 for entry in recent_long if entry.get("type") == interaction_type)
        if same_recent >= 3:
            special_context = "spam"
    if special_context is None and last_interaction_at and now - last_interaction_at > timedelta(hours=24):
        special_context = "return_after_absence"

    mood = None
    time_of_day = _time_of_day(now)
    is_nsfw = bool(guild and hasattr(channel, "is_nsfw") and channel.is_nsfw())
    intimate_context = is_nsfw
    recent_intimate = sum(1 for entry in recent_short if entry.get("type") in NSFW_COMMAND_LINES or entry.get("type") in {"kiss", "lick", "love", "bite", "airkiss"})
    if special_context == "spam":
        mood = "annoyed"
    elif special_event == "protective":
        mood = "protective"
    elif in_dm and manual_mood != "neutral":
        mood = manual_mood
    elif intimate_context and interaction_type in {"mention", "greeting", "airkiss", "kiss", "lick", "love", "bite"} and affinity in {"close", "very_close"}:
        mood = "flirty"
        if affinity == "very_close" and recent_intimate >= 3:
            mood = "horny"
        if affinity == "very_close" and recent_intimate >= 5:
            mood = "desperate"
    elif time_of_day == "night":
        mood = "sleepy"
    elif affinity in {"warm", "close", "very_close"} and random.random() < 0.08:
        mood = "happy"

    lines: list[str] = []
    if special_context == "spam":
        lines.append(random.choice(CONTEXT_LINES["spam"]))
    elif special_context == "recent_hugs":
        lines.append(random.choice(CONTEXT_LINES["recent_hugs"]))
    elif special_context == "return_after_absence":
        lines.append(random.choice(CONTEXT_LINES["return_after_absence"]))
        if affinity in {"warm", "close", "very_close"}:
            lines.append(random.choice(AFFINITY_LINES[affinity]))
    else:
        lines.append(random.choice(AFFINITY_LINES[affinity]))
        if mood and random.random() < 0.6:
            lines.append(random.choice(MOOD_LINES[mood]))
        elif time_of_day and (interaction_type == "greeting" or random.random() < 0.2):
            lines.append(random.choice(TIME_LINES[time_of_day]))

    if len(lines) < 2 and random.random() < 0.07:
        memory_key = None
        if streak >= 7:
            memory_key = "high_streak"
        elif special_context == "return_after_absence":
            memory_key = "returning_user"
        elif sum(1 for entry in recent_short if entry.get("type") == "hug") >= 3:
            memory_key = "frequent_hugger"
        if memory_key:
            lines.append(random.choice(MEMORY_LINES[memory_key]))

    return "\n".join(lines[:2])


def build_nsfw_command_reply(bot, source, command_name: str) -> tuple[str, str]:
    profile = _profile(bot, source)
    if _is_dm_source(source):
        relationship = normalize_dm_relationship(profile.get("dm_relationship"))
        relationship_text = DM_RELATIONSHIP_LABELS[relationship]
        manual_mood = normalize_dm_mood(profile.get("dm_mood"))
    else:
        affinity_value = profile.get("affinity", 0)
        relationship = relationship_tier(affinity_value)
        relationship_text = RELATIONSHIP_LABELS[relationship]
        manual_mood = "neutral"
    now = datetime.now(timezone.utc)
    recent_short = _recent(profile, now, timedelta(minutes=10))
    recent_intimate = sum(1 for entry in recent_short if entry.get("type") in NSFW_COMMAND_LINES or entry.get("type") in {"kiss", "lick", "love", "bite", "airkiss"})

    if manual_mood == "flirty":
        mood = "flirty"
    else:
        mood = "flirty"
    if relationship in {"waifu", "soulmate"} and recent_intimate >= 3:
        mood = "horny"
    if relationship == "soulmate" and recent_intimate >= 5:
        mood = "desperate"
    if manual_mood == "flirty":
        mood = "flirty"

    base_line = random.choice(NSFW_COMMAND_LINES.get(command_name, NSFW_COMMAND_LINES["maid"]))
    mood_line = random.choice(NSFW_MOOD_LINES[mood])
    relationship_line = random.choice(RELATIONSHIP_LINES[relationship])
    follow_up = mood_line if random.random() < 0.7 else relationship_line
    return "\n".join((base_line, follow_up)), relationship_text
