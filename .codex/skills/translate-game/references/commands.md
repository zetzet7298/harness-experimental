# Command Runbook

## 1) Giải nén + cài dependency
```bash
mkdir -p /var/www/vhst/tools/gpttranslator
unzip ~/Downloads/source.zip -d /var/www/vhst/tools/gpttranslator

cd /var/www/vhst/tools/gpttranslator/source
npm install

cd /var/www/vhst/tools/gpttranslator/source/server
npm install
```

## 2) Cấu hình server `.env`
```env
PORT=7770
PUBLIC_BASE_URL=http://127.0.0.1:7770
MONGODB_URI=mongodb://<user>:<pass>@127.0.0.1:27017/gpttranslator?authSource=admin
JWT_SECRET=<long-random-secret>
UPSTREAM_BASE_URL=http://127.0.0.1:20128/v1
UPSTREAM_API_KEY=<upstream-key>
UPSTREAM_MODEL=cx/gpt-5.4-mini
ONE_ACCOUNT_PER_IP=false
```

## 3) Start/stop server nền
```bash
# start
cd /var/www/vhst/tools/gpttranslator/source/server
node index.js > /tmp/gpttranslator-server.log 2>&1 &
echo $!

# health
curl -sS http://127.0.0.1:7770/health

# stop
kill <PID>
```

## 4) Smoke test register + lấy key + models
```bash
EMAIL="tester_$(date +%s)@example.com"
PASS='Test@123456'

curl -sS -X POST http://127.0.0.1:7770/api/auth/register \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}"

TOKEN=$(curl -sS -X POST http://127.0.0.1:7770/api/auth/login \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" | jq -r '.token')

curl -sS http://127.0.0.1:7770/api/auth/cli-key \
  -H "Authorization: Bearer $TOKEN"

curl -sS http://127.0.0.1:7770/v1/models \
  -H "Authorization: Bearer $TOKEN"
```

## 5) Test dịch trực tiếp qua API
```bash
cat >/tmp/sample-input.txt <<'EOF'
江湖侠客，欢迎来到新手村。
EOF

curl -sS -X POST http://127.0.0.1:7770/api/cli/translate \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@/tmp/sample-input.txt" \
  -F 'lang_input=zh' \
  -F 'lang_output=vi' \
  -F 'context=Game dialogue, keep placeholders unchanged'
```

## 6) Test không chạm source theo từng folder
```bash
WORK=/tmp/gpttranslator-folder-test-$(date +%s)
mkdir -p "$WORK/input" "$WORK/output"

# copy file mẫu đại diện (ví dụ)
cp /var/www/vhst/gamecenter/wwwroot/config/paklist.ini "$WORK/input/"
cp /var/www/vhst/gamecenter/Gateway/bin/systemmsg.ini "$WORK/input/"
cp /var/www/vhst/gamecenter/gameserver/script/gonggao.lua "$WORK/input/"

cat >"$WORK/config.env" <<'EOF'
Path_Input=./input
path_output=./output
lang_input=zh
lang_output=vi
context=Game content, keep IDs/placeholders/format unchanged
scan_lines=30
batch_segments=8
parallel_requests=1
EOF

cd "$WORK"
gpt translate
ls -la "$WORK/output"
```
