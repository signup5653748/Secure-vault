import re

with open('/app/applet/app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

start_idx = content.find('<intent-filter>', content.find('android.intent.action.VIEW'))
end_idx = content.rfind('</intent-filter>') + len('</intent-filter>')

new_filters = """            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="file" />
                <data android:scheme="content" />
                <data android:mimeType="application/x-keepass2" />
                <data android:mimeType="application/keepass" />
                <data android:mimeType="application/x-keepass" />
                <data android:mimeType="application/x-keepass-databases" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="file" />
                <data android:scheme="content" />
                <data android:host="*" />
                <data android:mimeType="*/*" />
                <data android:pathPattern=".*\\\\.kdbx" />
                <data android:pathPattern=".*\\\\..*\\\\.kdbx" />
                <data android:pathPattern=".*\\\\..*\\\\..*\\\\.kdbx" />
                <data android:pathPattern=".*\\\\..*\\\\..*\\\\..*\\\\.kdbx" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="file" />
                <data android:scheme="content" />
                <data android:host="*" />
                <data android:mimeType="application/octet-stream" />
                <data android:pathPattern=".*\\\\.kdbx" />
                <data android:pathPattern=".*\\\\..*\\\\.kdbx" />
                <data android:pathPattern=".*\\\\..*\\\\..*\\\\.kdbx" />
                <data android:pathPattern=".*\\\\..*\\\\..*\\\\..*\\\\.kdbx" />
            </intent-filter>"""

content = content[:start_idx] + new_filters + content[end_idx:]

with open('/app/applet/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
