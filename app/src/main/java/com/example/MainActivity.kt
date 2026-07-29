package com.example

import android.content.Intent
import android.os.Bundle
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
import com.example.ui.AppNavigation
import com.example.ui.theme.MyApplicationTheme
import com.example.viewmodel.KeePassViewModel

class MainActivity : FragmentActivity() {

  private val viewModel: KeePassViewModel by viewModels()

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
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
          if (viewModel.settings.openFromFileManager.value) {
            intent.data?.let { uri ->
              viewModel.importFile(uri)
            }
          }
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
  }
}
