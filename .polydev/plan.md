# Fix Workflow Failures in Secure‑Vault

## 1. Change compileSdk from 36 to 34 (or 35 if desired)
* Edit `app/build.gradle.kts` and replace `compileSdk = 36` with `compileSdk = 34`.

## 2. Ensure required GitHub secrets are set
* Add the following secrets in the repository Settings → Secrets and variables → Actions:
  * `KEYSTORE_BASE64` – Base64‑encoded keystore file.
  * `KEYSTORE_PASSWORD` – keystore password.
  * `KEY_PASSWORD` – key alias password.

## 3. (Optional) Add Gradle wrapper files if not present
* If a `gradlew` script or wrapper jar is missing, create the wrapper using a local Gradle installation or copy existing wrapper files from another Android project.

## 4. Verify
* Run the workflow again and check that the build passes and APK is generated.

**These steps will resolve the workflow failures without altering the signing block.**