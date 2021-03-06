# Copyright (C) 2014 Linaro Limited
#
# Author: Remi Duraffort remi.duraffort@linaro.org>
#
# This file is part of LAVA Dispatcher.
#
# LAVA Dispatcher is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# LAVA Dispatcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along
# with this program; if not, see <http://www.gnu.org/licenses>.

import os
import shutil
import subprocess  # nosec - unit test support.
import tempfile
import unittest

from lava_dispatcher.utils.filesystem import mkdtemp
from lava_dispatcher.test.test_uboot import UBootFactory, StdoutTestCase
from lava_dispatcher.actions.boot.u_boot import UBootAction, UBootRetry
from lava_dispatcher.power import ResetDevice, PDUReboot
from lava_dispatcher.test.utils import infrastructure_error
from lava_common.exceptions import InfrastructureError
from lava_dispatcher.action import Action
from lava_dispatcher.utils import vcs, installers


class TestGit(StdoutTestCase):  # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        self.cwd = os.getcwd()

        # Go into a temp dirctory
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)

        # Create a Git repository with two commits
        subprocess.check_output(['git', 'init', 'git'])  # nosec - unit test support.
        os.chdir('git')
        with open('test.txt', 'w') as testfile:
            testfile.write("Some data")
        subprocess.check_output(['git', 'add', 'test.txt'])  # nosec - unit test support.
        subprocess.check_output(['git', 'commit', 'test.txt', '-m', 'First commit'],  # nosec - unit test support.
                                env={'GIT_COMMITTER_DATE': 'Fri Oct 24 14:40:36 CEST 2014',
                                     'GIT_AUTHOR_DATE': 'Fri Oct 24 14:40:36 CEST 2014',
                                     'GIT_AUTHOR_NAME': 'Foo Bar',
                                     'GIT_AUTHOR_EMAIL': 'foo@example.com',
                                     'GIT_COMMITTER_NAME': 'Foo Bar',
                                     'GIT_COMMITTER_EMAIL': 'foo@example.com'})
        with open('second.txt', 'w') as datafile:
            datafile.write("Some more data")
        subprocess.check_output(['git', 'add', 'second.txt'])  # nosec - unit test support.
        subprocess.check_output(['git', 'commit', 'second.txt', '-m', 'Second commit'],  # nosec - unit test support.
                                env={'GIT_COMMITTER_DATE': 'Fri Oct 24 14:40:38 CEST 2014',
                                     'GIT_AUTHOR_DATE': 'Fri Oct 24 14:40:38 CEST 2014',
                                     'GIT_AUTHOR_NAME': 'Foo Bar',
                                     'GIT_AUTHOR_EMAIL': 'foo@example.com',
                                     'GIT_COMMITTER_NAME': 'Foo Bar',
                                     'GIT_COMMITTER_EMAIL': 'foo@example.com'})

        subprocess.check_output(['git', 'checkout', '-q', '-b', 'testing'])  # nosec - unit test support.
        with open('third.txt', 'w') as datafile:
            datafile.write("333")
        subprocess.check_output(['git', 'add', 'third.txt'])  # nosec - unit test support.
        subprocess.check_output(['git', 'commit', 'third.txt', '-m', 'Third commit'],  # nosec - unit test support.
                                env={'GIT_COMMITTER_DATE': 'Thu Sep  1 10:14:29 CEST 2016',
                                     'GIT_AUTHOR_DATE': 'Thu Sep  1 10:14:29 CEST 2016',
                                     'GIT_AUTHOR_NAME': 'Foo Bar',
                                     'GIT_AUTHOR_EMAIL': 'foo@example.com',
                                     'GIT_COMMITTER_NAME': 'Foo Bar',
                                     'GIT_COMMITTER_EMAIL': 'foo@example.com'})

        subprocess.check_output(['git', 'checkout', '-q', 'master'])  # nosec - unit test support.

        # Go into the tempdir
        os.chdir('..')

    def tearDown(self):
        os.chdir(self.cwd)
        # Remove everything
        shutil.rmtree(self.tmpdir)

    def test_simple_clone(self):
        git = vcs.GitHelper('git')
        self.assertEqual(git.clone('git.clone1'), 'a7af835862da0e0592eeeac901b90e8de2cf5b67')
        self.assertEqual(git.clone('git.clone2'), 'a7af835862da0e0592eeeac901b90e8de2cf5b67')
        self.assertEqual(git.clone('git.clone3'), 'a7af835862da0e0592eeeac901b90e8de2cf5b67')

    def test_clone_at_head(self):
        git = vcs.GitHelper('git')
        self.assertEqual(git.clone('git.clone1', revision='a7af835862da0e0592eeeac901b90e8de2cf5b67'), 'a7af835862da0e0592eeeac901b90e8de2cf5b67')

    def test_clone_at_head_1(self):
        git = vcs.GitHelper('git')
        self.assertEqual(git.clone('git.clone1', revision='2f83e6d8189025e356a9563b8d78bdc8e2e9a3ed'), '2f83e6d8189025e356a9563b8d78bdc8e2e9a3ed')
        self.assertEqual(git.clone('git.clone2', revision='2f83e6d8189025e356a9563b8d78bdc8e2e9a3ed'), '2f83e6d8189025e356a9563b8d78bdc8e2e9a3ed')

    def test_non_existing_git(self):
        git = vcs.GitHelper('does_not_exists')
        self.assertRaises(InfrastructureError, git.clone, ('foo.bar'))

    def test_existing_destination(self):
        git = vcs.GitHelper('git')
        self.assertEqual(git.clone('git.clone1'), 'a7af835862da0e0592eeeac901b90e8de2cf5b67')
        self.assertRaises(InfrastructureError, git.clone, ('git.clone1'))
        self.assertRaises(InfrastructureError, git.clone, ('git'))

    def test_invalid_commit(self):
        git = vcs.GitHelper('git')
        self.assertRaises(InfrastructureError, git.clone, 'foo.bar', True,
                          'badhash')

    def test_branch(self):
        git = vcs.GitHelper('git')
        self.assertEqual(git.clone('git.clone1', branch='testing'), 'f2589a1b7f0cfc30ad6303433ba4d5db1a542c2d')
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "git.clone1", ".git")))

    def test_no_history(self):
        git = vcs.GitHelper('git')
        self.assertEqual(git.clone('git.clone1', history=False), 'a7af835862da0e0592eeeac901b90e8de2cf5b67')
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "git.clone1", ".git")))


@unittest.skipIf(infrastructure_error('bzr'), "bzr not installed")
class TestBzr(StdoutTestCase):  # pylint: disable=too-many-public-methods

    def setUp(self):
        super().setUp()
        self.cwd = os.getcwd()

        # Go into a temp dirctory
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)
        self.env = {'BZR_HOME': self.tmpdir,
                    'BZR_LOG': os.path.join(self.tmpdir, "bzr.log")}

        # Create a Git repository with two commits
        subprocess.check_output(['bzr', 'init', 'repo'],  # nosec - unit test support.
                                env=self.env, stderr=subprocess.STDOUT)
        os.chdir('repo')
        subprocess.check_output(['bzr', 'whoami', 'lava-ci@example.com'],  # nosec - unit test support.
                                env=self.env, stderr=subprocess.STDOUT)
        with open('test.txt', 'w') as datafile:
            datafile.write("Some data")
        subprocess.check_output(['bzr', 'add', 'test.txt'],  # nosec - unit test support.
                                env=self.env, stderr=subprocess.STDOUT)
        subprocess.check_output(['bzr', 'commit', 'test.txt', '-m', 'First commit'],  # nosec - unit test support.
                                env=self.env, stderr=subprocess.STDOUT)
        with open('second.txt', 'w') as datafile:
            datafile.write("Some more data")
        subprocess.check_output(['bzr', 'add', 'second.txt'],  # nosec - unit test support.
                                env=self.env, stderr=subprocess.STDOUT)
        subprocess.check_output(['bzr', 'commit', 'second.txt', '-m', 'Second commit'],  # nosec - unit test support.
                                env=self.env, stderr=subprocess.STDOUT)

        # Go back into the tempdir
        os.chdir('..')

    def tearDown(self):
        os.chdir(self.cwd)
        # Remove everything
        shutil.rmtree(self.tmpdir)

    def test_simple_clone(self):
        bzr = vcs.BzrHelper('repo')
        self.assertEqual(bzr.clone('bzr.clone1'), '2')
        self.assertEqual(bzr.clone('bzr.clone2'), '2')
        self.assertEqual(bzr.clone('bzr.clone3'), '2')

    def test_clone_at_2(self):
        bzr = vcs.BzrHelper('repo')
        self.assertEqual(bzr.clone('bzr.clone1', revision='2'), '2')

    def test_clone_at_1(self):
        bzr = vcs.BzrHelper('repo')
        self.assertEqual(bzr.clone('bzr.clone1', revision='1'), '1')
        self.assertEqual(bzr.clone('bzr.clone2', revision='1'), '1')

    def test_non_existing_bzr(self):
        bzr = vcs.BzrHelper('does_not_exists')
        self.assertRaises(InfrastructureError, bzr.clone, ('foo.bar'))

    def test_existing_destination(self):
        bzr = vcs.BzrHelper('repo')
        self.assertEqual(bzr.clone('bzr.clone1'), '2')
        self.assertRaises(InfrastructureError, bzr.clone, ('bzr.clone1'))
        self.assertRaises(InfrastructureError, bzr.clone, ('repo'))

    def test_invalid_commit(self):
        bzr = vcs.BzrHelper('repo')
        self.assertRaises(InfrastructureError, bzr.clone, 'foo.bar', revision='3')
        self.assertRaises(InfrastructureError, bzr.clone, 'foo.bar', revision='badrev')


class TestConstants(StdoutTestCase):  # pylint: disable=too-many-public-methods
    """
    Tests that constants set in the Job YAML as parameters in an Action stanza
    override the value of that constant set in the python code for each action
    in that stanza.
    """
    def setUp(self):
        super().setUp()
        factory = UBootFactory()
        self.job = factory.create_bbb_job('sample_jobs/uboot-ramdisk.yaml')
        self.assertIsNotNone(self.job)

    def test_action_parameters(self):
        self.assertIsNotNone(self.job.parameters)
        deploy = self.job.pipeline.actions[0]
        self.assertIsNone(deploy.parameters.get('parameters'))
        uboot = self.job.pipeline.actions[1]
        self.assertEqual(
            "reboot: Restarting system",  # modified in the job yaml
            uboot.parameters.get('parameters', {}).get('shutdown-message', self.job.device.get_constant('shutdown-message'))
        )
        self.assertIsInstance(uboot, UBootAction)
        retry = [action for action in uboot.internal_pipeline.actions if action.name == 'uboot-retry'][0]
        self.assertEqual(
            "reboot: Restarting system",  # modified in the job yaml
            retry.parameters['parameters'].get('shutdown-message', self.job.device.get_constant('shutdown-message'))
        )
        self.assertIsInstance(retry, UBootRetry)
        reset = retry.internal_pipeline.actions[0]
        self.assertEqual(
            "reboot: Restarting system",  # modified in the job yaml
            reset.parameters['parameters'].get('shutdown-message', self.job.device.get_constant('shutdown-message'))
        )
        self.assertIsInstance(reset, ResetDevice)
        reboot = reset.internal_pipeline.actions[0]
        self.assertEqual(
            "reboot: Restarting system",  # modified in the job yaml
            reboot.parameters['parameters'].get('shutdown-message', self.job.device.get_constant('shutdown-message'))
        )
        self.assertIsInstance(reboot, PDUReboot)
        self.assertIsNotNone(reboot.parameters.get('parameters'))
        self.assertEqual(
            "reboot: Restarting system",  # modified in the job yaml
            reboot.parameters['parameters'].get('shutdown-message', self.job.device.get_constant('shutdown-message'))
        )


class TestClasses(StdoutTestCase):

    def setUp(self):
        super().setUp()
        from lava_dispatcher.actions.deploy import strategies  # pylint: disable=unused-variable
        from lava_dispatcher.actions.boot import strategies  # pylint: disable=reimported
        from lava_dispatcher.actions.test import strategies  # pylint: disable=reimported
        self.allowed = [
            'commands',  # pipeline.actions.commands.py
            'deploy',
            'test',
        ]

    def test_summary_exists(self):
        for subclass in Action.__subclasses__():  # pylint: disable=no-member
            if not hasattr(subclass, 'name'):
                continue
            if not hasattr(subclass, 'summary') and subclass.name not in self.allowed:
                self.fail(subclass)

    def test_description_exists(self):
        for subclass in Action.__subclasses__():  # pylint: disable=no-member
            if not hasattr(subclass, 'name'):
                continue
            if not hasattr(subclass, 'description') and subclass.name not in self.allowed:
                self.fail(subclass)


class TestInstallers(StdoutTestCase):

    def setUp(self):
        super().setUp()
        self.cwd = os.getcwd()
        self.tmpdir = tempfile.mkdtemp()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tmpdir)

    def test_add_late_command(self):
        # Create preseed file with a few lines.
        with open('preseed.cfg', 'w') as preseedfile:
            preseedfile.write('d-i netcfg/dhcp_timeout string 60\n')
            preseedfile.write('d-i pkgsel/include string openssh-server build-essential\n')
            preseedfile.write('d-i finish-install/reboot_in_progress note\n')
        preseedfile = 'preseed.cfg'

        # Test adding new preseed/late_command line.
        extra_command = 'cmd1'
        installers.add_late_command(preseedfile, extra_command)
        with open('preseed.cfg') as f_in:
            file_content = f_in.read()
            self.assertTrue('d-i preseed/late_command string cmd1' in file_content)

        # Test appending the second command to existing presseed/late_command line.
        extra_command = 'cmd2 ;'
        installers.add_late_command(preseedfile, extra_command)
        with open('preseed.cfg') as f_in:
            file_content = f_in.read()
            self.assertTrue('d-i preseed/late_command string cmd1; cmd2 ;' in file_content)

        # Test if it strips off extra space and semi-colon.
        extra_command = 'cmd3'
        installers.add_late_command(preseedfile, extra_command)
        with open('preseed.cfg') as f_in:
            file_content = f_in.read()
            self.assertTrue('d-i preseed/late_command string cmd1; cmd2; cmd3' in file_content)
