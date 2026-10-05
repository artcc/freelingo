"""Server-owned language arcade. No database or browser dependencies."""
import random
import time
import unicodedata
from uuid import uuid4

# This is intentionally server-owned. The client may present these games, but it
# cannot add an engine, change scoring, or make a non-arcade game enter this path.
GAME_CATALOG = {
    "quick_choice": {"engine": "arena", "skill": "vocabulary"},
    "spelling": {"engine": "arena", "skill": "writing"},
    "word_scramble": {"engine": "arena", "skill": "vocabulary"},
    "memory": {"engine": "arena", "skill": "memory"},
    "matching": {"engine": "arena", "skill": "vocabulary"},
}
GAMES = frozenset(GAME_CATALOG)


def letters(word):
    result = []
    for character in unicodedata.normalize("NFC", word):
        if unicodedata.combining(character) and result:
            result[-1] += character
        else:
            result.append(character)
    return result


def create(game, entries, difficulty, relaxed=False, now=None):
    if game not in GAME_CATALOG:
        raise ValueError("Unsupported arcade game")
    now = time.time() if now is None else now
    rng = random.SystemRandom()
    unique = {}
    for entry in entries:
        word, definition = entry.word.strip(), entry.definition.strip()
        if word and definition and len(letters(word)) <= 24:
            unique.setdefault(word.casefold(), (word, definition))
    bank = list(unique.values())
    rng.shuffle(bank)
    count = 3 + difficulty - 1 if game in {"memory", "matching"} else 5
    if len(bank) < max(count, 4):
        raise ValueError("Not enough authored vocabulary for this language and level")
    state = dict(arena=1, game=game, difficulty=difficulty, relaxed=relaxed,
        phase="playing", index=0, total=count, lives=3, correct=0,
        attempts=0, matched=[], opened=[], feedback=None, log=[],
        deadline=None, cooldown=0, started=now, questions=[], cards=[], max_moves=18 + difficulty * 4)
    if game in {"memory", "matching"}:
        cards = []
        for word, definition in bank[:count]:
            key = str(uuid4())
            cards += [dict(id=str(uuid4()), label=word, pair=key, side="word"),
                      dict(id=str(uuid4()), label=definition, pair=key, side="meaning")]
        rng.shuffle(cards)
        state["cards"] = cards
    else:
        for word, definition in bank[:count]:
            alternatives = [d for w, d in bank if d != definition]
            rng.shuffle(alternatives)
            choices = list(dict.fromkeys([definition, *alternatives]))[:4]
            if len(choices) != 4:
                raise ValueError("Not enough distinct definitions")
            rng.shuffle(choices)
            tiles = [dict(id=str(uuid4()), label=char) for char in letters(word)]
            rng.shuffle(tiles)
            state["questions"].append(dict(word=word, definition=definition, choices=choices, tiles=tiles))
        if game == "quick_choice" and not relaxed:
            state["deadline"] = now + 14 - difficulty * 2
    return state


def public(state):
    """Strict allowlist: never send solutions, deck labels, pairs or move log."""
    out = {key: state[key] for key in ("game", "difficulty", "phase", "index", "total", "lives", "correct",
        "attempts", "max_moves", "feedback", "deadline", "relaxed")}
    out["version"] = len(state["log"])
    out["server_time"] = time.time()
    if state["game"] in {"memory", "matching"}:
        out["cards"] = [dict(id=card["id"], side=card["side"],
            label=card["label"] if state["game"] == "matching" or card["id"] in state["opened"] + state["matched"] else None,
            matched=card["id"] in state["matched"], opened=card["id"] in state["opened"]) for card in state["cards"]]
    elif state["index"] < len(state["questions"]) and state["phase"] != "finished":
        question = state["questions"][state["index"]]
        out["question"] = dict(prompt=question["word"], choices=question["choices"]) if state["game"] == "quick_choice" else dict(prompt=question["definition"], tiles=question["tiles"])
    if "result" in state:
        out["result"] = state["result"]
    return out


def apply(state, move, now=None):
    now = time.time() if now is None else now
    action_id = move["action_id"]
    prior = next((item for item in state["log"] if item["action_id"] == action_id), None)
    if prior:
        if prior["move"] != move:
            raise ValueError("Action ID reused with different content")
        return False
    if state["phase"] == "finished":
        raise ValueError("Round already finished")
    if move["version"] != len(state["log"]):
        raise ValueError("Stale move; reload the round")
    if len(state["log"]) >= 100:
        raise ValueError("Move limit reached")
    kind, game = move["kind"], state["game"]
    if kind == "leave":
        if state["attempts"] == 0:
            raise ValueError("Play at least one move before saving")
        state["phase"], state["won"] = "finished", False
    elif kind == "continue" and state["phase"] == "feedback":
        state["feedback"], state["phase"] = None, "playing"
        state["index"] += 1
        if game == "quick_choice" and not state["relaxed"]:
            state["deadline"] = now + 14 - state["difficulty"] * 2
    elif kind == "hide" and game == "memory" and len(state["opened"]) == 2:
        if now < state["cooldown"]:
            raise ValueError("Wait before closing the cards")
        state["opened"], state["feedback"] = [], None
    elif kind == "flip" and game == "memory" and state["phase"] == "playing":
        card_id = move.get("value", "")
        card = next((c for c in state["cards"] if c["id"] == card_id), None)
        if not card or card_id in state["matched"] + state["opened"] or len(state["opened"]) == 2:
            raise ValueError("Invalid card")
        state["opened"].append(card_id)
        if len(state["opened"]) == 2:
            first = next(c for c in state["cards"] if c["id"] == state["opened"][0])
            correct = first["pair"] == card["pair"]
            state["attempts"] += 1
            if correct:
                state["matched"] += state["opened"]
                state["correct"] += 1
            state["feedback"], state["cooldown"] = dict(correct=correct), now + 0.8
            if state["correct"] == state["total"] or state["attempts"] >= state["max_moves"]:
                state["phase"] = "finished"
                state["won"] = state["correct"] == state["total"]
    elif kind == "pair" and game == "matching" and state["phase"] == "playing":
        ids = move.get("order", [])
        cards = [c for c in state["cards"] if c["id"] in ids]
        if len(ids) != 2 or len(cards) != 2 or any(i in state["matched"] for i in ids):
            raise ValueError("Invalid pair")
        if cards[0]["side"] == cards[1]["side"]:
            raise ValueError("Select a word and a meaning")
        correct = cards[0]["pair"] == cards[1]["pair"]
        state["attempts"] += 1
        state["feedback"] = dict(correct=correct)
        if correct:
            state["matched"] += ids
            state["correct"] += 1
        else:
            state["lives"] -= 1
        if state["correct"] == state["total"] or state["lives"] == 0:
            state["phase"], state["won"] = "finished", state["lives"] > 0
    elif kind in {"answer", "timeout"} and game not in {"memory", "matching"} and state["phase"] == "playing":
        question = state["questions"][state["index"]]
        expired = state["deadline"] is not None and now >= state["deadline"]
        if kind == "timeout" and not expired:
            raise ValueError("Timer has not expired")
        if game == "quick_choice":
            value = move.get("value", "")
            if kind != "timeout" and value not in question["choices"]:
                raise ValueError("Invalid choice")
            correct = not expired and kind != "timeout" and value == question["definition"]
        else:
            order = move.get("order", [])
            tile_map = {tile["id"]: tile["label"] for tile in question["tiles"]}
            if len(order) != len(tile_map) or set(order) != set(tile_map):
                raise ValueError("Use every letter exactly once")
            correct = "".join(tile_map[i] for i in order) == question["word"]
        state["attempts"] += 1
        if correct:
            state["correct"] += 1
        else:
            state["lives"] -= 1
        state["feedback"] = dict(correct=correct, answer=question["word"], meaning=question["definition"])
        state["deadline"] = None
        if state["index"] + 1 == state["total"] or state["lives"] == 0:
            state["phase"], state["won"] = "finished", state["lives"] > 0
        else:
            state["phase"] = "feedback"
    else:
        raise ValueError("Invalid move for this state")
    state["log"].append(dict(action_id=action_id, move=move))
    return True


def score(state):
    """Challenge completion and attempt accuracy are deliberately different."""
    return dict(correct=state["correct"], questions=state["attempts"], challenge_items=state["total"],
        round_score=round(state["correct"] / state["total"] * 100),
        xp=state["correct"] * 5, won=bool(state.get("won", False)))
