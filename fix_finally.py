import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target = """                context.contentResolver.openOutputStream(uri, "wt")?.use { outputStream ->
                    java.io.FileInputStream(tempFile).use { fis ->
                        fis.copyTo(outputStream)
                    }
                }
                tempFile.delete()"""

replacement = """                try {
                    context.contentResolver.openOutputStream(uri, "wt")?.use { outputStream ->
                        java.io.FileInputStream(tempFile).use { fis ->
                            fis.copyTo(outputStream)
                        }
                    }
                } finally {
                    tempFile.delete()
                }"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
print("Added finally block for tempFile deletion")
