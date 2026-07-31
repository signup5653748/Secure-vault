import sys

with open('app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

target = """                        }
                    }
                }
            if (showPassword) {"""
replacement = """                        }
                    }
                }
            }
            if (showPassword) {"""

new_content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(new_content)
print("Fixed Brace!")
