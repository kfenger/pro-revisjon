#!/bin/bash
# curl against local Apache only (never the real site)
exec env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u all_proxy curl -k -s \
 --resolve pro-revisjon.no:443:127.0.0.1 --resolve www.pro-revisjon.no:443:127.0.0.1 \
 --resolve pro-revisjon.no:80:127.0.0.1 --resolve www.pro-revisjon.no:80:127.0.0.1 "$@"
