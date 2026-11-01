#!/usr/bin/env bash
# BSM Mekanik — VDS kurulum betiği (Ubuntu / Debian, nginx)
#
# Kullanım (sunucuda root olarak):
#   Repo herkese açıksa:
#     curl -fsSL https://raw.githubusercontent.com/emremuslu42-hub/recep-berk-can/claude/bold-edison-kwvvmm/deploy/setup-server.sh -o setup-server.sh
#   Repo gizliyse: GitHub'da bu dosyayı açıp "Raw" düğmesinin verdiği (token'lı) adresi curl ile indirin.
#   Gizli repoda betik bir deploy key (yalnızca okuma) üretir ve GitHub'a eklemenizi ister.
#
#   bash setup-server.sh demo      # yalnızca bsmmekanik.mesakyazilim.com
#   bash setup-server.sh domains   # alan adları sunucuya yönlendikten sonra: www/çıplak bsmmekanik.com + bsmmechanical.com
#
# Betik tekrar çalıştırılabilir; her seferinde siteyi günceller, ayarları yeniden yazar.

set -euo pipefail

MODE="${1:-demo}"
REPO_HTTPS="https://github.com/emremuslu42-hub/recep-berk-can.git"
REPO_SSH="git@github.com:emremuslu42-hub/recep-berk-can.git"
DEPLOY_KEY="/root/.ssh/bsmmekanik_deploy"
BRANCH="claude/bold-edison-kwvvmm"
APP_DIR="/opt/bsmmekanik"
WEB_ROOT="/var/www/bsmmekanik"
SITE_CONF="/etc/nginx/sites-available/bsmmekanik"
DEMO_HOST="bsmmekanik.mesakyazilim.com"
DOMAIN_HOSTS="www.bsmmekanik.com bsmmekanik.com www.bsmmechanical.com bsmmechanical.com"
CERT_EMAIL="${CERT_EMAIL:-mert@bsmmechanical.com}"

say() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
die() { printf '\n\033[1;31mHATA: %s\033[0m\n' "$*" >&2; exit 1; }

[ "$(id -u)" -eq 0 ] || die "root olarak çalıştırın (sudo bash setup-server.sh $MODE)"
[ "$MODE" = "demo" ] || [ "$MODE" = "domains" ] || die "kullanım: bash setup-server.sh demo|domains"
command -v apt-get >/dev/null || die "Bu betik Ubuntu/Debian içindir."

# 80 numaralı portu nginx dışında bir şey (Apache, panel vb.) kullanıyorsa dur
if command -v ss >/dev/null; then
  busy=$(ss -ltnp 2>/dev/null | awk '$4 ~ /:80$/' | grep -v nginx || true)
  [ -z "$busy" ] || die "80 portu başka bir yazılım tarafından kullanılıyor:
$busy
Sunucuda Apache/panel varsa deploy/.htaccess dosyasını kullanın ya da bana yazın."
fi

say "Paketler kuruluyor (nginx, certbot, git)"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq nginx certbot python3-certbot-nginx git curl dnsutils >/dev/null

say "Site dosyaları GitHub'dan alınıyor"
if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" fetch -q --depth 1 origin "$BRANCH"
  git -C "$APP_DIR" reset -q --hard "origin/$BRANCH"
elif GIT_TERMINAL_PROMPT=0 git ls-remote -q "$REPO_HTTPS" >/dev/null 2>&1; then
  git clone -q --depth 1 --branch "$BRANCH" "$REPO_HTTPS" "$APP_DIR"
else
  # Gizli repo: yalnızca okuma yetkili deploy key
  mkdir -p /root/.ssh && chmod 700 /root/.ssh
  [ -f "$DEPLOY_KEY" ] || ssh-keygen -q -t ed25519 -N "" -C "bsmmekanik-vds" -f "$DEPLOY_KEY"
  SSH_CMD="ssh -i $DEPLOY_KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
  until GIT_SSH_COMMAND="$SSH_CMD" git ls-remote -q "$REPO_SSH" >/dev/null 2>&1; do
    printf '\n\033[1;33mRepo gizli. Aşağıdaki anahtarı GitHub'"'"'a ekleyin:\033[0m\n'
    echo "  https://github.com/emremuslu42-hub/recep-berk-can/settings/keys → Add deploy key"
    echo "  Title: bsmmekanik-vds   ·   \"Allow write access\" İŞARETLEMEYİN"
    echo
    cat "$DEPLOY_KEY.pub"
    echo
    read -r -p "Ekledikten sonra Enter'a basın (çıkmak için Ctrl+C)... " _
  done
  GIT_SSH_COMMAND="$SSH_CMD" git clone -q --depth 1 --branch "$BRANCH" "$REPO_SSH" "$APP_DIR"
  git -C "$APP_DIR" config core.sshCommand "$SSH_CMD"
fi
# nginx (www-data) dosyaları okuyabilsin; umask'ı sıkı sunucular için
chmod 755 "$APP_DIR"
chmod -R a+rX "$APP_DIR/public"
mkdir -p "$(dirname "$WEB_ROOT")"
if [ -e "$WEB_ROOT" ] && [ ! -L "$WEB_ROOT" ]; then
  mv "$WEB_ROOT" "$WEB_ROOT.yedek-$(date +%Y%m%d%H%M%S)"
fi
ln -sfn "$APP_DIR/public" "$WEB_ROOT"

say "nginx ayarı yazılıyor"
cp "$APP_DIR/deploy/nginx.conf" "$SITE_CONF"
# IPv6 kapalı sunucularda [::] dinleme satırı nginx'i durdurur
[ -s /proc/net/if_inet6 ] || sed -i '/listen \[::\]:80;/d' "$SITE_CONF"
ln -sfn "$SITE_CONF" /etc/nginx/sites-enabled/bsmmekanik
grep -q "webmanifest" /etc/nginx/mime.types || sed -i 's#^}#    application/manifest+json webmanifest;\n}#' /etc/nginx/mime.types
nginx -t
systemctl enable -q nginx
systemctl reload nginx || systemctl restart nginx

if command -v ufw >/dev/null && ufw status | grep -q "Status: active"; then
  say "Güvenlik duvarında 80/443 açılıyor"
  ufw allow 'Nginx Full' >/dev/null
fi

say "Otomatik güncelleme (5 dakikada bir GitHub'dan çeker)"
cat > /usr/local/bin/bsmmekanik-update <<EOF
#!/usr/bin/env bash
set -e
cd "$APP_DIR"
git fetch -q --depth 1 origin "$BRANCH"
if [ "\$(git rev-parse HEAD)" != "\$(git rev-parse "origin/$BRANCH")" ]; then
  git reset -q --hard "origin/$BRANCH"
  chmod -R a+rX public
  if ! cmp -s deploy/nginx.conf "$SITE_CONF"; then
    cp deploy/nginx.conf "$SITE_CONF.new"
    # certbot'un eklediği SSL satırlarını korumak için ayar dosyası otomatik değiştirilmez
    echo "nginx.conf değişti; inceleyip elle güncelleyin: $SITE_CONF.new" | logger -t bsmmekanik
  fi
  logger -t bsmmekanik "site güncellendi: \$(git rev-parse --short HEAD)"
fi
EOF
chmod +x /usr/local/bin/bsmmekanik-update
echo "*/5 * * * * root /usr/local/bin/bsmmekanik-update" > /etc/cron.d/bsmmekanik
chmod 644 /etc/cron.d/bsmmekanik

# SSL: yalnızca DNS'i bu sunucuyu gösteren adlar için sertifika alınır
MYIP=$(curl -fsS4 https://api.ipify.org || true)
[ "$MODE" = "demo" ] && HOSTS="$DEMO_HOST" || HOSTS="$DEMO_HOST $DOMAIN_HOSTS"
ready=()
say "DNS kontrolü (sunucu IP: ${MYIP:-bilinmiyor})"
for h in $HOSTS; do
  ips=$(dig +short A "$h" @1.1.1.1 2>/dev/null | grep -E '^[0-9.]+$' | tr '\n' ' ' || true)
  if [ -n "$MYIP" ] && echo " $ips" | grep -q " $MYIP"; then
    echo "  ✔ $h → $ips"
    ready+=("-d" "$h")
  else
    echo "  ✘ $h → ${ips:-kayıt yok} (henüz bu sunucuyu göstermiyor, atlandı)"
  fi
done

if [ ${#ready[@]} -gt 0 ]; then
  say "SSL sertifikası alınıyor (Let's Encrypt)"
  certbot --nginx --non-interactive --agree-tos --redirect --expand -m "$CERT_EMAIL" "${ready[@]}"
  systemctl reload nginx
else
  echo "SSL atlandı: hiçbir ad bu sunucuyu göstermiyor. DNS kaydını ekleyip betiği yeniden çalıştırın."
fi

say "Bitti"
echo "Demo:   https://$DEMO_HOST"
[ "$MODE" = "domains" ] && echo "Siteler: https://www.bsmmekanik.com  ·  https://www.bsmmechanical.com/en/"
echo "Güncelleme kaydı: journalctl -t bsmmekanik   ·   Elle güncelle: bsmmekanik-update"
