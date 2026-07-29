with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# I will count { and } and append enough } at the very end
open_b = content.count("{")
close_b = content.count("}")

print(f"Open: {open_b}, Close: {close_b}")

if open_b > close_b:
    content += "}" * (open_b - close_b) + "\n"
    with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
        f.write(content)

