#!/bin/bash
#
# Copyright 2021-2024 Software Radio Systems Limited
# By using this file, you agree to the terms and conditions set
# forth in the LICENSE file which can be found at the top level of
# the distribution.
#
. /usr/lib/tuned/functions

start() {
  # srsran performance script
  echo N | tee /sys/module/drm_kms_helper/parameters/poll >/dev/null
  echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor >/dev/null
  return "$?"
}

stop() {
  return "$?"
}

process $@
