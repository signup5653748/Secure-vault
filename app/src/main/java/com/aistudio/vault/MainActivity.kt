package com.aistudio.vault

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.OpenableColumns
import android.widget.Toast
import androidx.fragment.app.FragmentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.aistudio.vault.ui.AppNavigation
import com.aistudio.vault.ui.theme.MyApplicationTheme
import com.aistudio.vault.viewmodel.KeePassViewModel

class MainActivity : FragmentActivity() {

  private val viewModel: KeePassViewModel by viewModels()

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    window.setFlags(
        android.view.WindowManager.LayoutParams.FLAG_SECURE,
        android.view.WindowManager.LayoutParams.FLAG_SECURE
    )
    enableEdgeToEdge()
    
    handleIntent(intent)
    
    setContent {
      val themeColor by viewModel.settings.themeColor.collectAsState()
      val textSizeMultiplier by viewModel.settings.textSizeMultiplier.collectAsState()

      MyApplicationTheme(
        themeColorName = themeColor,
        textSizeMultiplier = textSizeMultiplier
      ) {
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
          androidx.compose.foundation.layout.Box(modifier = Modifier.padding(innerPadding)) {
            AppNavigation(viewModel = viewModel)
          }
        }
      }
    }
  }


  override fun onStop() {
    super.onStop()
    if (viewModel.settings.lockOnBackground.value) {
        viewModel.lockDatabase()
    }
  }

  override fun onNewIntent(intent: Intent) {
    super.onNewIntent(intent)
    handleIntent(intent)
  }

  private fun handleIntent(intent: Intent?) {
    try {
        if (intent?.action == Intent.ACTION_VIEW) {
            intent.data?.let { uri ->
                if (isKdbxFile(uri)) {
                    viewModel.importFile(uri)
                } else {
                    Toast.makeText(this, "Not a KeePass (.kdbx) file", Toast.LENGTH_SHORT).show()
                }
            }
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
  }

  // Validates that the incoming ACTION_VIEW Uri really points at a .kdbx file.
  // File managers embed the name in the path; cloud apps (Drive/Dropbox) send
  // opaque content:// ids with a generic MIME type, so we also resolve the
  // provider's display name before trusting the URI.
  private fun isKdbxFile(uri: Uri): Boolean {
    val path = uri.path
    if (path != null && path.substringAfterLast('/').lowercase().endsWith(".kdbx")) {
        return true
    }
    if (uri.scheme == "content") {
        try {
            contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { cursor ->
                if (cursor.moveToFirst()) {
                    val idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                    if (idx >= 0) {
                        val name = cursor.getString(idx)
                        if (name != null && name.lowercase().endsWith(".kdbx")) return true
                    }
                }
            }
        } catch (_: Exception) {
        }
    }
    return false
  }
}
