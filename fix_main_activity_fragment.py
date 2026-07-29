import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("import androidx.appcompat.app.AppCompatActivity", "import androidx.fragment.app.FragmentActivity")
content = content.replace("class MainActivity : AppCompatActivity()", "class MainActivity : FragmentActivity()")

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
