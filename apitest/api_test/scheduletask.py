#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
import logging
from api_test.service import scheduleService as schedule
from api_test.api.automationReport import updateApiAutomationCoverage

# add autotest reminder task
schedule.addScheduler("更新接口自动化覆盖率自动任务", "0 * * * *", updateApiAutomationCoverage,[])