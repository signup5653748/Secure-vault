with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

import re

notes_old = """                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Text(
                        text = (entry[BasicField.Notes]?.content ?: ""),
                        modifier = Modifier.padding(16.dp),
                        fontSize = 16.sp
                    )
                }"""

notes_new = """                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    androidx.compose.foundation.text.selection.SelectionContainer {
                        Text(
                            text = (entry[BasicField.Notes]?.content ?: ""),
                            modifier = Modifier.padding(16.dp),
                            fontSize = 16.sp
                        )
                    }
                }"""

text = text.replace(notes_old, notes_new)

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)
print("fixed selection")
