#!/bin/bash
# Team Agent Tracker - Takım agent'larını izler ve kaydeder
# Kullanım: ./team_tracker.sh [add|remove|list|save]

TEAM_DIR="/home/gokhan/UniverseCreator/.team"
TEAM_FILE="$TEAM_DIR/agents.json"
LOG_FILE="$TEAM_DIR/team.log"

# Dizin yoksa oluştur
mkdir -p "$TEAM_DIR"

# Log fonksiyonu
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Agent ekle
add_agent() {
    local name="$1"
    local type="$2"
    local prompt="$3"

    if [ -z "$name" ]; then
        echo "Kullanım: add <agent_name> <agent_type> [prompt]"
        return 1
    fi

    local agent_json="{\"name\":\"$name\",\"type\":\"$type\",\"prompt\":\"$prompt\",\"added_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"

    if [ -f "$TEAM_FILE" ]; then
        # Mevcut agent'ları al ve yeni agent'ı ekle
        local existing=$(cat "$TEAM_FILE")
        echo "[$existing, $agent_json]" | jq -s '.' > "$TEAM_FILE.tmp"
        mv "$TEAM_FILE.tmp" "$TEAM_FILE"
    else
        echo "[$agent_json]" > "$TEAM_FILE"
    fi

    log "Agent eklendi: $name ($type)"
    echo "Agent eklendi: $name"
}

# Agent kaldır
remove_agent() {
    local name="$1"

    if [ -z "$name" ]; then
        echo "Kullanım: remove <agent_name>"
        return 1
    fi

    if [ -f "$TEAM_FILE" ]; then
        cat "$TEAM_FILE" | jq --arg name "$name" 'map(select(.name != $name))' > "$TEAM_FILE.tmp"
        mv "$TEAM_FILE.tmp" "$TEAM_FILE"
        log "Agent kaldırıldı: $name"
        echo "Agent kaldırıldı: $name"
    else
        echo "Takım dosyası bulunamadı"
    fi
}

# Agent'ları listele
list_agents() {
    if [ -f "$TEAM_FILE" ]; then
        echo "=== Kayıtlı Agent'lar ==="
        cat "$TEAM_FILE" | jq -r '.[] | "  - \(.name) (\(.type)) - eklenme: \(.added_at)"'
    else
        echo "Kayıtlı agent bulunmuyor"
    fi
}

# Team durumunu kaydet (tam takım snapshot'ı)
save_team_snapshot() {
    local snapshot_file="$TEAM_DIR/snapshot_$(date +%Y%m%d_%H%M%S).json"

    if [ -f "$TEAM_FILE" ]; then
        cp "$TEAM_FILE" "$snapshot_file"
        log "Takım snapshot'ı kaydedildi: $snapshot_file"
        echo "Snapshot kaydedildi: $snapshot_file"
    else
        echo "Kaydedilecek takım bulunmuyor"
    fi
}

# En son snapshot'ı yükle
load_latest_snapshot() {
    local latest=$(ls -t "$TEAM_DIR"/snapshot_*.json 2>/dev/null | head -1)

    if [ -n "$latest" ]; then
        cp "$latest" "$TEAM_FILE"
        log "En son snapshot yüklendi: $latest"
        echo "Yüklendi: $latest"
    else
        echo "Snapshot bulunamadı"
    fi
}

# Ana menü
case "$1" in
    add)
        add_agent "$2" "$3" "$4"
        ;;
    remove)
        remove_agent "$2"
        ;;
    list)
        list_agents
        ;;
    save)
        save_team_snapshot
        ;;
    load)
        load_latest_snapshot
        ;;
    *)
        echo "Team Agent Tracker"
        echo "Kullanım: $0 <komut> [argümanlar]"
        echo ""
        echo "Komutlar:"
        echo "  add <isim> <tip> [prompt]  - Yeni agent ekle"
        echo "  remove <isim>              - Agent'ı kaldır"
        echo "  list                      - Tüm agent'ları listele"
        echo "  save                      - Snapshot kaydet"
        echo "  load                      - En son snapshot'ı yükle"
        ;;
esac