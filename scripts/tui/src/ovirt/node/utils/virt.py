#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# virt.py - Copyright (C) 2012 Red Hat, Inc.
# Written by Fabian Deutsch <fabiand@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.  A copy of the GNU General Public License is
# also available at http://www.gnu.org/copyleft/gpl.html.

"""
Some convenience functions related to virtualization
"""

import os.path
import libvirt

from ovirt.node import base


def hardware_is_available():
    """Determins if virtualization hardware is available.

    Returns:
        True if there is hardware virtualization hardware available
    """
    has_virtualization = False

    has_module = False
    with open("/proc/modules") as modules:
        for line in modules:
            has_module = (line.startswith("kvm_intel") or
                          line.startswith("kvm_amd"))
            if has_module:
                break

    if has_module and os.path.exists("/dev/kvm"):
        has_virtualization = True

    return has_virtualization


def hardware_is_enabled():
    """Determins if virtualization hardware is available and enabled.

    Returns:
        True if there is hardware virtualization hardware available and enabled
    """
    is_enabled = False
    if hardware_is_available():
        with open("/proc/cpuinfo") as cpuinfo:
            for line in cpuinfo:
                if line.startswith("flags"):
                    if "vmx" in line or "svm" in line:
                        is_enabled = True
    return is_enabled


def hardware_status():
    """Status of virtualization on this machine.

    Returns:
        Status of hardware virtualization support on this machine as a human
        read-able string
    """
    if hardware_is_enabled():
        return "Virtualization hardware was detected and is enabled"
    if hardware_is_available():
        return "Virtualization hardware was detected but is disabled"
    return "No virtualization hardware was detected on this system"


class LibvirtConnection(base.Base):
    def __init__(self, readonly=True):
        super(LibvirtConnection, self).__init__()
        if readonly:
            self.con = libvirt.openReadOnly(None)
        else:
            raise Exception("Not supported")

    def __enter__(self, *args, **kwargs):
        return self.con

    def __exit__(self, *args, **kwargs):
        self.con.close()
