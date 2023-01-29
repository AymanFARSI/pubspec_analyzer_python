import pandas as pd
from src.pubspec import *


def packages_to_df(dependencies: dict) -> pd.DataFrame:
    df = pd.DataFrame(columns=['package', 'android', 'ios',
                               'linux', 'windows', 'macos', 'web'],
                      dtype='bool')
    for package in list(dependencies):
        if package == 'flutter':
            continue
        tags = fetch_package_tags(package)
        metrics = {
            'package': [package],
            'android': [False],
            'ios': [False],
            'linux': [False],
            'windows': [False],
            'macos': [False],
            'web': [False],
        }
        for tag in tags:
            if 'platform' in tag:
                metrics[tag.split(':')[1]] = [True]
        df = pd.concat([df, pd.DataFrame.from_dict(metrics)])
    return df
