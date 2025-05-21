# Правило Автоматического Сохранения Логов

## 🚨 Триггер: Контекст > 85%

**Когда контекст заполнен более чем на 85%, автоматически выполнить:**

### 1. Сохранение Tmux Логов
```bash
# Сохранить текущую сессию
tmux capture-pane -t 0 -p > "/mnt/c/Desktop/work for claude/logs_organized/auto_tmux_$(date +%Y%m%d_%H%M%S).log"

# Сохранить полную историю
tmux capture-pane -t 0 -S -2000 -p > "/mnt/c/Desktop/work for claude/logs_organized/auto_tmux_full_$(date +%Y%m%d_%H%M%S).log"
```

### 2. Сохранение Терминала
```bash
# Сохранить bash историю
history > "/mnt/c/Desktop/work for claude/logs_organized/auto_bash_history_$(date +%Y%m%d_%H%M%S).log"

# Сохранить переменные окружения
env > "/mnt/c/Desktop/work for claude/logs_organized/auto_env_$(date +%Y%m%d_%H%M%S).log"

# Сохранить активные процессы
ps aux > "/mnt/c/Desktop/work for claude/logs_organized/auto_processes_$(date +%Y%m%d_%H%M%S).log"
```

### 3. Создание Checkpoint Файла  
```bash
echo "=== AUTO CHECKPOINT - CONTEXT >85% ===" > "/mnt/c/Desktop/work for claude/logs_organized/auto_checkpoint_$(date +%Y%m%d_%H%M%S).log"
echo "Date: $(date)" >> "/mnt/c/Desktop/work for claude/logs_organized/auto_checkpoint_$(date +%Y%m%d_%H%M%S).log"
echo "Working Directory: $(pwd)" >> "/mnt/c/Desktop/work for claude/logs_organized/auto_checkpoint_$(date +%Y%m%d_%H%M%S).log"
echo "Current Project: $(basename $(pwd))" >> "/mnt/c/Desktop/work for claude/logs_organized/auto_checkpoint_$(date +%Y%m%d_%H%M%S).log"
echo "Python Environment: $VIRTUAL_ENV" >> "/mnt/c/Desktop/work for claude/logs_organized/auto_checkpoint_$(date +%Y%m%d_%H%M%S).log"
```

### 4. Автоскрипт для Быстрого Выполнения
```bash
#!/bin/bash
# AUTO_SAVE_LOGS.sh - Выполнить при контексте >85%

LOG_DIR="/mnt/c/Desktop/work for claude/logs_organized"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🚨 CONTEXT >85% - AUTO SAVING LOGS..."

# Tmux logs
tmux capture-pane -t 0 -p > "$LOG_DIR/auto_tmux_$TIMESTAMP.log"
tmux capture-pane -t 0 -S -2000 -p > "$LOG_DIR/auto_tmux_full_$TIMESTAMP.log"

# Terminal logs  
history > "$LOG_DIR/auto_bash_history_$TIMESTAMP.log"
env > "$LOG_DIR/auto_env_$TIMESTAMP.log"
ps aux > "$LOG_DIR/auto_processes_$TIMESTAMP.log"

# Checkpoint
echo "=== AUTO CHECKPOINT - CONTEXT >85% ===" > "$LOG_DIR/auto_checkpoint_$TIMESTAMP.log"
echo "Date: $(date)" >> "$LOG_DIR/auto_checkpoint_$TIMESTAMP.log"
echo "Working Directory: $(pwd)" >> "$LOG_DIR/auto_checkpoint_$TIMESTAMP.log"
echo "Current Project: $(basename $(pwd))" >> "$LOG_DIR/auto_checkpoint_$TIMESTAMP.log"
echo "Python Environment: $VIRTUAL_ENV" >> "$LOG_DIR/auto_checkpoint_$TIMESTAMP.log"

echo "✅ Logs saved with timestamp: $TIMESTAMP"
ls -la "$LOG_DIR/auto_*$TIMESTAMP*"
```

## 📋 Применение Правила

**Это правило применяется автоматически когда:**
- Контекст Claude достигает 85%+ заполнения  
- Перед началом новой крупной задачи
- При переключении между проектами
- При возникновении ошибок требующих перезапуска

## 🎯 Цель
Обеспечить непрерывность работы и сохранность всей информации при достижении лимитов контекста.