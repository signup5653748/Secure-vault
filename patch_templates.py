import re

with open('/app/applet/app/src/main/java/com/example/ui/TemplatesScreen.kt', 'r') as f:
    content = f.read()

btn_old = """        floatingActionButton = {
            FloatingActionButton(
                onClick = onNavigateToAddTemplate,
                containerColor = Color(0xFF0066FF),
                contentColor = Color.White
            ) {"""
btn_new = """        floatingActionButton = {
            var isNavigating by remember { mutableStateOf(false) }
            FloatingActionButton(
                onClick = {
                    if (!isNavigating) {
                        isNavigating = true
                        onNavigateToAddTemplate()
                    }
                },
                containerColor = Color(0xFF0066FF),
                contentColor = Color.White
            ) {"""
content = content.replace(btn_old, btn_new)

with open('/app/applet/app/src/main/java/com/example/ui/TemplatesScreen.kt', 'w') as f:
    f.write(content)
