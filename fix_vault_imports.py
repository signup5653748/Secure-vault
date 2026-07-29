with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# I'll just write a whole new set of imports and replace the top ones
good_imports = """package com.example.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.background
import androidx.compose.ui.graphics.Color
import com.example.viewmodel.KeePassViewModel
import app.keemobile.kotpass.models.Group
import app.keemobile.kotpass.models.Entry
import kotlinx.coroutines.launch
import app.keemobile.kotpass.constants.BasicField
"""

# The file currently starts with "package com.example.ui"
idx = content.find("@OptIn")
if idx == -1:
    idx = content.find("@Composable")

content = good_imports + content[idx:]

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
