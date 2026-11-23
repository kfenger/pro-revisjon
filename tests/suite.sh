#!/bin/bash
# Full server-side suite against local Apache. Prints PASS/FAIL lines.
C=/home/claude/qa/c.sh; B=https://pro-revisjon.no; fail=0
rm -rf /var/www/pr && cp -r /home/claude/pro-revisjon/dist /var/www/pr && apache2ctl graceful 2>/dev/null; sleep 1
t(){ # name expected actual
  if [[ "$3" == $2 ]]; then echo "PASS $1"; else echo "FAIL $1 (expected $2, got $3)"; fail=$((fail+1)); fi; }
code(){ $C -o /dev/null -w '%{http_code}' "$@"; }
loc(){ $C -o /dev/null -w '%{http_code} %{redirect_url}' "$@"; }
hdr(){ $C -D - -o /dev/null "$1" | tr -d '\r' | grep -i "^$2:" | cut -d' ' -f2-; }
for p in / /tjenester/ /tjenester/revisjon/ /tjenester/regnskap-og-skatt/ /tjenester/radgivning/ /om-oss/ /ansatte/ /kontakt/ /nyttige-lenker/ /personvern/ /sitemap.xml /robots.txt /favicon.svg /favicon.ico /apple-touch-icon.png /.well-known/security.txt; do t "200 $p" 200 "$(code $B$p)"; done
t "http->https"            "301 https://pro-revisjon.no/" "$(loc http://pro-revisjon.no/)"
t "www->apex"              "301 https://pro-revisjon.no/ansatte/" "$(loc https://www.pro-revisjon.no/ansatte/)"
t "http www->apex"         "301 https://pro-revisjon.no/kontakt/" "$(loc http://www.pro-revisjon.no/kontakt/)"
t "no trailing slash"      "301 https://pro-revisjon.no/tjenester/" "$(loc $B/tjenester)"
t "om-oss no slash"        "301 https://pro-revisjon.no/om-oss/" "$(loc $B/om-oss)"
t "subpage no slash"       "301 https://pro-revisjon.no/tjenester/revisjon/" "$(loc $B/tjenester/revisjon)"
t "testside"               "301 https://pro-revisjon.no/" "$(loc $B/testside/)"
t "query kept on redirect" "301 https://pro-revisjon.no/kontakt/?a=1" "$(loc 'http://pro-revisjon.no/kontakt/?a=1')"
t "open redirect //"       "404*" "$(loc $B//evil.com/)"
t "open redirect http //"  "301 https://pro-revisjon.no/*evil.com*" "$(loc http://pro-revisjon.no//evil.com)"
t "open redirect %2f"      "404*" "$(loc $B/%2F%2Fevil.com)"
t "host header injection"  "301 https://pro-revisjon.no/" "$(env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY curl -s -o /dev/null -w '%{http_code} %{redirect_url}' -H 'Host: evil.com' http://127.0.0.1/)"
for p in wp-login.php xmlrpc.php wp-admin/ wp-content/plugins/x.php wp-includes/js/jquery/jquery.js feed/ files/2012/08/oystein.jpg; do t "410 /$p" 410 "$(code $B/$p)"; done
for p in .htaccess .env .git/config .well-known/ _headers _redirects _astro/ .DS_Store; do t "hidden /$p" "40[34]" "$(code $B/$p)"; done
t "404 status"             404 "$(code $B/finnes-ikke/)"
t "404 branded"            "*Fant ikke siden*" "$($C $B/finnes-ikke/)"
t "dir listing blocked branded" "*Fant ikke siden*" "$($C $B/_astro/)"
for m in POST PUT DELETE PATCH OPTIONS TRACE; do t "method $m" "405" "$(code -X $m $B/)"; done
t "HEAD ok"                200 "$($C -I -o /dev/null -w '%{http_code}' $B/)"
t "charset html"           "text/html; charset=utf-8" "$(hdr $B/ content-type)"
t "charset 404"            "text/html; charset=utf-8" "$(hdr $B/x/ content-type)"
t "woff2 type"             "font/woff2" "$(hdr $B/$(cd /var/www/pr; ls _astro/*.woff2|head -1) content-type)"
t "xml type"               "application/xml*" "$(hdr $B/sitemap.xml content-type)"
t "security.txt type"      "text/plain*" "$(hdr $B/.well-known/security.txt content-type)"
for u in $B/ $B/x/ http://pro-revisjon.no/ $B/wp-login.php $B/_astro/; do
  t "CSP on $u" "default-src 'none'*" "$(hdr $u content-security-policy)"
  t "HSTS on $u" "max-age=31536000" "$(hdr $u strict-transport-security)"
  t "XFO on $u" "DENY" "$(hdr $u x-frame-options)"
  t "nosniff on $u" "nosniff" "$(hdr $u x-content-type-options)"
  t "CORP on $u" "same-origin" "$(hdr $u cross-origin-resource-policy)"
done
t "css immutable"  "*immutable*" "$(hdr $B/$(cd /var/www/pr; ls _astro/*.css) cache-control)"
t "html revalidate" "*must-revalidate*" "$(hdr $B/ cache-control)"
t "gzip"           "gzip" "$($C -H 'Accept-Encoding: gzip' -D - -o /dev/null $B/personvern/ | tr -d '\r' | grep -i '^content-encoding' | cut -d' ' -f2)"
t "no X-Powered-By" "" "$(hdr $B/ x-powered-by)"
t "no reflection"  0 "$($C "$B/?q=%3Cscript%3Ex%3C/script%3E" | grep -c '<script>x')"
t "no reflection 404" 0 "$($C "$B/%3Cscript%3Ex%3C/script%3E/" | grep -c '<script>x')"
echo "== $fail failures"
