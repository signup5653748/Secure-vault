import os

for root, dirs, files in os.walk("app/src/main/java"):
    for file in files:
        if file.endswith(".kt"):
            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                content = f.read()
            
            content = content.replace("Icons.Default.ArrowBack", "Icons.AutoMirrored.Filled.ArrowBack")
            
            with open(filepath, "w") as f:
                f.write(content)

print("Fixed icons again")
