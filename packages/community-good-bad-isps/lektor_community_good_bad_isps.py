# -*- coding: utf-8 -*-
import os
import re

import json
from datetime import datetime
import requests

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter


class CommunityGoodBadIspsPlugin(Plugin):
    """ Custom plugin for the Tor Project Community website """

    name = 'TorBlog'
    description = u'Custom plugin for the Tor Project Community Website.'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)

    def generate_cw_fractions(self):
        """ Generate Good Bad ISPs data from OnionOO """

        # this downloads a ~35M JSON file in memory
        resp = requests.get("https://onionoo.torproject.org/details",
                            timeout=10)
        onionoo_data = resp.json()

        root = self.env.root_path
        asn_cw = {}

        for relay in onionoo_data['relays']:
            if relay["running"]:
                asn = relay["as"]
                if asn not in asn_cw:
                    asn_cw[asn] = 0
                asn_cw[asn] += relay["consensus_weight_fraction"] * 100

        with open(os.path.join(root, "databags/good-bad-isps.json"), "r", encoding="utf-8") as file:
            isp_list = json.load(file)

        isp_list['metrics_date'] = datetime.today().strftime('%Y-%m-%d')

        for country in isp_list["isps"].copy():
            for index, isp in enumerate(isp_list["isps"][country]):
                if isp["asn"] in asn_cw:
                    cw_fraction = f"{round(asn_cw[isp['asn']], 2)}%"
                else:
                    cw_fraction = ""
                isp_list["isps"][country][index]["cw_fraction"] = cw_fraction

        with open(os.path.join(root, "databags/good-bad-isps.json"), "w", encoding="utf-8") as file:
            json.dump(isp_list, file, indent=2)

    def on_before_build_all(self, builder, **extra):
        """ Before build process begins """

        if 'generate-cw-fractions' in builder.extra_flags:
            reporter.report_generic("Start generating Good Bad ISPs consensus weight fractions")
            self.generate_cw_fractions()
            reporter.report_generic("Finished generating Good Bad ISPs consensus weight fractions")
