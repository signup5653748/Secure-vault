import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

bad_import1 = "app.keemobile.kotpass.models.PredefinedIcon.valueOf"
good_import1 = "app.keemobile.kotpass.constants.PredefinedIcon.valueOf"
content = content.replace(bad_import1, good_import1)

bad_import2 = "app.keemobile.kotpass.models.PredefinedIcon.Key"
good_import2 = "app.keemobile.kotpass.constants.PredefinedIcon.Key"
content = content.replace(bad_import2, good_import2)

bad_fields = "fields = fieldsMap"
good_fields = "fields = EntryFields(fieldsMap)"
content = content.replace(bad_fields, good_fields)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
