import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

text = text.replace("newCustomFields\n    } else {\n        mutableListOf<CustomFieldData>()\n    }) }", "newCustomFields.toList()\n    } else {\n        listOf<CustomFieldData>()\n    }) }")

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)
print("fixed type")
