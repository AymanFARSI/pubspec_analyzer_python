import yaml
import requests


def fetch_package_tags(package: str) -> dict:
    url = f'https://pub.dartlang.org/api/packages/{package}/metrics'
    return requests.get(url).json()['score']['tags']


def read_yaml_file(path: str) -> dict:
    with open(path) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            exit(1)


def parse_yaml(content: str) -> dict:
    return yaml.safe_load(content)
