import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

bank_account_old = """                        BasicField.Title() to EntryValue.Plain("Bank Account"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain("")"""

bank_account_new = """                        BasicField.Title() to EntryValue.Plain("Bank Account"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain(""),
                        BasicField.Notes() to EntryValue.Plain(""),
                        "Account Number" to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        "Routing Number" to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        "Bank Name" to EntryValue.Plain("")"""

content = content.replace(bank_account_old, bank_account_new)

note_old = """                        BasicField.Title() to EntryValue.Plain("Note"),
                        BasicField.Notes() to EntryValue.Plain("")"""

note_new = """                        BasicField.Title() to EntryValue.Plain("Note"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain(""),
                        BasicField.Notes() to EntryValue.Plain(""),
                        "Note Content" to EntryValue.Plain("")"""
                        
content = content.replace(note_old, note_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
