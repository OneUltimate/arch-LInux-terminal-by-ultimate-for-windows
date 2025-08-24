
help_database = {
    "powerful": {
        "description": "Включает/выключает режим повышенных прав (доступ к системным командам)",
        "syntax": "powerful [0|1]",
        "examples": [
            "powerful 1 # Включить режим суперпользователя",
            "powerful 0 # Выключить режим (рекомендуется для безопасности)"
        ]
    },
    "welcome": {
        "description": "Управляет показом приветственного окна при запуске",
        "syntax": "welcome window [0|1]",
        "examples": [
            "welcome window 0 # Отключить заставку",
            "welcome window 1 # Включить заставку"
        ]
    },
    "plugin": {
        "description": "Управление плагинами терминала",
        "syntax": "plugin [help|list|reload]",
        "examples": [
            "plugin help # Показать помощь по плагинам",
            "plugin list # Показать список загруженных плагинов",
            "rp # Перезагрузить все плагины (краткая форма)"
        ]
    },
    "env": {
        "description": "Показывает содержимое .env файла с настройками",
        "syntax": "env read",
        "examples": [
            "env read # Показать все переменные окружения"
        ]
    },
    "clear": {
        "description": "Очищает экран терминала",
        "syntax": "clear",
        "examples": [
            "clear # Очистить экран"
        ]
    },
    "datahelp": {
        "description": "Показывает справку по командам",
        "syntax": "datahelp [name]",
        "examples": [
            "data help # Показать все доступные темы",
            "data help powerful # Справка по команде powerful"
        ]
    }
}