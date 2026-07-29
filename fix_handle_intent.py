import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_handle = """  private fun handleIntent(intent: Intent?) {
    if (intent?.action == Intent.ACTION_VIEW) {
      if (viewModel.settings.openFromFileManager.value) {
        intent.data?.let { uri ->
          viewModel.importFile(uri)
        }
      }
    }
  }"""

new_handle = """  private fun handleIntent(intent: Intent?) {
    try {
        if (intent?.action == Intent.ACTION_VIEW) {
          if (viewModel.settings.openFromFileManager.value) {
            intent.data?.let { uri ->
              viewModel.importFile(uri)
            }
          }
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
  }"""

content = content.replace(old_handle, new_handle)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

