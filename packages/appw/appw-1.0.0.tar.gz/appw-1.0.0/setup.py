#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'appw',
        version = '1.0.0',
        description = 'An alternative CLI wrapper on top of Appwrite API with support for creating & restoring snapshots to easily reproduce dev. environments.',
        long_description = '# 3rd party Appwrite CLI - `appw`\n\n> This is not a replacement for the official Appwrite CLI. It just provides\n> additional functionality by using the Appwrite API directly.\n\n### Installation\n```sh\npip install appw\n```\n\nThis installs a command line tool called `appw` which helps you manage your\nappwrite instance.\n\n\n### Usage\n\n```sh\n$ appw --help\n\n Usage: appw [OPTIONS] COMMAND [ARGS]...\n\n Appwrite wrapper cli to perform administrative tasks\n\n╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮\n│ --help      Show this message and exit.                                                   │\n╰───────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────────────────────────────────╮\n│ create       Create a new org, project, key, db, collection etc;                          │\n│ delete       Remove org, project, key, db, collection etc;                                │\n│ get          Get a specific org, project, key, db, collection etc; details                │\n│ list         List org, project, key, db, collection etc;                                  │\n│ login                                                                                     │\n│ show         View summary/information of the current context                              │\n│ snapshot     Create/restore/migrate snapshots                                             │\n│ switch       Switch the default org/project/database                                      │\n╰───────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\n```sh\nappw snapshot --help                          1 changed file  main\n\n Usage: appw snapshot [OPTIONS] COMMAND [ARGS]...\n\n Create/restore/migrate snapshots\n\n╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮\n│ --help      Show this message and exit.                                                   │\n╰───────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ────────────────────────────────────────────────────────────────────────────────╮\n│ create                                                                                    │\n│ restore   Restores an existing snapshot and syncs everything - names, schema and more     │\n╰───────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\nMore details below.\n\n\n### Creating a snapshot\nAssuming you are running your appwrite instance at http://localhost (this will\nbe made configurable in the upcoming changes), you can run the following\ncommand to create a snapshot of your entire configuration.\n\n```sh\nappw login  # enter your credentials\nappw snapshot create\n```\n\nThis creates the `snapshots` directory under the current directory where you\nare running the command with a backup of all the configurations. You can\ncheck-in these files into your (private) repo. If you are using public\nrepositories keep in mind that your OAuth credentials also get backend up in\nplain text.\n\n### Restoring/Syncing snapshot\nYou can use the `snapshot restore` command to either sync/migrate an existing\nappwrite instance or setup a completely new instance.\n\n```sh\nappw snapshot restore\n```\n\nOnce you have the snapshot restored, you can run the official `appwrite` cli to\ninitialize the project (to generate appwrite.json) - helps in deploying functions\nduring development\n\n```\nappwrite init\n```\n\n## NOTE\nAs mentioned above, this is not a replacement for the offcial CLI. But it has\ncommands to create a new/update/remove organization, projects etc; without\nhaving to create them on the appwrite web console directly. This is what helps\nus to create and restore snapshots.\n\n## Contribute\nFeatures, bug-fixes, issue reports are all welcome.\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = '',
        author_email = '',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT',

        url = 'https://github.com/TheGallliNetwork/appwrite-cli',
        project_urls = {},

        scripts = ['scripts/appw'],
        packages = [
            'appw',
            'appw.cli',
            'appw.cli.snapshots',
            'appw.cli.snapshots.utils',
            'appw.cli.snapshots.utils.restore',
            'appw.client'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'appwrite==4.1.0',
            'click==8.1.3',
            'inquirer==3.1.3',
            'requests==2.31.0',
            'rich==12.6.0',
            'rich-click==1.6.1',
            'jsondiff',
            'python-dotenv==1.0.0'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
