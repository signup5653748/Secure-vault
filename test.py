with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    print("private val _groupStack" in f.read())
