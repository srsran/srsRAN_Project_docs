#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GEO NTN Channel Emulator
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq




class geo_ntn_channel_emulator(gr.top_block):

    def __init__(self, channel_delay_us=0, samp_rate=5.76e6):
        gr.top_block.__init__(self, "GEO NTN Channel Emulator", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.channel_delay_us = channel_delay_us
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.channel_delay_samples = channel_delay_samples = int(samp_rate*1e-6*channel_delay_us)

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_req_source_0_0 = zeromq.req_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2101', 100, False, -1)
        self.zeromq_req_source_0 = zeromq.req_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2000', 100, False, -1)
        self.zeromq_rep_sink_0_0 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2001', 100, False, -1)
        self.zeromq_rep_sink_0 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2100', 100, False, -1)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, channel_delay_samples)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, channel_delay_samples)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self.zeromq_rep_sink_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.zeromq_rep_sink_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.zeromq_req_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.zeromq_req_source_0_0, 0), (self.blocks_throttle_0_0, 0))


    def get_channel_delay_us(self):
        return self.channel_delay_us

    def set_channel_delay_us(self, channel_delay_us):
        self.channel_delay_us = channel_delay_us
        self.set_channel_delay_samples(int(self.samp_rate*1e-6*self.channel_delay_us))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_channel_delay_samples(int(self.samp_rate*1e-6*self.channel_delay_us))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)

    def get_channel_delay_samples(self):
        return self.channel_delay_samples

    def set_channel_delay_samples(self, channel_delay_samples):
        self.channel_delay_samples = channel_delay_samples
        self.blocks_delay_0.set_dly(self.channel_delay_samples)
        self.blocks_delay_0_0.set_dly(self.channel_delay_samples)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--channel-delay-us", dest="channel_delay_us", type=intx, default=0,
        help="Set channel_delay_us [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(5.76e6)),
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=geo_ntn_channel_emulator, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(channel_delay_us=options.channel_delay_us, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
