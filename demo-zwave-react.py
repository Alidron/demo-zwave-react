# Copyright (c) 2015-2016 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import signal
import sys
from functools import partial
from isac import IsacNode, IsacValue
from isac.tools import green

class DemoNode(object):

    def __init__(self):
        self.node = IsacNode('demo-zwave-react')
        green.signal(signal.SIGTERM, partial(self.sigterm_handler))

        self.action_value = IsacValue(self.node, 'zwave://0xdefbc93b.power_strip001/switch_binary/1/switch', survey_last_value=False, survey_static_tags=False)

        self.sensor_value = IsacValue(self.node, 'zwave://0xdefbc93b.13/alarm/access_control', survey_last_value=False, survey_static_tags=False)
        self.sensor_value.observers += self.value_update

    def value_update(self, iv, value, timestamp, tags):
        print 'Received update: ', value
        if value == 0x16: # Open
            self.action_value.value = True
        elif value == 0x17: # Close
            self.action_value.value = False

    def sigterm_handler(self):
        self.node.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    demo = DemoNode()

    try:
        print 'serving'
        demo.node.serve_forever()
    except KeyboardInterrupt:
        demo.node.shutdown()
