import re

with open('/app/applet/app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

content = content.replace('android:taskAffinity=".SecureVault"', 'android:taskAffinity=".SecureVault"\n            android:clearTaskOnLaunch="true"')

with open('/app/applet/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)

