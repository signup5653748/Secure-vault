import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

bottom_bar_old = """        bottomBar = {
            if (isDeleteMode) {
                BottomAppBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {"""

bottom_bar_new = """        bottomBar = {
            if (isDeleteMode || isReorderMode) {
                BottomAppBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {"""

text = text.replace(bottom_bar_old, bottom_bar_new)

delete_btn_old = """                            isDeleteMode = false
                            selectedFieldsToDelete = setOf()
                        }
                    ) {
                        Text("Delete Selected Fields")
                    }
                }
            } else {"""

delete_btn_new = """                            isDeleteMode = false
                            selectedFieldsToDelete = setOf()
                        }
                    ) {
                        Text("Delete Selected Fields")
                    }
                }
            }
            if (isReorderMode) {
                BottomAppBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {
                    Spacer(modifier = Modifier.weight(1f))
                    Button(onClick = { isReorderMode = false }) {
                        Text("Done Reordering")
                    }
                }
            } else if (!isDeleteMode && !isReorderMode) {"""

# Need to accurately replace the end of bottombar
# Let's just find the exact text in the file.
