import os, re, sys

path = os.environ.get("SIGNING_SRC", "")
if not path or not os.path.isfile(path):
    print("::warning::No signing source file detected - skipping signing config enforcement.")
    sys.exit(0)

store_pass_var = os.environ.get("STORE_PASS_VAR") or "STORE_PASSWORD"
key_pass_var = os.environ.get("KEY_PASS_VAR") or "KEY_PASSWORD"

with open(path, "r") as f:
    content = f.read()

canonical = '''  signingConfigs {
    create("release") {
      val keystorePath = System.getenv("KEYSTORE_PATH") ?: "${rootDir}/my-upload-key.jks"
      storeFile = file(keystorePath)
      storePassword = System.getenv("''' + store_pass_var + '''")
      val isReleaseBuild = gradle.startParameter.taskNames.any { it.contains("Release", ignoreCase = true) }
      val alias = System.getenv("KEY_ALIAS")
      if (isReleaseBuild && alias.isNullOrEmpty()) {
        throw GradleException("KEY_ALIAS environment variable is not set")
      }
      keyAlias = alias ?: ""
      keyPassword = System.getenv("''' + key_pass_var + '''")
    }
    create("debugConfig") {
      storeFile = file("${rootDir}/debug.keystore")
      storePassword = "android"
      keyAlias = "androiddebugkey"
      keyPassword = "android"
    }
  }
'''

idx = content.find("signingConfigs")
if idx == -1:
    m = re.search(r"android\s*\{", content)
    if not m:
        print("::error::No android {} block found - cannot insert signingConfigs.")
        sys.exit(1)
    insert_at = m.end()
    new_content = content[:insert_at] + "\n" + canonical + content[insert_at:]
    print("No existing signingConfigs block found - inserted canonical block.")
else:
    brace_start = content.find("{", idx)
    depth = 0
    i = brace_start
    while i < len(content):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    block_end = i + 1
    line_start = content.rfind("\n", 0, idx) + 1
    tail = content[block_end:]
    if tail.startswith("\n"):
        tail = tail[1:]
    new_content = content[:line_start] + canonical + tail
    print("Existing signingConfigs block replaced with canonical version.")

with open(path, "w") as f:
    f.write(new_content)
