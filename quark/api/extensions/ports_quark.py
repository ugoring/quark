# Copyright (c) 2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webob

from quantum.api import extensions
from quantum.api.v2 import base
from quantum.api.v2 import resource
from quantum.common import exceptions
from quantum import manager
from quantum import wsgi

RESOURCE_NAME = "port"
RESOURCE_COLLECTION = RESOURCE_NAME + "s"
EXTENDED_ATTRIBUTES_2_0 = {
    RESOURCE_COLLECTION: {}
}


class QuarkPortsIPAddressController(wsgi.Controller):
    def __init__(self, plugin):
        self._plugin = plugin

    def delete(self, request, id, **kwargs):
        try:
            self._plugin.disassociate_port(request.context, kwargs["port_id"],
                                           id)
        except exceptions.NotFound:
            raise webob.exc.HTTPNotFound()


class Ports_quark(object):
    """Extends ports for quark API purposes.

    * Allows for DELETE (disassociation of port) with IP address
    """

    @classmethod
    def get_name(cls):
        return "Quark Ports API Extension"

    @classmethod
    def get_alias(cls):
        return "ports_quark"

    @classmethod
    def get_description(cls):
        return "Quark Ports API Extension"

    @classmethod
    def get_namespace(cls):
        return ("http://docs.openstack.org/network/ext/"
                "port_disassociate/api/v2.0")

    @classmethod
    def get_updated(cls):
        return "2013-03-25T19:00:00-00:00"

    def get_extended_resources(self, version):
        if version == "2.0":
            return EXTENDED_ATTRIBUTES_2_0
        else:
            return {}

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        exts = []

        parent = dict(member_name=RESOURCE_NAME,
                      collection_name=RESOURCE_COLLECTION)
        quark_ports_ip_address_controller = resource.Resource(
            QuarkPortsIPAddressController(
                manager.QuantumManager.get_plugin()),
            base.FAULT_MAP)
        extension = extensions.ResourceExtension(
            "ip_address",
            quark_ports_ip_address_controller,
            parent)
        exts.append(extension)

        return exts