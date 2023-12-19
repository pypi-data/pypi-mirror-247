# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 16:18:19
# @Author  : Pane Li
# @File    : functions_locators.py
"""
functions_locators

"""
from playwright.sync_api import Page
from inhandtest.pages.adapt_model_locator import AdaptModelLocator


class FunctionsLocators(AdaptModelLocator):

    def __init__(self, page: Page, locale: dict, model: str):
        super().__init__(model)
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    @AdaptModelLocator.adapt_model
    def lan_or_localnetwork(self) -> list:
        return [
            ('lan_resource',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first}, 'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#lan_modal_alias')}, 'type': 'fill'}),
                 ('mode', {'locator': {
                     'default': self.page.locator('#lan_modal_l3_vlan')}, 'type': 'radio_select',
                     'param': {'ip_mode': self.locale.ip_mode, 'vlan_only_mode': self.locale.vlan_only_mode}}),
                 ('type', {'locator': {
                     'default': self.page.locator('#lan_modal_guest')}, 'type': 'radio_select',
                     'param': {'standrad': self.locale.standard, 'guest': self.locale.guest}}),
                 ('vlan', {'locator': {'default': self.page.locator('#lan_modal_vlan')}, 'type': 'fill'}),
                 ('ip_address_mask', {'locator': {'default': self.page.locator('#lan_modal_ipv4_ip')},
                                      'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('ip_address', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@type="text"]').first, }, 'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('mask', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@class="ant-input-number-input"]').first}, 'type': 'fill',
                           "relation": [('mode', 'ip_mode')]}),
                 ('dhcp_server', {'locator': {'default': self.page.locator('#lan_modal_enabled')},
                                  'type': 'switch_button', "relation": [('mode', 'ip_mode')]}),
                 ('dhcp_ip_range_start_ip', {'locator': {'default': self.page.locator('#lan_modal_ip_pool_start_ip')},
                                             'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('dhcp_ip_range_end_ip', {'locator': {'default': self.page.locator('#lan_modal_ip_pool_end_ip')},
                                           'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('ipv6', {'locator': {'default': self.page.locator('#lan_modal_ipv6_mode')}, 'type': 'select',
                           'param': {'disable': self.locale.disable, 'auto': self.locale.auto,
                                     'static_ip': self.locale.static_ip}}),
                 ('ipv6_address', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@type="text"]').last}, 'type': 'fill', 'relation': [('ipv6', 'static_ip')]}),
                 ('ipv6_prefix_length', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@class="ant-input-number-input"]').last}, 'type': 'fill',
                                         'relation': [('ipv6', 'static_ip')]}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first}, 'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)}, 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def wan(self) -> list:
        return [
            ('type', {'locator': {'default': self.page.locator('#ipType'),
                                  'EAP600': self.page.locator('#ipType')}, 'type': 'select'}),
            ('ip_address', {'locator': {'default': self.page.locator('#ip'),
                                        'EAP600': self.page.locator('#ip')}, 'type': 'fill'}),
            ('mask', {'locator': {'default': self.page.locator('#mask'),
                                  'EAP600': self.page.locator('#mask')}, 'type': 'fill'}),
            ('gateway_address', {'locator': {"default": self.page.locator('#gateway'),
                                             "EAP600": self.page.locator('#gateway')}, 'type': 'input'}),
            ('main_dns', {'locator': {"default": self.page.locator('#dns1'),
                                      'EAP600': self.page.locator('#dns1')}, 'type': 'fill', }),
            ('secondary_dns', {'locator': {"default": self.page.locator('#dns2'),
                                           'EAP600': self.page.locator('#dns2')}, 'type': 'fill'}),
            ('mtu', {'locator': {"default": self.page.locator('#mtu'),
                                 'EAP600': self.page.locator('#mtu')}, 'type': 'fill'}),
            ('save', {'locator': {"default": self.page.locator(f'button:has-text("{self.locale.get("save")}")'),
                                  'EAP600': self.page.locator(f'button:has-text("{self.locale.get("save")}")')},
                      'type': 'button'}),
            ('reset', {'locator': {"default": self.page.locator(f'button:has-text("{self.locale.get("reset")}")'),
                                   'EAP600': self.page.locator(f'button:has-text("{self.locale.get("reset")}")')},
                       'type': 'button'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def internet(self) -> list:
        return [
            ('uplink_table',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first}, 'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')}, 'type': 'radio_select'}),
                 ('status', {'locator': {'default': self.page.locator('#status')}, 'type': 'switch_button'}),
                 ('nat', {'locator': {'default': self.page.locator('#nat')}, 'type': 'check'}),
                 ('ipv4_type', {'locator': {'default': self.page.locator('#ipType')}, 'type': 'select',
                                'param': {'dhcp': 'DHCP', 'static_ip': self.locale.static_ip, 'pppoe': 'PPPoE'}}),
                 ('ipv4_address', {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill'}),
                 ('mask', {'locator': {'default': self.page.locator('#mask')}, 'type': 'fill'}),
                 ('ipv4_gateway_address', {'locator': {'default': self.page.locator('#gateway')}, 'type': 'fill'}),
                 ('main_dns', {'locator': {'default': self.page.locator('#dns1')}, 'type': 'fill'}),
                 ('secondary_dns', {'locator': {'default': self.page.locator('#dns2')}, 'type': 'fill'}),
                 ('pppoe_user_name', {'locator': {'default': self.page.locator('#pppoe_username')}, 'type': 'fill'}),
                 ('pppoe_password', {'locator': {'default': self.page.locator('#pppoe_password')}, 'type': 'fill'}),
                 ('local_ip_address', {'locator': {'default': self.page.locator('#pppoe_local_ip')}, 'type': 'fill'}),
                 ('remote_ip_address', {'locator': {'default': self.page.locator('#pppoe_remote_ip')}, 'type': 'fill'}),
                 ('ipv6_type', {'locator': {'default': self.page.locator('#ipv6_mode')}, 'type': 'select',
                                'param': {'disable': self.locale.disable, 'static_ip': self.locale.static_ip,
                                          'auto': self.locale.auto}}),
                 ('ipv6_address', {'locator': {'default': self.page.locator('#ipv6_ip')}, 'type': 'fill'}),
                 ('prefix_length', {'locator': {'default': self.page.locator('#ipv6_prefix_len')}, 'type': 'fill'}),
                 ('ipv6_gateway_address', {'locator': {'default': self.page.locator('#ipv6_gateway')}, 'type': 'fill'}),
                 ('main_ipv6_dns', {'locator': {'default': self.page.locator('#ipv6_dns1')}, 'type': 'fill'}),
                 ('secondary_ipv6_dns', {'locator': {'default': self.page.locator('#ipv6_dns2')}, 'type': 'fill'}),
                 ('mtu', {'locator': {'default': self.page.locator('#mtu')}, 'type': 'fill'}),
                 ('band', {'locator': {'default': self.page.locator('#band')}, 'type': 'radio_select',
                           'param': {'2.4g': '2.4GHz', '5g': '5GHz'}}),
                 ('ssid', {'locator': {'default': self.page.locator('#ssid')}, 'type': 'fill'}),
                 ('security', {'locator': {'default': self.page.locator('#auth')}, 'type': 'select',
                               'param': {'open': 'OPEN', 'wpa_psk': 'WPA-PSK',
                                         'wpa2_psk': 'WPA2-PSK', 'wpa_wpa2_psk': 'WPA-PSK/WPA2-PSK'}}),
                 ('encryption', {'locator': {'default': self.page.locator('#encrypt')}, 'type': 'select',
                                 'param': {'ccmp': 'CCMP', 'ccmp_tkip': 'CCMP/TKIP'}}),
                 ('wlan_password', {'locator': {'default': self.page.locator('#key')}, 'type': 'fill'}),
                 ('work_mode', {'locator': {'default': self.page.locator('#simMode')}, 'type': 'select',
                                'param': {'only_sim1': self.locale.only_sim1, 'only_sim2': self.locale.only_sim2,
                                          'dual_mode': self.locale.dual_mode}}),
                 ('primary_card', {'locator': {'default': self.page.locator('#mainSim')}, 'type': 'select',
                                   'param': {'sim1': 'SIM1', 'sim2': 'SIM2'},
                                   'relation': [('work_mode', 'dual_mode')]}),
                 ('sim1_tab', {'locator': {'default': self.page.locator('.ant-tabs-tab-btn').nth(0)}, 'type': 'click'}),
                 ('sim1_dialing_parameters',
                  {'locator': {'default': self.page.locator('#sim1_dialingParameters')}, 'type': 'select',
                   'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 (
                     'sim1_service_type',
                     {'locator': {'default': self.page.locator('#sim1_network_type')}, 'type': 'select',
                      'param': {'auto': self.locale.auto, '2g': '2G', '3g': '3G', '4g': '4G',
                                '5g_sa': '5G SA', '4g&5g': '4G&5G'}}),
                 ('sim1_5g_type', {'locator': {'default': self.page.locator('#sim1_nr5g_mode')}, 'type': 'select',
                                   'param': {'sa': 'SA', 'nsa': 'NSA', 'sa_nsa': 'SA/NSA', 'sa_nsa_lte': 'SA/NSA/LTE',
                                             'nsa_lte': 'NSA/LTE', 'sa_lte': 'SA/LTE'}}),
                 ('sim1_pin_code', {'locator': {'default': self.page.locator('#sim1_pin_code')}, 'type': 'fill'}),
                 ('sim1_ims', {'locator': {'default': self.page.locator('#sim1_ims')}, 'type': 'select',
                               'param': {'auto': self.locale.auto, 'enable': self.locale.enable,
                                         'disable': self.locale.disable}}),
                 ('sim1_ip_type', {'locator': {'default': self.page.locator('#sim1_type')}, 'type': 'select',
                                   'param': {'ipv4': 'IPv4', 'ipv6': 'IPv6', 'ipv4&ipv6': 'IPv4&IPv6'}}),
                 ('sim1_apn', {'locator': {'default': self.page.locator('#sim1_apn')}, 'type': 'fill'}),
                 ('sim1_authentication', {'locator': {'default': self.page.locator('#sim1_auth')}, 'type': 'select',
                                          'param': {'auto': self.locale.auto, 'pap': 'PAP', 'chap': 'CHAP',
                                                    'ms_chap': 'MS-CHAP',
                                                    'ms_chapv2': 'MS-CHAPv2'}}),
                 ('sim1_username', {'locator': {'default': self.page.locator('#sim1_username')}, 'type': 'fill'}),
                 ('sim1_password', {'locator': {'default': self.page.locator('#sim1_password')}, 'type': 'fill'}),
                 ('sim2_tab', {'locator': {'default': self.page.locator('.ant-tabs-tab-btn').nth(1)}, 'type': 'click'}),
                 ('sim2_dialing_parameters',
                  {'locator': {'default': self.page.locator('#sim2_dialingParameters')}, 'type': 'select',
                   'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 (
                     'sim2_service_type',
                     {'locator': {'default': self.page.locator('#sim2_network_type')}, 'type': 'select',
                      'param': {'auto': self.locale.auto, '2g': '2G', '3g': '3G', '4g': '5G',
                                '5g_sa': '5G SA', '4g&5g': '4G&5G'}}),
                 ('sim2_5g_type', {'locator': {'default': self.page.locator('#sim2_nr5g_mode')}, 'type': 'select',
                                   'param': {'auto': self.locale.auto, '2g': '2G', '3g': '3G', '4g': '5G',
                                             'sa': 'SA', 'nsa': 'NSA', 'sa_nsa': 'SA/NSA'}}),
                 ('sim2_pin_code', {'locator': {'default': self.page.locator('#sim2_pin_code')}, 'type': 'fill'}),
                 ('sim2_ims', {'locator': {'default': self.page.locator('#sim2_ims')}, 'type': 'select',
                               'param': {'auto': self.locale.auto, 'enable': self.locale.enable,
                                         'disable': self.locale.disable}}),
                 ('sim2_ip_type', {'locator': {'default': self.page.locator('#sim2_type')}, 'type': 'select',
                                   'param': {'ipv4': 'IPv4', 'ipv6': 'IPv6', 'ipv4&ipv6': 'IPv4&IPv6'}}),
                 ('sim2_apn', {'locator': {'default': self.page.locator('#sim2_apn')}, 'type': 'fill'}),
                 ('sim2_authentication', {'locator': {'default': self.page.locator('#sim2_auth')}, 'type': 'select',
                                          'param': {'auto': self.locale.auto, 'pap': 'PAP', 'chap': 'CHAP',
                                                    'ms_chap': 'MS-CHAP',
                                                    'ms_chapv2': 'MS-CHAPv2'}}),
                 ('sim2_username', {'locator': {'default': self.page.locator('#sim2_username')}, 'type': 'fill'}),
                 ('sim2_password', {'locator': {'default': self.page.locator('#sim2_password')}, 'type': 'fill'}),
                 ('cellular_mtu_mode', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@class="ant-select-selection-search-input"]')}, 'type': 'select',
                     'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 ('cellular_mtu_input', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     "//input[@class='ant-input-number-input']")},
                     'type': 'fill', 'relation': [('cellular_mtu_mode', 'manual')]}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up, 'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.pop_up.locator(
                     '.ant-btn.ant-btn-primary.ant-btn-dangerous').first}, 'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)},
                 'type': 'table_tr', }),
            ('policy', {'table': [
                ('add', {'locator': {'default': self.page.locator('.anticon.anticon-setting').first},
                         'type': 'button'}),
                ('sim1_threshold_enable',
                 {'locator': {'default': self.page.locator('#sim1_enabled')}, 'type': 'switch_button'}),
                ('sim1_threshold_input',
                 {'locator': {'default': self.page.locator('#sim1_threshold')}, 'type': 'fill'}),
                ('sim1_threshold_unit',
                 {'locator': {'default': self.page.locator('#sim1_threshold_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim1_monthly_reset_day',
                 {'locator': {'default': self.page.locator('#sim1_start_date')}, 'type': 'select'}),
                ('sim1_action',
                 {'locator': {'default': self.page.locator('#sim1_over_threshold_oper')}, 'type': 'select',
                  'param': {'notification': self.locale.notification,
                            'only_cloud_management_traffic': self.locale.only_cloud_management_traffic,
                            'switch_sim': self.locale.switch_sim}}),
                ('sim1_modify',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-link').nth(0)}, 'type': 'button'}),
                ('sim1_usage_of_the_month',
                 {'locator': {'default': self.page.locator('#sim1_adjust_usage')}, 'type': 'fill'}),
                ('sim1_usage_of_the_month_unit',
                 {'locator': {'default': self.page.locator('#sim1_adjust_usage_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim1_usage_of_the_month_confirm',
                 {'locator': {
                     'default': self.pop_up.locator(
                         'button[class="ant-btn ant-btn-primary"]:right-of(#sim1_adjust_usage_unit)').first},
                     'type': 'button'}),
                ('sim2_threshold_enable',
                 {'locator': {'default': self.page.locator('#sim2_enabled')}, 'type': 'switch_button'}),
                ('sim2_threshold_input',
                 {'locator': {'default': self.page.locator('#sim2_threshold')}, 'type': 'fill'}),
                ('sim2_threshold_unit',
                 {'locator': {'default': self.page.locator('#sim2_threshold_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim2_monthly_reset_day',
                 {'locator': {'default': self.page.locator('#sim2_start_date')}, 'type': 'select'}),
                ('sim2_action',
                 {'locator': {'default': self.page.locator('#sim2_over_threshold_oper')}, 'type': 'select',
                  'param': {'notification': self.locale.notification,
                            'only_cloud_management_traffic': self.locale.only_cloud_management_traffic,
                            'switch_sim': self.locale.switch_sim}}),
                ('sim2_modify',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-link').nth(1)}, 'type': 'button'}),
                ('sim2_usage_of_the_month',
                 {'locator': {'default': self.page.locator('#sim2_adjust_usage')}, 'type': 'fill'}),
                ('sim2_usage_of_the_month_unit',
                 {'locator': {'default': self.page.locator('#sim2_adjust_usage_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim2_usage_of_the_month_confirm',
                 {'locator': {'default': self.pop_up.locator(
                     'button[class="ant-btn ant-btn-primary"]:right-of(#sim2_adjust_usage_unit)').first},
                  'type': 'button'}),
                ('abnormal_card_switching_time',
                 {'locator': {'default': self.page.locator('#dial_timeout')}, 'type': 'fill'}),
                ('reuse_the_primary_card',
                 {'locator': {'default': self.page.locator('.ant-select-selection-overflow')},
                  'type': 'select_more',
                  'param': {'usage': self.locale.usage, 'time': self.locale.time, 'date': self.locale.date}}),
                ('usage_traffic',
                 {'locator': {'default': self.page.locator('#backup_sim_policy_usage_traffic_value')}, 'type': 'fill'}),
                ('usage_traffic_unit',
                 {'locator': {'default': self.page.locator('#backup_sim_policy_usage_traffic_unit')}, 'type': 'select',
                  'param': {'mb': 'MB', 'gb': 'GB'}}),
                ('using_time',
                 {'locator': {'default': self.page.locator('//input[@id="backup_sim_policy_using_time"]')},
                  'type': 'fill'}),
                ('switching_day_of_month',
                 {'locator': {'default': self.page.locator('#backup_sim_policy_revert_day')}, 'type': 'select'}),
                ('save', {'locator': self.pop_up.locator(
                    '//button[@class="ant-btn ant-btn-primary"]').last, 'type': 'button',
                          'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                  "always_do": True}),
                ('pop_up', {'locator': {'default': self.pop_up, 'default': self.pop_up}, 'type': 'button'}),
                ('action_confirm', {'locator': {'default': self.pop_up.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                    'type': 'button'})],
                'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                            },
                'type': 'table_tr', }),
            ('link_detection',
             {'locator': {'default': self.page.locator('#enabled')}, 'type': 'switch_button'}),
            ('detection_address_1',
             {'locator': {'default': self.page.locator('#target')}, 'type': 'fill'}),
            ('detection_address_2',
             {'locator': {'default': self.page.locator('#target2')}, 'type': 'fill'}),
            ('link_backup',
             {'locator': {'default': self.page.locator('#failover')}, 'type': 'radio'}),
            ('failover_mode',
             {'locator': {'default': self.page.locator('#switch_model')}, 'type': 'select',
              'param': {'immediately_switch': self.locale.immediately_switch,
                        'delayed_switch': self.locale.delayed_switch, 'do_not_switch': self.locale.do_not_switch}}),
            ('delay_number',
             {'locator': {'default': self.page.locator('#delay_num')}, 'type': 'fill',
              'relation': [('failover_mode', 'delayed_switch')]}),
            ('load_balancing',
             {'locator': {'default': self.page.locator('#load_balancing')}, 'type': 'radio'}),
            ('save', {'locator': self.page.locator(
                '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]').nth(1), 'type': 'button',
              "always_do": True})

        ]

    @property
    @AdaptModelLocator.adapt_model
    def inbound_rules(self) -> list:
        return [
            ('inbound_rules',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('interface', {'locator': {'default': self.page.locator('#interface')},
                                'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'custom': self.locale.custom,
                                                           'tcp': 'TCP', 'udp': 'UDP', 'icmp': 'ICMP', 'any': 'Any'}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', "relation": [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select',
                             'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', "relation": [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                                  'type': 'select',
                                  'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                        'type': 'fill', "relation": [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('permit', {'locator': {'default': self.page.locator('//input[@value="permit"]')},
                             'type': 'check'}),
                 ('deny', {'locator': {'default': self.page.locator('//input[@value="deny"]')},
                           'type': 'check'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})

             ],
                 'locator': {'default': self.page.locator('.ant-tabs-content.ant-tabs-content-top').nth(1)
                             },
                 'type': 'grid', }
             ),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def ipsec_vpn(self) -> list:
        return [(
            'ipsec_vpn',
            {'table': [
                ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                         'type': 'button'}),
                ('name', {'locator': {'default': self.page.locator('#name')},
                          'type': 'fill'}),
                ('status', {'locator': {'default': self.page.locator('#enabled')},
                            'type': 'switch_button'}),
                ('ike_version', {'locator': {'default': self.page.locator('#ike_version')},
                                 'type': 'select', 'param': {'ikev1': 'IKEv1', 'ikev2': 'IKEv2'}}),
                ('negotiation_mode', {'locator': {'default': self.page.locator('#ike_profile_ikev1_mode')},
                                      'type': 'select', 'param': {'main_mode': self.locale.main_mode,
                                                                  'agressive_mode': self.locale.agressive_mode},
                                      'relation': [('ike_version', 'ikev1')]}),
                ('pre_shared_key', {'locator': {'default': self.page.locator('#key')},
                                    'type': 'fill'}),
                ('uplink_interface', {'locator': {'default': self.page.locator('#interface')},
                                      'type': 'select'}),
                ('peer_address', {'locator': {'default': self.page.locator('#peeraddr')},
                                  'type': 'fill'}),
                ('tunnel_mode', {'locator': {'default': self.page.locator('#mode')},
                                 'type': 'select', 'param': {'tunnel': self.locale.tunnel,
                                                             'transmission': self.locale.transmission}}),
                ('local_subnet', {'locator': {'default': self.page.locator('#local_subnet_0')},
                                  'type': 'multi_fill'}),
                ('remote_subnet', {'locator': {'default': self.page.locator('#remote_subnet_0')},
                                   'type': 'multi_fill'}),
                ('local_identity', {'locator': {'default': self.page.locator('#ike_profile_lid_type')},
                                    'type': 'select', 'param': {'auto': self.locale.auto,
                                                                'ip_address': 'IP Address',
                                                                'fqdn': 'FQDN',
                                                                'user_fqdn': 'User FQDN', }}),
                ('local_identity_id', {'locator': {'default': self.page.locator('#ike_profile_local_id')},
                                       'type': 'fill'}),
                ('peer_identity', {'locator': {'default': self.page.locator('#ike_profile_rid_type')},
                                   'type': 'select', 'param': {'auto': self.locale.auto,
                                                               'ip_address': 'IP Address',
                                                               'fqdn': 'FQDN',
                                                               'user_fqdn': 'User FQDN', }}),
                ('peer_identity_id', {'locator': {'default': self.page.locator('#ike_profile_remote_id')},
                                      'type': 'fill'}),
                ('ike_policy_encryption', {'locator': {'default': self.page.locator('#ike_policy_encrypt')},
                                           'type': 'select', }),
                ('ike_policy_authentication', {'locator': {'default': self.page.locator('#ike_policy_auth')},
                                               'type': 'select', }),
                ('ike_policy_dh_groups', {'locator': {'default': self.page.locator('#ike_policy_dh')},
                                          'type': 'select', }),
                ('ike_policy_lifetime', {'locator': {'default': self.page.locator('#ike_policy_lifetime')},
                                         'type': 'fill'}),
                (
                    'ike_policy_peer_status_detect',
                    {'locator': {'default': self.page.locator('#ike_profile_dpd_enabled')},
                     'type': 'switch_button'}),
                ('ike_policy_dpd_interval', {'locator': {'default': self.page.locator('#ike_profile_dpd_interval')},
                                             'type': 'fill'}),
                ('ike_policy_dpd_timeout', {'locator': {'default': self.page.locator('#ike_profile_dpd_timeout')},
                                            'type': 'fill'}),
                ('ipsec_policy_security_protocol',
                 {'locator': {'default': self.page.locator('#ipsec_policy_sec_protocol')},
                  'type': 'select', }),
                ('ipsec_policy_encryption', {'locator': {'default': self.page.locator('#ipsec_policy_encrypt')},
                                             'type': 'select', }),
                ('ipsec_policy_authentication', {'locator': {'default': self.page.locator('#ipsec_policy_auth')},
                                                 'type': 'select', }),
                ('ipsec_policy_pfs_groups', {'locator': {'default': self.page.locator('#ipsec_policy_pfs')},
                                             'type': 'select', }),
                ('ipsec_policy_lifetime', {'locator': {'default': self.page.locator('#ipsec_policy_lifetime')},
                                           'type': 'fill'}),
                ('save', {'locator': self.page.locator(
                    '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                    'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                  "always_do": True}),
                ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                    'type': 'button'})],
                'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                            },
                'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def l2tp_vpn(self) -> list:
        return [
            ('status', {'locator': {'default': self.page.locator('#enabled')}, 'type': 'switch_button', }),
            ('uplink_interface', {'locator': {'default': self.page.locator('#interface')}, 'type': 'select', }),
            ('vpn_connection_address',
             {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill', }),
            ('ip_pool_start',
             {'locator': {
                 'default': self.page.locator('//input[@type="text"]').nth(1)},
                 'type': 'fill', }),
            ('ip_pool_end',
             {'locator': {'default': self.page.locator('//input[@type="text"]').nth(2)}, 'type': 'fill', }),
            ('username',
             {'locator': {'default': self.page.locator('#username')}, 'type': 'fill', }),
            ('password',
             {'locator': {'default': self.page.locator('#password')}, 'type': 'fill', }),
            ('authentication_mode', {'locator': {'default': self.page.locator('#ppp_auth')}, 'type': 'select',
                                     'param': {'pap': 'PAP', 'chap': 'CHAP', 'auto': 'AUTO'}}),
            ('enable_tunnel_verification',
             {'locator': {'default': self.page.locator('#tunnel_auth_enabled')}, 'type': 'check', }),
            ('server_name',
             {'locator': {'default': self.page.locator('#tunnel_auth_server')}, 'type': 'fill',
              'relation': [('enable_tunnel_verification', 'check')]}),
            ('tunnel_verification_key',
             {'locator': {'default': self.page.locator('#tunnel_auth_password')}, 'type': 'fill',
              'relation': [('enable_tunnel_verification', 'check')]}),
            ('save', {'locator': self.page.locator(
                '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
              "always_do": True}),
            ('l2tp_client',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#alias')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('uplink_interface', {'locator': {'default': self.page.locator('#interface')},
                                       'type': 'select'}),
                 ('server_address', {'locator': {'default': self.page.locator('#server_ip')},
                                     'type': 'fill'}),
                 ('username', {'locator': {'default': self.page.locator('#username')},
                               'type': 'fill', }),
                 ('password',
                  {'locator': {'default': self.page.locator('#password')}, 'type': 'fill', }),
                 ('authentication_mode', {'locator': {'default': self.page.locator('#ppp_auth')}, 'type': 'select',
                                          'param': {'pap': 'PAP', 'chap': 'CHAP', 'auto': 'AUTO'}}),
                 ('enable_tunnel_verification',
                  {'locator': {'default': self.page.locator('#tunnel_auth_enabled')}, 'type': 'check', }),
                 ('server_name',
                  {'locator': {'default': self.page.locator('#tunnel_auth_server')}, 'type': 'fill',
                   'relation': [('enable_tunnel_verification', 'check')]}),
                 ('tunnel_verification_key',
                  {'locator': {'default': self.page.locator('#tunnel_auth_password')}, 'type': 'fill',
                   'relation': [('enable_tunnel_verification', 'check')]}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def vxlan_vpn(self) -> list:
        return [
            ('vxlan_vpn',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#vxlanEditor_name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#vxlanEditor_enabled')},
                             'type': 'switch_button'}),
                 ('uplink_interface', {'locator': {'default': self.page.locator('#vxlanEditor_interface')},
                                       'type': 'select'}),
                 ('peer_address', {'locator': {'default': self.page.locator('#vxlanEditor_remote')},
                                   'type': 'fill'}),
                 ('vni', {'locator': {'default': self.page.locator('#vxlanEditor_vni')},
                          'type': 'fill', }),
                 ('local_subnets', {'locator': {'default': self.page.locator('#vxlanEditor_vlan')},
                                    'type': 'select'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def outbound_rules(self) -> list:
        return [
            ('outbound_rules',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('interface', {'locator': {'default': self.page.locator('#interface')},
                                'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'custom': self.locale.custom,
                                                           'tcp': 'TCP', 'udp': 'UDP', 'icmp': 'ICMP', 'any': 'Any'}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', "relation": [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select',
                             'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', "relation": [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                                  'type': 'select',
                                  'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                        'type': 'fill', "relation": [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('permit', {'locator': {'default': self.page.locator('//input[@value="permit"]')},
                             'type': 'check'}),
                 ('deny', {'locator': {'default': self.page.locator('//input[@value="deny"]')},
                           'type': 'check'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})

             ],
                 'locator': {'default': self.page.locator('.ant-tabs-content.ant-tabs-content-top').nth(1)
                             },
                 'type': 'grid', }
             ),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def port_forwarding(self) -> list:
        return [
            ('port_forwarding',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#port_modal_name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#port_modal_enabled')},
                             'type': 'switch_button'}),
                 ('interface', {'locator': {'default': self.page.locator('#port_modal_interface')},
                                'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#port_modal_protocol')},
                               'type': 'select', 'param': {'tcp': 'TCP', 'udp': 'UDP', 'tcp&udp': 'TCP&UDP'}}),
                 ('public_port', {'locator': {'default': self.page.locator('#port_modal_external_port')},
                                  'type': 'fill'}),
                 ('local_address', {'locator': {'default': self.page.locator('#port_modal_ip')},
                                    'type': 'fill', }),
                 ('local_port', {'locator': {'default': self.page.locator('#port_modal_internal_port')},
                                 'type': 'fill'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def nat(self) -> list:
        return [
            ('input_name_query', {'locator': {'default': self.page.locator('#name')}, 'type': 'fill'}),
            ('input_ip_query', {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill'}),
            ('input_port_query', {'locator': {'default': self.page.locator('#port')}, 'type': 'fill'}),
            ('reset',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
              "always_do": True}),
            ('nat',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#natEditForm_name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#natEditForm_enabled')},
                             'type': 'switch_button'}),
                 ('type', {'locator': {'default': self.page.locator('#natEditForm_type')},
                           'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#natEditForm_protocol')},
                               'type': 'select',
                               'param': {'tcp': 'TCP', 'udp': 'UDP', 'tcp&udp': 'TCP&UDP', 'any': 'Any'}}),
                 ('source',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.source}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.source}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('source', 'custom')]}),
                 ('src_port',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.src_port}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.src_port}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('src_port', 'custom')]}),
                 ('destination',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.destination}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.destination}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('destination', 'custom')]}),
                 ('dst_port',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.dst_port}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.dst_port}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('dst_port', 'custom')]}),
                 ('converted_address', {'locator': {'default': self.page.locator('#natEditForm_translation')},
                                        'type': 'fill', }),
                 ('converted_port',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.converted_port}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('converted_port_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.converted_port}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('converted_port', 'custom')]}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def mac_address_filter(self) -> list:
        return [
            ('unlimited',
             {'locator': {'default': self.page.locator('#macFilterListSet_mode').locator('.ant-radio-input').nth(0)},
              'type': 'radio'}),
            ('blacklist',
             {'locator': {'default': self.page.locator('#macFilterListSet_mode').locator('.ant-radio-input').nth(1)},
              'type': 'radio'}),
            ('whitelist',
             {'locator': {'default': self.page.locator('#macFilterListSet_mode').locator('.ant-radio-input').nth(2)},
              'type': 'radio'}),
            ('save',
             {'locator': {'default': self.page.locator(
                 '//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button'}),
            ('reset',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
              "always_do": True}),
            ('mac_address_list',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('mac_address', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(0)},
                                  'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('//button[@role="switch"]')},
                             'type': 'switch_button'}),
                 ('description', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(1)},
                                  'type': 'fill'}),
                 ('save', {'locator': self.page.locator('.anticon.anticon-save'), 'type': 'button'}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def domin_name_filter(self) -> list:
        return [
            ('unlimited',
             {'locator': {'default': self.page.locator('#domainFilterListSet_mode').locator('.ant-radio-input').nth(0)},
              'type': 'radio'}),
            ('blacklist',
             {'locator': {'default': self.page.locator('#domainFilterListSet_mode').locator('.ant-radio-input').nth(1)},
              'type': 'radio'}),
            ('whitelist',
             {'locator': {'default': self.page.locator('#domainFilterListSet_mode').locator('.ant-radio-input').nth(2)},
              'type': 'radio'}),
            ('save',
             {'locator': {'default': self.page.locator(
                 '//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button'}),
            ('reset',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
              "always_do": True}),
            ('domin_name_list',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('domains', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(0)},
                              'type': 'fill'}),
                 ('description', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(1)},
                                  'type': 'fill'}),
                 ('save', {'locator': self.page.locator('.anticon.anticon-save'), 'type': 'button'}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def policy_based_routing(self) -> list:
        return [
            ('policy_based_routing',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'tcp': 'TCP', 'udp': 'UDP', 'any': 'Any', 'icmp': 'ICMP',
                                                           'custom': self.locale.custom}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', 'relation': [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', 'relation': [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', 'relation': [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                   'type': 'fill', 'relation': [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', 'relation': [('dst_port', 'custom')]}),
                 ('output', {'locator': {'default': self.page.locator('#preferred_outif')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('forced_forwarding', {'locator': {'default': self.page.locator('#force_forward')},
                           'type': 'check'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-pro-grid-content-children').nth(0)
                             },
                 'type': 'grid', })
        ]
