#!/usr/bin/env python3

# Copyright (C) 2016 - 2019 Sylvia van Os <sylvia@hackerchick.me>
#
# Pext pass module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gettext
import html
import platform
import os
import shutil
import threading
from datetime import datetime
from os.path import expanduser, normcase
from time import sleep

from babel.dates import format_datetime
from dulwich import client, porcelain
from dulwich.file import FileLocked
from dulwich.repo import Repo
from dulwich.contrib.paramiko_vendor import ParamikoSSHVendor
from paramiko import ssh_exception

import pypass
import pyotp
import pyscreenshot
import zbar

from pext_base import ModuleBase
from pext_helpers import Action, SelectionType

class Module(ModuleBase):
    def init(self, settings, q):
        if platform.system() == 'Darwin':
            # Explicitly add support for MacGPG2
            os.environ['PATH'] = os.environ['PATH'] + ':/usr/local/MacGPG2/bin'

        try:
            lang = gettext.translation('pext_module_pass', localedir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale'), languages=[settings['_locale']])
        except FileNotFoundError:
            lang = gettext.NullTranslations()
            print("No {} translation available for pext_module_pass".format(settings['_locale']))

        lang.install()

        self.result_display_thread = None
        self.result_display_active = True

        self.data_location = expanduser(normcase("~/.password-store/")) if ('directory' not in settings) else expanduser(normcase(settings['directory']))
        self.password_store = pypass.PasswordStore(self.data_location)

        self.q = q
        self.settings = settings

        if 'ssh_password' not in self.settings or not self.settings['ssh_password']:
            self.settings['ssh_password'] = None

        if self.settings['_api_version'] < [0, 11, 1]:
            self.q.put([Action.critical_error, _("This module requires at least API version 0.11.1, you are using {}. Please update Pext.").format(".".join([str(i) for i in self.settings['_api_version']]))])
            return

        self.git_repo = self.data_location
        if (not os.path.isdir(os.path.join(self.data_location, ".git"))) or ('use_git' in self.settings and self.settings['use_git'] == _('No')):
            self.git_repo = None

        self.passwordEntries = {}

        self.q.put([Action.set_base_context, [_("Create"), _("Generate")]])

        self._get_entries()

        if not os.path.exists(os.path.join(self.data_location, ".gpg-id")):
            self._init()

    def _git_pull(self):
        try:
            if self.git_repo:
                with Repo(self.git_repo) as repo:
                    config = repo.get_config()
                    remote_url = config.get(("remote".encode(), "origin".encode()), "url".encode()).decode()
                    client.get_ssh_vendor = ParamikoSSHVendor
                    try:
                        porcelain.pull(repo, remote_url, password=self.settings['ssh_password'])
                    except (ssh_exception.SSHException, OSError) as e:
                        self.q.put([Action.add_error, _("Failed to pull from git: {}").format(str(e))])

            return
        except FileLocked:
            print("File locked when trying to pull, giving up on this pull")

    def _git_push(self):
        try:
            if self.git_repo:
                with Repo(self.git_repo) as repo:
                    config = repo.get_config()
                    remote_url = config.get(("remote".encode(), "origin".encode()), "url".encode()).decode()
                    client.get_ssh_vendor = ParamikoSSHVendor
                    try:
                        porcelain.push(repo, remote_url, 'master', password=self.settings['ssh_password'])
                    except (ssh_exception.SSHException, OSError) as e:
                        self.q.put([Action.add_error, _("Failed to push to git: {}").format(str(e))])

            return
        except FileLocked:
            print("File locked when trying to push, giving up on this push")

    def _get_data_location(self):
        return self.data_location

    def _get_entries(self):
        self._git_pull()

        for password in sorted(self.password_store.get_passwords_list(), key=lambda name: os.path.getatime("{}.gpg".format(name)), reverse=True):
            entry_path = "{}.gpg".format(password)
            entry = password[len(self._get_data_location()):]

            self.q.put([Action.add_entry, entry])
            self.q.put([Action.set_entry_info, entry, _("<b>{}</b><br/><br/><b>Last opened</b><br/>{}<br/><br/><b>Last modified</b><br/>{}").format(html.escape(entry), format_datetime(datetime.fromtimestamp(os.path.getatime(entry_path)).replace(microsecond=0), locale=self.settings['_locale']), format_datetime(datetime.fromtimestamp(os.path.getmtime(entry_path)).replace(microsecond=0), locale=self.settings['_locale']))])
            if self.settings['_api_version'] < [0, 12, 0]:
                self.q.put([Action.set_entry_context, entry, [_("Open"), _("Edit"), _("Copy"), _("Rename"), _("Remove")]])
            else:
                self.q.put([Action.set_entry_context, entry, [_("Open"), _("Edit"), _("Copy"), _("Rename"), _("Remove"), _("Add OTP")]])

    def process_response(self, response, identifier):
        # User cancellation
        if response is None:
            return

        data = identifier.split()
        if data[0] == "add_otp":
            if len(data) == 1:
                if response is not None:
                    self._add_otp(name=response)
                else:
                    self._add_otp()
            else:
                if response is not None:
                    if data[-1] in ["TOTP", "HOTP"]:
                        self._add_otp(name=" ".join(data[1:-1]), otp_type=data[-1], secret=response)
                    else:
                        self._add_otp(name=" ".join(data[1:]), otp_type=response)
                else:
                    if data[-1] in ["TOTP", "HOTP"]:
                        self._add_otp(name=" ".join(data[1:-1], otp_type=data[-1]))
                    else:
                        self._add_otp(name=" ".join(data[1:]))
        elif data[0] == "copy":
            if len(data) == 1:
                if response is not None:
                    self._copy(name=response)
                else:
                    self._copy()
            else:
                if response is not None:
                    self._copy(name=" ".join(data[1:]), copy_name=response)
                else:
                    self._copy(name=" ".join(data[1:]))
        elif data[0] == "edit":
            if len(data) == 1:
                if response is not None:
                    self._edit(name=response)
                else:
                    self._edit()
            else:
                if response is not None:
                    self._edit(name=" ".join(data[1:]), value=response)
                else:
                    self._edit(name=" ".join(data[1:]))
        elif data[0] == "generate":
            if len(data) == 1:
                if response is not None:
                    self._generate(name=response)
                else:
                    self._generate()
            else:
                if response is not None:
                    self._generate(name=" ".join(data[1:]), length=response if response else 15)
                else:
                    self._generate(name=" ".join(data[1:]))
        elif data[0] == "init":
            if response is not None:
                self._init(gpg_id=response)
            else:
                self._init()
        elif data[0] == "insert":
            if len(data) == 1:
                if response is not None:
                    self._insert(name=response)
                else:
                    self._insert()
            else:
                if response is not None:
                    self._insert(name=" ".join(data[1:]), value=response)
                else:
                    self._insert(name=" ".join(data[1:]))
        elif data[0] == "remove":
            if len(data) == 1:
                if response is not None:
                    self._remove(name=response)
                else:
                    self._remove()
            else:
                if response is not None:
                    self._remove(name=" ".join(data[1:]), confirmed=response)
                else:
                    self._remove(name=" ".join(data[1:]))
        elif data[0] == "rename":
            if len(data) == 1:
                if response is not None:
                    self._rename(name=response)
                else:
                    self._rename()
            else:
                if response is not None:
                    self._rename(name=" ".join(data[1:]), new_name=response)
                else:
                    self._rename(name=" ".join(data[1:]))
        else:
            self.q.put([Action.critical_error, _("Unknown request received: {}").format(" ".join(data))])

    def _save_password(self, name, value):
        if not value.endswith('\n'):
            value = "{}\n".format(value)

        self.password_store.insert_password(name, value)

        if self.git_repo:
            porcelain.add(self.git_repo, os.path.join(self._get_data_location(), "{}.gpg".format(name)))
            porcelain.commit(self.git_repo, message="Created/Modified {} with Pext".format(name))
            self._git_push()

    def _append_password(self, name, value):
        current_data = self.password_store.get_decrypted_password(name)

        if not current_data.endswith('\n'):
            current_data = "{}\n".format(current_data)

        if not value.endswith('\n'):
            value = "{}\n".format(value)

        self.password_store.insert_password(name, "{}{}".format(current_data, value))

        if self.git_repo:
            porcelain.add(self.git_repo, os.path.join(self._get_data_location(), "{}.gpg".format(name)))
            porcelain.commit(self.git_repo, message="Appended to {} with Pext".format(name))
            self._git_push()

    def _add_otp(self, name=None, otp_type=None, secret=None):
        if not name:
            self.q.put([Action.ask_input, _("Add OTP to which password?"), "", "add_otp"])
        elif not otp_type:
            screenshot = pyscreenshot.grab(childprocess=False).convert('L')
            qr_codes = zbar.Scanner().scan(screenshot)
            autodetected = 0
            for qr_code in qr_codes:
                qr_data = qr_code.data.decode()
                try:
                    pyotp.parse_uri(qr_data)
                except ValueError:
                    continue

                autodetected += 1
                self._append_password(name, qr_data)

            if autodetected == 0:
                self.q.put([Action.add_error, _("Could not detect any valid OTP QR codes on your screen. Continuing with manual configuration...")])
                self.q.put([Action.ask_choice, _("Use which OTP type?"), ["TOTP", "HOTP"], "add_otp {}".format(name)])
            else:
                self.q.put([Action.add_message, _("Detected and added {} valid OTP QR code(s) on your screen.").format(str(autodetected))])
                return
        elif not secret:
            self.q.put([Action.ask_input, _("What is the OTP secret?"), "", "add_otp {} {}".format(name, otp_type)])
        else:
            if otp_type == "TOTP":
                otp_uri = pyotp.TOTP(secret).provisioning_uri()
            elif otp_type == "HOTP":
                otp_uri = pyotp.HOTP(secret).provisioning_uri()
            else:
                return

            self._append_password(name, otp_uri)

    def _copy(self, name=None, copy_name=None):
        if not name:
            self.q.put([Action.ask_input, _("Copy which password?"), "", "copy"])
        elif not copy_name:
            self.q.put([Action.ask_input, _("What should the copy of {} be named?").format(name), name, "copy {}".format(name)])
        else:
            try:
                original_file_path = os.path.join(self._get_data_location(), "{}.gpg".format(name))
                copy_file_path = os.path.join(self._get_data_location(), "{}.gpg".format(copy_name))
                shutil.copyfile(original_file_path, copy_file_path)

                if self.git_repo:
                    porcelain.add(self.git_repo, [copy_file_path])
                    porcelain.commit(self.git_repo, message="Copied {} to {} with Pext".format(name, copy_name))
                    self._git_push()
            except shutil.SameFileError:
                self.q.put([Action.ask_input, _("What should the copy of {} be named?").format(name), name, "copy {}".format(name)])
                return

            self.q.put([Action.set_selection, []])

    def _edit(self, name=None, value=None):
        if not name:
            self.q.put([Action.ask_input, _("What is the name of the password to edit?"), "", "edit"])
        elif not value:
            current_data = self.password_store.get_decrypted_password(name)
            self.q.put([Action.ask_input_multi_line, _("What should the value of {} be?").format(name), current_data, "edit {}".format(name)])
        else:
            self._save_password(name, value)
            self.q.put([Action.set_selection, []])

    def _generate(self, name=None, length=None):
        if not name:
            self.q.put([Action.ask_input, _("Generate a random password under which name?"), "", 'generate'])
        elif not length:
            self.q.put([Action.ask_input, _("How many characters long should the password be?"), "15", "generate {}".format(name)])
        else:
            password = self.password_store.generate_password(name, length=int(length))
            self._insert(name=name, value=password)

    def _init(self, gpg_id=None):
        if not gpg_id:
            self.q.put([Action.ask_input, _("Please provide a GPG ID to initialize this directory with."), "", "init"])
        else:
            self.password_store.init(gpg_id, self._get_data_location)
            self.q.put([Action.set_selection, []])

    def _insert(self, name=None, value=None):
        if not name:
            self.q.put([Action.ask_input, _("What is the name of the password?"), "", 'insert'])
        elif not value:
            self.q.put([Action.ask_input_multi_line, _("What should the value of {} be?").format(name), "", "insert {}".format(name)])
        else:
            self._save_password(name, value)
            self.q.put([Action.set_selection, []])

    def _remove(self, name=None, confirmed=None):
        if not name:
            self.q.put([Action.ask_input, _("Remove which password?"), "", "remove"])
        elif confirmed is None:
            self.q.put([Action.ask_question, _("Are you sure you want to remove {}?").format(name), "remove {}".format(name)])
        elif not confirmed:
            return
        else:
            file_path = os.path.join(self._get_data_location(), "{}.gpg".format(name))
            os.remove(file_path)

            if self.git_repo:
                porcelain.add(self.git_repo, [file_path])
                porcelain.commit(self.git_repo, message="Removed {} with Pext".format(name))
                self._git_push()

            self.q.put([Action.set_selection, []])

    def _rename(self, name=None, new_name=None):
        if not name:
            self.q.put([Action.ask_input, _("Rename which password?"), "", "rename"])
        elif not new_name:
            self.q.put([Action.ask_input, _("What should the new name of {} be?").format(name), name, "rename {}".format(name)])
        else:
            old_file_path = os.path.join(self._get_data_location(), "{}.gpg".format(name))
            new_file_path = os.path.join(self._get_data_location(), "{}.gpg".format(new_name))
            os.rename(old_file_path, new_file_path)

            if self.git_repo:
                porcelain.add(self.git_repo, [old_file_path, new_file_path])
                porcelain.commit(self.git_repo, message="Renamed {} to {} with Pext".format(name, new_name))
                self._git_push()

            self.q.put([Action.set_selection, []])

    def _display_results(self, results):
        while self.result_display_active:
            result_lines = results.rstrip().splitlines()
            self.passwordEntries = {}
            # Parse OTP
            for number, line in enumerate(result_lines):
                try:
                    otp = pyotp.parse_uri(line)
                except ValueError:
                    continue

                if isinstance(otp, pyotp.TOTP):
                    otp_code = otp.now()
                else:
                    otp_code = otp.generate_otp()

                otp_description = "{} - {}".format(otp.issuer, otp.name) if otp.issuer else otp.name
                result_lines[number] = "OTP ({}): {}".format(otp_description, otp_code)

            # If only a password and no other fields, select password immediately
            if len(result_lines) == 1:
                self.q.put([Action.copy_to_clipboard, result_lines[0]])
                self.q.put([Action.close])
                return

            for line in result_lines:
                if len(self.passwordEntries) == 0:
                    self.passwordEntries["********"] = line
                else:
                    self.passwordEntries[line] = line

            self.q.put([Action.replace_entry_list, ["********"] + result_lines[1:]])

            if self.result_display_active:
                sleep(1)

    def selection_made(self, selection):
        if len(selection) == 0:
            # We're at the main menu
            if self.result_display_thread:
                self.result_display_active = False
                self.result_display_thread.join()

            self.passwordEntries = {}
            self.q.put([Action.set_header])
            self.q.put([Action.replace_command_list, []])
            self.q.put([Action.replace_entry_list, []])
            self._get_entries()
        elif selection[-1]["type"] == SelectionType.none:
            if self.result_display_thread:
                self.result_display_active = False
                self.result_display_thread.join()

            # Global context menu option
            if selection[-1]["context_option"] == _("Create"):
                self._insert()
                self.q.put([Action.set_selection, []])
                return
            elif selection[-1]["context_option"] == _("Generate"):
                self._generate()
                self.q.put([Action.set_selection, []])
                return
            else:
                self.q.put([Action.critical_error, _("Unexpected selection_made value: {}").format(selection)])
        elif len(selection) == 1:
            if self.result_display_thread:
                self.result_display_active = False
                self.result_display_thread.join()

            if selection[0]["type"] == SelectionType.entry:
                if selection[0]["context_option"] == _("Edit"):
                    self._edit(name=selection[0]["value"])
                    self.q.put([Action.set_selection, []])
                    return
                elif selection[0]["context_option"] == _("Copy"):
                    self._copy(name=selection[0]["value"])
                    self.q.put([Action.set_selection, []])
                    return
                elif selection[0]["context_option"] == _("Rename"):
                    self._rename(name=selection[0]["value"])
                    self.q.put([Action.set_selection, []])
                    return
                elif selection[0]["context_option"] == _("Remove"):
                    self._remove(selection[0]["value"])
                    self.q.put([Action.set_selection, []])
                    return
                elif selection[0]["context_option"] == _("Add OTP"):
                    self._add_otp(selection[0]["value"])
                    self.q.put([Action.set_selection, []])
                    return

                results = self.password_store.get_decrypted_password(selection[0]["value"])
                if results is None:
                    self.q.put([Action.set_selection, []])
                    return

                self.q.put([Action.replace_entry_list, []])
                self.q.put([Action.replace_command_list, []])

                self.result_display_active = True
                self.result_display_thread = threading.Thread(target=self._display_results, args=(results,), daemon=True)
                self.result_display_thread.start()
            else:
                self.q.put([Action.critical_error, _("Unexpected selection_made value: {}").format(selection)])
        elif len(selection) == 2:
            # We're selecting a password
            if self.result_display_thread:
                self.result_display_active = False
                self.result_display_thread.join()

            if selection[1]["value"] == "********":
                self.q.put([Action.copy_to_clipboard, self.passwordEntries["********"]])
            else:
                # Get the final part to prepare for copying. For example, if
                # the entry is named URL: https://example.org/", only copy
                # "https://example.org/" to the clipboard
                copyStringParts = self.passwordEntries[selection[1]["value"]].split(": ", 1)

                copyString = copyStringParts[1] if len(copyStringParts) > 1 else copyStringParts[0]
                self.q.put([Action.copy_to_clipboard, copyString])

            self.passwordEntries = {}
            self.q.put([Action.close])
        else:
            self.q.put([Action.critical_error, _("Unexpected selection_made value: {}").format(selection)])
