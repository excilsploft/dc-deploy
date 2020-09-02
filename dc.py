#!/usr/bin/env python

import argparse
import yaml
import sys


def main(args):
    """Write the docker compose yaml"""

    labels = {}
    labels["traefik.enable"] = "true"
    labels["traefik.http.routers.link-checker.rule"] = "Host(`{0}`)".format(args.url)
    labels["traefik.http.routers.link-checker.entrypoints"] = "web"
    labels["traefik.http.routers.link-checker.middlewares"] = "https-only"
    labels["traefik.http.middlewares.https-only.redirectscheme.scheme"] = "https"
    labels["traefik.http.middlewares.https-only.redirectscheme.permanent"] = "true"
    labels["traefik.http.middlewares.https-only.redirectscheme.port"] = "443"
    labels["traefik.http.routers.link-checker-secure.rule"] = "Host(`{0}`)".format(args.url)
    labels["traefik.http.routers.link-checker-secure.entrypoints"] = "websecure"
    labels["traefik.http.routers.link-checker-secure.tls"] = "true"

    volumes = ["{0}:/usr/share/nginx/html".format(args.mountdir)]

    dc = {"version": "3.7"}
    dc["services"] = {
            "site": {
                "image":  'nginx:1.17.9-alpine',
                "networks": ["traefik"],
                "expose": [80],
                "labels": labels,
                "hostname": args.hostname,
                "volumes": volumes}}

    dc["networks"] = {"traefik": {"external": True}}


    yaml_string = yaml.dump(dc)

    try:
        with open(args.filename, 'w') as file_out:
            file_out.write(yaml_string)
    except IOError:
        sys.stderr.write("Error Writing file {0}\n".format(args.filename))
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="write docker-compose.yml")
    PARSER.add_argument('-f', '--filename', type=str,
                        default='./docker-compose.yml',
                        help='the name of the docker-compose.yml',
                        required=True)
    PARSER.add_argument('-m', '--mountdir', type=str,
                        help='the directory to mount to the container',
                        required=True)
    PARSER.add_argument('-u', '--url', type=str,
                        help='the url for the website',
                        required=True)
    PARSER.add_argument('-hn', '--hostname', type=str,
                        help='the hostname to pass to the compose file',
                        required=True)

    ARGS = PARSER.parse_args()
    main(ARGS)


