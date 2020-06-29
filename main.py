import sleepscheduler as sl
import machine

sl.schedule_on_cold_boot("my_module", "init_on_cold_boot")

if machine.wake_reason() is machine.DEEPSLEEP_RESET:
    sl.run_forever()
