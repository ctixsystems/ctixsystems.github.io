# Implementing OAuth2 via NGINX and Vouch-Proxy

## Infrastructure
- docker containers
- specific internal network for OAuth exchanges
- Let's encrypt certificate for domain
- TinyCA to issue certificates for the client mTLS
- Azure AD registered application

### Docker network to allow inter-container traffic

Details on docker networking are provided in the [official documentation](https://docs.docker.com/network/) 
and allow inter-container communications using locally scoped hostnames.

For the nginx and vouch proxy integration, I create an *oauthnet* as follows:

```bash
docker network create oauthnet
```

When creating the docker configurations for nginx and vouch, you include the
```--network=oauthnet``` so that these systems are connected. This can be
verified as follows:

```bash
[
    {
        "Name": "oauthnet",
        "Id": "0ec879edc8957c5a7113fcab77dd4ddbfeb0b623ba52b1cc37ed6b297b020663",
        "Created": "2020-08-23T05:04:22.170515647Z",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.19.0.0/16",
                    "Gateway": "172.19.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "88e82b6d2f4677779acad49f17902685ac21ca2904d8887392242eee9c8958cc": {
                "Name": "nginx",
                "EndpointID": "a66b6d8670da1c24e53fdb891bb394749c5b583a487d19c79aff42a0407d3043",
                "MacAddress": "02:42:ac:13:00:02",
                "IPv4Address": "172.19.0.2/16",
                "IPv6Address": ""
            },
            "d4b2b00629178d02e22d6e747473f15bde6d8a42943fff16a418a780348219e8": {
                "Name": "vouch",
                "EndpointID": "00bd246da7c4d85aab14f682e3ed48df37872ad8b3373e6163fd877b27a1dae9",
                "MacAddress": "02:42:ac:13:00:03",
                "IPv4Address": "172.19.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {},
        "Labels": {}
    }
]
```

Looking through the output you can confirm that systems 'vouch' and 'nginx' can
reach each other on addresses 172.19.0.3 and 172.19.0.2 respectively.

### Create docker instances for nginx and vouch oauth2

#### nginx
```bash
docker create --name=nginx --network=oauthnet \
    -e PUID=1000 -e PGID=1000 \
    -e TZ=Australia/Brisbane -p 443:443 -p 80:80 \
    -v /mnt/docker/nginx/config:/config \
    --restart unless-stopped \
    linuxserver/nginx
```

#### vouch
```bash
docker create --name=vouch --network=oauthnet \
    -e PUID=1000 -e PGID=1000 \
    -e TZ=Australia/Brisbane -p 9090:9090  \
    -v /mnt/docker/vouch/config:/config \
    --restart unless-stopped \
    voucher/vouch-proxy
```

## Information flows
- Internet to NGINX (via mTLS)
- NGINX to Vouch (via auth-request)
- Vouch - Identity Provider (AzureAD in my case)

### nginx configuration

### vouch configuration

## Testing
