import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("import androidx.activity.ComponentActivity", "import androidx.appcompat.app.AppCompatActivity")
content = content.replace("class MainActivity : ComponentActivity()", "class MainActivity : AppCompatActivity()")

new_lifecycle = """
  override fun onStop() {
    super.onStop()
    if (viewModel.settings.lockOnBackground.value) {
        viewModel.lockDatabase()
    }
  }
"""

content = content.replace("  override fun onNewIntent", new_lifecycle + "\n  override fun onNewIntent")

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
