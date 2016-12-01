Design:

server: cache01/cache02:
    mode: singleton daemon start.sh
    init:
        wait(sec) before start: hash to smooth upward bandwidth
    start two independent work:
        loop:
            try:
                parse domain.conf
                probe:
                    try:
                        async http request with timeout:
                        measure return time http GET 2M
                        drop return data, donnot use MEM
                    except:
                        set timeout result
                get return results from all ips
                sort ips by timeout
                write to local path of anyhost file
            except:
                /bin/mail alert to XX@kingsoft.com
            sleep 60s
        http server:
            run forever

clients: each caches:
    for ip in servers:
        fetch anyhost to tmp file
        if old != new file && new is valid:
            mv tmp file to anyhost
            reload named
            return

    protocol:
        http server

Server down, deploy mannually:
    cache1/cacche2 all down:
        server to cache03/cache04
        client add cache03/cache04 to config
    cache1/cacche2 up:
        shut down cache03/cache04 agent service
        client remove cache03/cache04 from config

Server recover or startup:
    start daemon
    run background and singleton

Test:
    prepare:
        two relay machines:
            nginx:
                relay static file: 2M
                reload nginx
        probe from remote:
            time curl -H 'Host: fake.com' http://222.222.207.9:8081/2M.dat > 2M.dat
Deploy:
    to severs
        start
    to clients
        start

Get test file:
```

for f in /usr/local/squid/etc/domain.conf /usr/local/squid/etc/origin_domain_ip /var/named/anyhost
remote:
    nc -l 8008 < $f
localhost:
    nc 222.222.207.10 8008 > $f

service named reload
dig domain @127.0.0.1

dd if=/dev/urandom of=/tmp/2M.dat bs=1024k count=2

vim /etc/nginx/nginx.conf

    server {
        listen 8081;
        server_name  fake.com;
        location = /2M.dat {
            root  /tmp/;
        }
    }

nginx -s reload

#test mail alert
echo "test" | mail -s "test ${HOSTNAME}"  wangzhiguo1@kingsoft.com

```
