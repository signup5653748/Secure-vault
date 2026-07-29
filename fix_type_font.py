import re

with open('/app/applet/app/src/main/java/com/example/ui/theme/Type.kt', 'r') as f:
    content = f.read()

content = content.replace("FontFamily.Monospace", "FontFamily.SansSerif")

with open('/app/applet/app/src/main/java/com/example/ui/theme/Type.kt', 'w') as f:
    f.write(content)
