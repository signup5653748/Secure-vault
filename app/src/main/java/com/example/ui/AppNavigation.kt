package com.example.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
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
            LaunchedEffect(database) {
                if (database != null) {
                    navController.navigate("vault") {
                        popUpTo("auth") { inclusive = true }
                    }
                }
            }
            if (database == null) {
                AuthScreen(viewModel = viewModel)
            }
        }
        composable("vault") {
            LaunchedEffect(database) {
                if (database == null) {
                    navController.navigate("auth") {
                        popUpTo("vault") { inclusive = true }
                    }
                }
            }
            if (database != null) {
                VaultScreen(
                    viewModel = viewModel, 
                    onNavigateToView = {
                        navController.navigate("view")
                    },
                    onNavigateToSettings = {
                        navController.navigate("settings")
                    }
                )
            }
        }
        composable("view") {
            if (database != null) {
                ViewEntryScreen(
                    viewModel = viewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            } else {
                LaunchedEffect(Unit) {
                    navController.navigate("auth") {
                        popUpTo(0)
                    }
                }
            }
        }
        composable("settings") {
            SettingsScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
