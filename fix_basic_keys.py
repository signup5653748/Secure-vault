with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

# Make sure basic keys also filters out string values if they accidentally ended up as strings
# Actually it filters out standard fields:
filter_old = """            val basicKeys = setOf(BasicField.Title(), BasicField.UserName(), BasicField.Password(), BasicField.Url(), BasicField.Notes())
            val customFields = entry.fields.entries.filter { it.key !in basicKeys }"""

filter_new = """            val basicKeys = setOf(BasicField.Title(), BasicField.UserName(), BasicField.Password(), BasicField.Url(), BasicField.Notes())
            val customFields = entry.fields.entries.filter { it.key !in basicKeys && it.key != "Notes" && it.key != "Title" && it.key != "UserName" && it.key != "URL" && it.key != "Password" }"""

text = text.replace(filter_old, filter_new)

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

filter_old_add = """        val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
        for ((key, value) in currentEntry!!.fields) {
            if (key !in basicFields) {"""

filter_new_add = """        val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
        for ((key, value) in currentEntry!!.fields) {
            if (key !in basicFields && key != "Notes" && key != "Title" && key != "UserName" && key != "URL" && key != "Password") {"""

text = text.replace(filter_old_add, filter_new_add)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

print("Fixed basic keys filtering")
