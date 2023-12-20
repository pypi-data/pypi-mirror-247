import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import List

import yaml
from shopcloud_secrethub import SecretHub

from . import exceptions, file_content, helpers


class Config:
    FILENAME = '.eventbus.yaml'
    VERSION = 'V1'

    def __init__(self):
        self.version = None
        self.project = None
        self.region = None
        self.app_endpoint = None
        self.secrethub_endpoint_user = None
        self.secrethub_endpoint_pwd = None

    def load(self) -> bool:
        if not Path(Config.FILENAME).exists():
            return False
        with open(Config.FILENAME) as f:
            data = yaml.safe_load(f)
            self.project = data.get('project')
            self.region = data.get('region')
            self.app_endpoint = data.get('app_endpoint')
            self.secrethub_endpoint_user = data.get('secrethub_endpoint_user')
            self.secrethub_endpoint_pwd = data.get('secrethub_endpoint_pwd')
            self.version = data.get('version', '')

        if str(self.version).strip() != self.VERSION:
            raise exceptions.ConfigInvalidVersion()

        return True

    def save(self):
        with open(Config.FILENAME, 'w') as f:
            yaml.dump(self.dict(), f)

    def dict(self):
        return {
            'project': self.project,
            'region': self.region,
            'app_endpoint': self.app_endpoint,
            'secrethub_endpoint_user': self.secrethub_endpoint_user,
            'secrethub_endpoint_pwd': self.secrethub_endpoint_pwd,
            'version': self.VERSION,
        }


class Step:
    def __init__(self):
        pass

    def run(self, config: Config, simulate: bool = False):
        raise NotImplementedError()


class StepDeleteDir(Step):
    def __init__(self, dir: str):
        self.dir = dir

    def run(self, config: Config, simulate: bool = False):
        if not Path(self.dir).exists():
            return None
        print('+ Deleting .eventbus directory')
        shutil.rmtree('.eventbus')


class StepCreatDir(Step):
    def __init__(self, dir: str):
        self.dir = dir

    def run(self, config: Config, simulate: bool = False):
        print('+ Create .eventbus directory')
        os.mkdir(self.dir)


class StepWriteFileContent(Step):
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content

    def run(self, config: Config, simulate: bool = False):
        print(f'+ Create .eventbus/{self.filename} file')
        with open(f'.eventbus/{self.filename}', 'w') as f:
            f.write(self.content)


class StepCommand(Step):
    def __init__(self, command: List[str], **kwargs):
        self.command = command
        self.work_dir = kwargs.get('work_dir')

    def run(self, config: Config, simulate: bool = False):
        print('+ Run command:')
        print(" ".join(self.command))
        if not simulate:
            p = subprocess.run(self.command, stdout=subprocess.PIPE, cwd=self.work_dir)
            if p.returncode != 0:
                raise exceptions.CommandError('command not success')


class Manager:
    def __init__(self, config: Config, steps: list, **kwargs):
        self.config = config
        self.steps = steps
        self.simulate = kwargs.get('simulate', False)

    def run(self) -> int:
        if self.simulate:
            print(helpers.bcolors.WARNING + '+ Simulate' + helpers.bcolors.ENDC)
        for step in self.steps:
            try:
                step.run(self.config, self.simulate)
            except Exception as e:
                print(helpers.bcolors.FAIL + f'ERROR: {e}' + helpers.bcolors.ENDC)
                return 1
        return 0


def main(args) -> int:
    if hasattr(args, 'secrethub_token'):
        hub = SecretHub(user_app="eventbus-cli", api_token=args.secrethub_token)
    else:
        hub = SecretHub(user_app="eventbus-cli")

    if hasattr(args, 'debug') and args.debug:
        print(args)

    config = Config()

    if hasattr(args, 'which'):
        if args.which == 'deploy':
            try:
                is_loaded = config.load()
            except exceptions.ConfigInvalidVersion:
                print(
                    helpers.bcolors.FAIL
                    + 'Config file is not compatible with this version. Please run `init` again.'
                    + helpers.bcolors.ENDC
                )
                return 1

            if not is_loaded:
                print('No config file found. Please run `init` first.')
                return 1

            memory_limit = "256MB"
            runtime = "python312"

            dir = '.eventbus'
            manager = Manager(config, [
                StepDeleteDir(dir),
                StepCreatDir(dir),
                StepWriteFileContent('main.py', file_content.main_py),
                StepWriteFileContent('requirements.txt', file_content.requirements_txt),
                StepWriteFileContent('.env.yaml', yaml.dump({
                    'API_AUTH_USER': helpers.fetch_secret(hub, config.secrethub_endpoint_user, simulate=args.simulate),
                    'API_AUTH_PWD': helpers.fetch_secret(hub, config.secrethub_endpoint_pwd, simulate=args.simulate),
                    'API_ENDPOINT': config.app_endpoint,
                    'TASK_PROJECT': config.project,
                    'TASK_LOCATION': config.region,
                })),
                StepCommand(
                    shlex.split(
                        f"gcloud functions deploy --project='{config.project}' eventbus --memory='{memory_limit}' --runtime {runtime} --trigger-topic='events' --allow-unauthenticated --entry-point='main_pub_sub' --region='{config.region}' --env-vars-file='.env.yaml' "
                    ),
                    work_dir=dir,
                ),
            ], simulate=args.simulate)
            rc = manager.run()
            if rc != 0:
                return rc

            print(helpers.bcolors.OKGREEN + 'Deployed eventbus' + helpers.bcolors.ENDC)
            print('Manuel Steps:')
            print('- Generate the log event senke with PubSub Topic')
            return 0
        elif args.which == 'init':

            print('# GCP Config')
            config.project = args.project or helpers.ask_for('Project')
            config.region = args.region or helpers.ask_for('Region', 'europe-west3')
            config.app_endpoint = args.app_endpoint or helpers.ask_for(
                'App endpoint',
                f'https://{config.project}.ey.r.appspot.com'
            )

            if args.secrethub_endpoint_user is None and args.secrethub_endpoint_pwd is None:
                print('# Secrethub Config')
                secrethub_namesapce = helpers.ask_for('Namespace', 'talk-point')
                secrethub_repo = helpers.ask_for('Repo')

                config.secrethub_endpoint_user = f'{secrethub_namesapce}/{secrethub_repo}/production/evenbus-user'
                config.secrethub_endpoint_pwd = f'{secrethub_namesapce}/{secrethub_repo}/production/evenbus-pwd'

                if helpers.ask_for_yes_no('Create items on secrethub?'):
                    username = 'api-eventbus'
                    pwd = helpers.generate_safe_password_32()
                    hub.write(config.secrethub_endpoint_user, username)
                    hub.write(config.secrethub_endpoint_pwd, pwd)

                    print('# Django')
                    print(f'- Create user "{username}" with password {pwd}')
                    helpers.ask_for_enter()
            else:
                config.secrethub_endpoint_user = args.secrethub_endpoint_user
                config.secrethub_endpoint_pwd = args.secrethub_endpoint_pwd

            config.save()
            print(helpers.bcolors.OKGREEN + f'Config saved under `{Config.FILENAME}`' + helpers.bcolors.ENDC)
            return 0
