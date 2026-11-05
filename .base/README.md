# Secure-Vault 🔐

**Secure-Vault** is an offline, privacy-first Android password manager compatible with standard KeePass KDBX format (KDBX 3.1 & 4.x). It gives you complete control over your credentials and sensitive data without relying on proprietary third-party cloud servers.

---

## 🌟 Features

- **Standard KDBX 3.1 & 4.x Compatibility**: Seamlessly open, view, edit, and create KeePass database files using Kotpass.
- **Biometric Authentication**: Fast and secure biometric unlock (Fingerprint / Face Unlock) using Android BiometricPrompt.
- **Zero-Cloud & Local-First**: No external servers, no tracking, and no telemetry. All credentials reside strictly on your local device.
- **Hierarchical Groups & Entries**: Organize accounts with custom groups, tags, notes, and color-coded labels.
- **Built-in Password Generator**: Create cryptographically secure passwords with customizable length, symbols, digits, and character sets.
- **Custom Fields & Templates**: Store custom metadata such as OTP tokens, security questions, URLs, and server keys.
- **Screenshot & Memory Protection**: Sensitive views enforce `FLAG_SECURE` to prevent unauthorized screenshots and app switcher caching.

---

## 🛡️ Security Architecture

Secure-Vault is engineered with zero-trust and defense-in-depth security principles:

1. **Industry-Standard Encryption (AES-256 & ChaCha20)**
   - Database contents are encrypted using AES-256-CBC or ChaCha20 cipher suites through verified KDBX standards.
2. **Key Derivation (Argon2d / Argon2id & AES-KDF)**
   - Master keys are transformed using memory-hard Argon2 or AES-KDF algorithms to resist GPU/ASIC brute-force attacks.
3. **Hardware-Backed Master Key Storage (Android Keystore)**
   - When biometric unlock is enabled, database credentials and master keys are sealed inside the Android Keystore (backed by TEE / StrongBox hardware) using `EncryptedSharedPreferences` and AES-256-GCM.
4. **App Sandboxing & Network Isolation**
   - The app has no internet requirements for local database operations. Cleartext traffic is strictly blocked by network security policy.

---

## 🚀 Building the Project

### Prerequisites
- **Android Studio Ladybug (2024.2.1+)** or higher
- **JDK 17** (configured as your Gradle JDK)
- **Android SDK Platform 36** (minimum API level 24 / Android 7.0+)

### Step-by-Step Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/secure-vault.git
   cd secure-vault
   ```

2. **Open in Android Studio**
   - Launch Android Studio.
   - Select **Open** and choose the `secure-vault` folder.
   - Wait for Gradle sync to complete automatically.

3. **Build via Terminal**
   - **Debug APK**:
     ```bash
     ./gradlew assembleDebug
     ```
     The output APK will be located at:
     `app/build/outputs/apk/debug/app-debug.apk`

   - **Release APK**:
     ```bash
     ./gradlew assembleRelease
     ```
     The minified, production-ready APK will be located at:
     `app/build/outputs/apk/release/app-release.apk`

4. **Automated CI/CD**
   - A GitHub Actions workflow (`.github/workflows/build-apk.yml`) is included. Every push to the `main` branch builds a clean debug APK and uploads it to GitHub Actions Artifacts for instant download.

---

## 📄 License
This project is licensed under the Apache License 2.0.
