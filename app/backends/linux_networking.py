import logging
from typing import Dict, List, Optional
from pyroute2 import IPRoute, NetlinkError
import json

logger = logging.getLogger(__name__)

class LinuxNetworkingBackend:
    def __init__(self):
        self.ipr = IPRoute()

    def list_interfaces(self) -> List[Dict]:
        interfaces = []
        try:
            for link in self.ipr.get_links():
                ifname = link.get_attr('IFLA_IFNAME')
                interfaces.append({
                    'name': ifname,
                    'index': link['index'],
                    'state': 'up' if link['flags'] & 1 else 'down',
                    'mtu': link.get_attr('IFLA_MTU')
                })
            return interfaces
        except Exception as e:
            logger.error(f"Failed to list interfaces: {e}")
            return []

    def create_vlan(self, parent_iface: str, vlan_id: int, vlan_iface: str):
        try:
            parent_idx = self._get_iface_index(parent_iface)
            if not parent_idx:
                raise ValueError(f"Parent interface {parent_iface} not found")
            self.ipr.link('add', ifname=vlan_iface, kind='vlan', link=parent_idx, vlan_id=vlan_id)
            logger.info(f"Created VLAN {vlan_id} ({vlan_iface}) on {parent_iface}")
        except NetlinkError as e:
            logger.error(f"Failed to create VLAN: {e}")
            raise RuntimeError(f"Failed to create VLAN: {e}")

    def delete_vlan(self, vlan_iface: str):
        try:
            idx = self._get_iface_index(vlan_iface)
            if idx:
                self.ipr.link('del', index=idx)
                logger.info(f"Deleted VLAN interface {vlan_iface}")
        except NetlinkError as e:
            logger.error(f"Failed to delete VLAN: {e}")
            raise

    def create_bridge(self, bridge_name: str) -> Dict:
        try:
            self.ipr.link('add', ifname=bridge_name, kind='bridge')
            logger.info(f"Created bridge {bridge_name}")
            return {'name': bridge_name, 'state': 'created'}
        except NetlinkError as e:
            logger.error(f"Failed to create bridge: {e}")
            raise

    def _get_iface_index(self, iface_name: str) -> Optional[int]:
        try:
            for link in self.ipr.get_links():
                if link.get_attr('IFLA_IFNAME') == iface_name:
                    return link['index']
        except Exception as e:
            logger.error(f"Failed to get interface index: {e}")
        return None

    def close(self):
        self.ipr.close()