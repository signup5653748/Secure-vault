import re
with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

bottom_bar_old = """                            isDeleteMode = false
                            selectedFieldsToDelete = setOf()
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color.Red)
                    ) {
                        Text("Delete / Done")
                    }
                    Spacer(modifier = Modifier.weight(1f))
                }
            } else {"""

bottom_bar_new = """                            isDeleteMode = false
                            selectedFieldsToDelete = setOf()
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color.Red)
                    ) {
                        Text("Delete / Done")
                    }
                    Spacer(modifier = Modifier.weight(1f))
                }
            } else if (isReorderMode) {
                BottomAppBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {
                    Spacer(modifier = Modifier.weight(1f))
                    Button(onClick = { isReorderMode = false }) {
                        Text("Done Reordering")
                    }
                    Spacer(modifier = Modifier.weight(1f))
                }
            } else {"""

text = text.replace(bottom_bar_old, bottom_bar_new)
with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

