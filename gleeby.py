#!/usr/bin/env python3

import random
import time
import os
import json
from datetime import datetime, timedelta

gleeby_art_paths = [
    "/home/mossware/mossware/gleeb/gleeby.txt",
    "/home/mossware/mossware/gleeb/gleeby_2.txt",
    "/home/mossware/mossware/gleeb/gleeby_3.txt"
]

state_path = "/home/mossware/mossware/gleeb/gleeby_state.json"

def load_random_gleeby_art():
    art_path = random.choice(gleeby_art_paths)
    with open(art_path, "r") as file:
        return file.read()

moods = [
    "(*≧▽≦)", "(｡•́︿•̀｡) zzz", "(*´﹃｀*)",
    "(╥﹏╥)", "(≖︿≖)", "(＾▽＾)", "(¬_¬ )"
]
gibberish = [
    "bleep veerp glorp", "zrrrp zrrp... blaaah", "*GLRPPP*",
    "neerp bloop!!", "GLOORB!!!", "veeeb vrrrp~"
]
random_events = [
    "Gleeby found a space snail and made it a hat.",
    "Gleeby stared at a star until it blinked back.",
    "A cosmic fart passed by. Gleeby giggled.",
    "Gleeby accidentally invented a new dance move.",
    "Gleeby thought your shoe was a spaceship.",
    "Gleeby whispered to a meteorite. It whispered back.",
    "Gleeby painted a picture using moon slime.",
    "Gleeby tried to eat a comet. Oops.",
    "Gleeby watched space TV: just static, but compelling.",
    "Gleeby tried to do taxes. Failed adorably."
]

if os.path.exists(state_path):
    with open(state_path, "r") as file:
        state = json.load(file)
        hunger = state.get("hunger", 7)
        happiness = state.get("happiness", 5)
        start_time = datetime.fromisoformat(state.get("start_time"))
        inventory = state.get("inventory", {})
        level = state.get("level", 1)
else:
    hunger = 7
    happiness = 5
    inventory = {}
    level = 1
    start_time = datetime.now()

last_event_time = datetime.now()
last_hunger_tick = datetime.now()

def save_state():
    with open(state_path, "w") as file:
        json.dump({
            "hunger": hunger,
            "happiness": happiness,
            "start_time": start_time.isoformat(),
            "inventory": inventory,
            "level": level
        }, file)

def check_level_up():
    global inventory, level
    requirements = {1: 5, 2: 10, 3: 25}
    max_level = max(requirements.keys())
    current_required = requirements.get(level, 9999)
    if all(inventory.get(item, 0) >= current_required for item in ["shiny rock", "alien flower", "comet dust", "star fragment", "moon shard"]):
        print(f"\n🎉 Gleeby leveled up to level {level + 1}!! 🎉")
        level += 1
        for item in inventory:
            inventory[item] -= current_required
        inventory = {k: v for k, v in inventory.items() if v > 0}

def print_gleeby():
    os.system("clear")
    print("\n" + load_random_gleeby_art())
    print("Mood:", random.choice(moods))
    print("Gleeby says:", random.choice(gibberish))
    print(f"Happiness: {happiness}/10")
    print(f"Hunger: {hunger}/10")
    print(f"Level: {level}")

    item_emojis = {
        "shiny rock": "🪨",
        "alien flower": "🌸👽",
        "comet dust": "✨",
        "star fragment": "🌟",
        "moon shard": "🌙"
    }

    print("\nInventory:")
    if inventory:
        for item, count in inventory.items():
            emoji = item_emojis.get(item, "❓")
            print(f"- {emoji} {item}: {count}")
    else:
        print("~ (empty)")


while True:
    if datetime.now() - last_hunger_tick > timedelta(seconds=180):
        hunger = max(hunger - 1, 0)
        last_hunger_tick = datetime.now()
        if hunger < 3:
            print("\n⚠️ Gleeby is getting HUNGRY and sad...")
            happiness = max(happiness - 1, 0)

    print_gleeby()

    if datetime.now() - last_event_time > timedelta(seconds=random.randint(60, 180)):
        event = random.choice(random_events)
        print("\n🌟 RANDOM EVENT! 🌟")
        print(f"{event}")
        last_event_time = datetime.now()

    if datetime.now() - start_time > timedelta(hours=24):
        print("\n💖 Gleeby has been with you for 24 hours!")
        print("He emits a happy slime burble.")
        os.remove(state_path)
        break

    print("\nPress to interact:")
    print("1 - Feed")
    print("2 - Play")
    print("3 - Put to sleep")
    print("4 - Go for a walk")
    print("5 - Quit")

    choice = input("\n> ")

    if choice == "1":
        print("\n🍽️ Gleeby chomps your offering...\n")
        if random.random() < 0.2:
            print("😖 Gleeby hated it! He lets out a disappointed glorp.")
            hunger = max(hunger - 1, 0)
            happiness = max(happiness - 4, 0)
        else:
            print("😋 Gleeby is satisfied and wiggles happily.")
            hunger = min(hunger + 2, 10)
            happiness = min(happiness + 1, 10)

    elif choice == "2":
        print("\n🎲 You play space peek-a-boo with Gleeby!\n")
        happiness = min(happiness + 1, 10)

    elif choice == "3":
        print("\n🛌 Gleeby curls into a goop-ball and dozes off.\n")
        happiness = min(happiness + 2, 10)

    elif choice == "4":
        print("\n🚶 Gleeby oozes outside for a walk...\n")
        if random.random() < 0.5:
            walk_events = {
                "shiny rock": "You find a shiny rock.",
                "star fragment": "You discover a glowing star fragment.",
                "alien flower": "An alien flower blooms at your feet.",
                "comet dust": "You catch a piece of comet dust.",
                "moon shard": "You find a mysterious moon shard."
            }
            item, message = random.choice(list(walk_events.items()))
            print(f"🌿 {message}")
            if item in inventory:
                inventory[item] += 1
            else:
                inventory[item] = 1
        else:
            print("🌌 A calm stroll. Nothing unusual happens.")

    elif choice == "5":
        print("\n👋 Gleeby glorps away into the mist. Goodbye!\n")
        save_state()
        break

    else:
        print("\n?? Gleeby blinks in confusion.\n")
        happiness = max(happiness - 1, 0)

    check_level_up()
    save_state()
    time.sleep(2)
    print_gleeby()
