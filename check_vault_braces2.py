with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    text = f.read()

start_index = text.find('fun VaultScreen')
start_brace = text.find('{', start_index)
open_braces = 0

for i in range(start_brace, len(text)):
    if text[i] == '{': open_braces += 1
    elif text[i] == '}': open_braces -= 1
    if open_braces == 0:
        line_num = text[:i].count('\n') + 1
        print(f"Ends at line {line_num}")
        break
