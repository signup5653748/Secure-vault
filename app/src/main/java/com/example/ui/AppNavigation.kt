package com.example.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.viewmodel.KeePassViewModel

@Composable
fun AppNavigation(viewModel: KeePassViewModel) {
    val navController = rememberNavController()
    val database by viewModel.database.collectAsState()

    NavHost(navController = navController, startDestination = "auth") {
        composable("auth") {
            if (database != null) {
                // If already unlocked, skip auth screen
                navController.navigate("vault") {
                    popUpTo("auth") { inclusive = true }
                }
            } else {
                AuthScreen(viewModel = viewModel)
            }
        }
        composable("vault") {
            if (database == null) {
                navController.navigate("auth") {
                    popUpTo("vault") { inclusive = true }
                }
            } else {
                VaultScreen(
                    viewModel = viewModel, 
                    onNavigateToView = {
                        navController.navigate("view")
                    }
                )
            }
        }
        composable("view") {
            ViewEntryScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
