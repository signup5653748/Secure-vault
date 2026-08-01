with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    lines = f.readlines()

effect_lines = lines[74:107]
del lines[74:107]

lines.insert(103, "".join(effect_lines))

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.writelines(lines)
print("moved effect")
