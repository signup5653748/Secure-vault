with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

filter_old_add2 = """                                            val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
                                            
                                            for ((key, value) in template.fields) {
                                                if (key !in basicFields) {"""
                                                
filter_new_add2 = """                                            val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
                                            
                                            for ((key, value) in template.fields) {
                                                if (key !in basicFields && key != "Notes" && key != "Title" && key != "UserName" && key != "URL" && key != "Password") {"""

text = text.replace(filter_old_add2, filter_new_add2)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

print("Fixed template filter")
