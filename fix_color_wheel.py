import re

files = [
    'app/src/main/java/com/example/ui/AddEntryScreen.kt',
    'app/src/main/java/com/example/ui/AddGroupScreen.kt'
]

old_colors = """                                        colors = listOf(
                                            Color.Red,
                                            Color.Magenta,
                                            Color.Blue,
                                            Color.Cyan,
                                            Color.Green,
                                            Color.Yellow,
                                            Color.Red
                                        )"""

new_colors = """                                        colors = listOf(
                                            Color.Red,
                                            Color.Yellow,
                                            Color.Green,
                                            Color.Cyan,
                                            Color.Blue,
                                            Color.Magenta,
                                            Color.Red
                                        )"""

for fpath in files:
    with open(fpath, 'r') as f:
        content = f.read()
    
    if old_colors in content:
        content = content.replace(old_colors, new_colors)
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"Fixed {fpath}")
    else:
        print(f"Pattern not found in {fpath}")
