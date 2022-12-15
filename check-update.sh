#!/bin/sh
curl "https://github.com/BelledonneCommunications/postquantumcryptoengine/tags" 2>/dev/null |grep "tag/" |sed -e 's,.*tag/,,;s,\".*,,;' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1
curl -s "https://gitlab.linphone.org/BC/public/postquantumcryptoengine/-/tags"  |grep "tags/" |sed -e 's,.*tags/,,;s,\".*,,;' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1

