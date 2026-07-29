import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

new_state = """    val currentGroup: StateFlow<Group?> = _currentGroup.asStateFlow()

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _searchResults = MutableStateFlow<List<app.keemobile.kotpass.models.Entry>>(emptyList())
    val searchResults: StateFlow<List<app.keemobile.kotpass.models.Entry>> = _searchResults.asStateFlow()

    fun setSearchQuery(query: String) {
        _searchQuery.value = query
        if (query.isEmpty()) {
            _searchResults.value = emptyList()
        } else {
            viewModelScope.launch(Dispatchers.Default) {
                val db = _database.value
                if (db != null) {
                    val allEntries = mutableListOf<app.keemobile.kotpass.models.Entry>()
                    fun traverse(group: app.keemobile.kotpass.models.Group) {
                        allEntries.addAll(group.entries.filter {
                            val title = it[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
                            val user = it[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                            val url = it[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                            title.contains(query, ignoreCase = true) || user.contains(query, ignoreCase = true) || url.contains(query, ignoreCase = true)
                        })
                        group.groups.forEach { traverse(it) }
                    }
                    traverse(db.content.group)
                    _searchResults.value = allEntries
                }
            }
        }
    }
"""

content = content.replace("    val currentGroup: StateFlow<Group?> = _currentGroup.asStateFlow()", new_state)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
