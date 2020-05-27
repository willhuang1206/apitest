{{ result['name'] }}执行结果:
         >用例数:{{ result['totalCount'] }}
         >通过数:<font color="info">{{ result['passCount'] }}</font>
         >失败数:<font color="warning">{{ result['failCount'] }}</font>
         >测试时间:{{ result['testtime'] }}
         >执行时间:{{ result['duration'] }}秒
         >[详细执行报告]({{ result['reportUrl'] }})