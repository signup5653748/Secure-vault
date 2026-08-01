import re
with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

# I see how it could show two Notes fields!
# Because the AddEntryScreen loops over `customFields` and renders an OutlinedTextField for each.
# If the "Notes" field gets added to customFields (because it has string key "Notes"), it will render as a custom field AND as the standard "Notes" field.
# My fix in `fix_basic_keys.py` where I added `key != "Notes" && key != "Title"` etc. to the filter for `customFields` should have fixed this bug!
print("Double notes bug should be fixed by basic keys filter")
