plugins {
  alias(libs.plugins.android.application) apply true
  alias(libs.plugins.kotlin.compose) apply true
}

android {
  namespace = "com.aistudio.vault"
  compileSdk = 35

  defaultConfig {
    applicationId = "com.aistudio.vault"
    minSdk = 24
    targetSdk = 35
    versionCode = 1
    versionName = "1.0"
  }

  signingConfigs {
    release {
      storeFile = file(System.getenv("RELEASE_STORE_FILE") ?: "release-keystore.jks")
      storePassword = System.getenv("RELEASE_STORE_PASSWORD") ?: ""
      keyAlias = System.getenv("RELEASE_KEY_ALIAS") ?: ""
      keyPassword = System.getenv("RELEASE_KEY_PASSWORD") ?: ""
    }
  }

  buildTypes {
    release {
      signingConfig = signingConfigs.release
      minifyEnabled = true
      proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
    }
    debug {
      minifyEnabled = false
    }
  }

  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
  }

  kotlinOptions {
    jvmTarget = "1.8"
  }

  composeOptions {
    kotlinCompilerExtensionVersion = libs.versions.composeBom.get()
  }

  packaging {
    resources {
      excludes += "/META-INF/{AL2.0,LGPL2.1}"
    }
  }
}

dependencies {
  implementation(platform(libs.androidx.compose.bom))
  implementation(libs.androidx.core.ktx)
  implementation(libs.androidx.appcompat)
  implementation(libs.androidx.compose.ui)
  implementation(libs.androidx.compose.ui.graphics)
  implementation(libs.androidx.compose.ui.tooling)
  implementation(libs.androidx.navigation.compose)
  implementation(libs.androidx.compose.material3)
  implementation(libs.androidx.compose.material.icons.core)
  implementation(libs.androidx.compose.material.icons.extended)
  implementation(libs.coil.compose)
  implementation(libs.kotlinx.coroutines.android)
  implementation(libs.kotlinx.coroutines.core)
  implementation(libs.accompanist.permissions)
  implementation(libs.androidx.camera.camera2)
  implementation(libs.androidx.camera.lifecycle)
  implementation(libs.androidx.camera.view)
  implementation(libs.androidx.camera.core)
  implementation(libs.androidx.datastore.preferences)
  implementation(libs.keepassjava.kdbx)
  implementation(libs.keepassjava.dom)
  implementation(libs.keepassjava.simple)
  implementation(libs.keepassjava.jackson)

  debugImplementation(libs.androidx.compose.ui.tooling.preview)

  androidTestImplementation(libs.androidx.junit)
  androidTestImplementation(libs.androidx.espresso.core)
  androidTestImplementation(libs.androidx.compose.ui.test.manifest)
  androidTestImplementation(libs.androidx.compose.ui.test.junit4)
  debugImplementation(libs.androidx.compose.ui.tooling)
  debugImplementation(libs.androidx.compose.ui.test.junit4)
  testImplementation(libs.junit)
  testImplementation(libs.robolectric)
  testImplementation(libs.roborazzi)
  testImplementation(libs.roborazzi.compose)
  testImplementation(libs.roborazzi.junit.rule)
  testImplementation(libs.kotlinx.coroutines.test)
}
