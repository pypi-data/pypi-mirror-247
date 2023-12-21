# ThingsPro Edge Function SDK

ThingsPro Edge Function SDK provides several APIs to interact with ThingsPro Edge features.

- Tag (v1)
  - PubSub
  - Direct Access
- Http Server (v1)
  - Get
  - Post
  - Put
  - Delete

Besides, SDK is tested with Python3.9, theoretically compatible with all other modules which you can refer to [Python3.9 official website](https://docs.python.org/3.9/library/index.html). Python3.6 is no longer in the support list.

# Release Note
## 2023-12-21 V1.2.6
### Changes:
- chore: upgrade to python3.9

## 2023-05-03 V1.2.5
### Bug Fix:
- fix: http function missing essential module folder

## 2023-04-26 V1.2.4
### Features:
- feat: support unsubscribe all

## 2021-07-26 V1.2.3
### Bug Fix:
- fix: can't receive messages after tag_v1 subscribe callback exception

## 2021-07-23 V1.2.2
### Bug Fix:
- fix: tag_v1 subscribe init always run into exception
