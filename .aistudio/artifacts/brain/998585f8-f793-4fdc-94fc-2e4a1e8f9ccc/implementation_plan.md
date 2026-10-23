# Implementation Plan - TOTP Support Fixes

## Proposed Changes

### 1. `app/build.gradle.kts`
- Update kotpass dependency to `implementation("com.github.keemobile:kotpass:0.13.0")`.
- Ensure Jitpack repository is included in project repositories.
- Add `implementation("dev.turingcomplete:kotlin-onetimepassword:3.0.0")` and `implementation("androidx.security:security-crypto:1.1.0")` / biometric dependencies.

### 2. `app/src/main/java/com/example/viewmodel/KeePassViewModel.kt`
- Add inline `generateTotpCode(otpValue: String?)` function using `TimeBasedOneTimePasswordGenerator` and `Base32` without depending on missing external helper classes.

### 3. `app/src/main/java/com/example/ui/ViewEntryScreen.kt`
- Add the TOTP UI Card with live countdown timer, code display, and copy button linked to `viewModel.generateTotpCode(otpValue)`.

## Verification Plan
- Run `compile_applet` to verify compilation.
- Run `gradle :app:testDebugUnitTest` to verify test suite.
