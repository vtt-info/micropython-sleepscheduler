import sleepscheduler as sl
import utime


INITIAL_DEEP_SLEEP_DELAY = 20
set_on_cold_boot = False


def init_on_cold_boot():
    sl.schedule_at_sec(__name__, finish_test, utime.time() + 61)
    sl.schedule_at_sec(__name__, check_no_deep_sleep,
                       utime.time() + INITIAL_DEEP_SLEEP_DELAY)
    global set_on_cold_boot
    set_on_cold_boot = True
    sl.schedule_immediately(__name__, every_14_seconds, 14)
    # also test schedule_immediately() with function_name
    sl.schedule_immediately(__name__, "every_30_seconds", 30)
    # test that a function with an exception it not scheduled anymore
    sl.schedule_immediately(__name__, function_div0, 10)
    sl.print_tasks()


def check_no_deep_sleep():
    print("check_no_deep_sleep(), time: {}".format(utime.time()))
    if set_on_cold_boot:
        store_current_time()
    else:
        sl.remove_all_by_module_name(__name__)
        print("TEST_ERROR Deep sleep done within first '{}' seconds".format(
            INITIAL_DEEP_SLEEP_DELAY))


def function_div0():
    store_current_time()
    return 1/0


def finish_test():
    print("finish_test(), time: {}".format(utime.time()))
    # test removal with function and function_name
    sl.remove_all(__name__, every_14_seconds)
    sl.remove_all(__name__, "every_30_seconds")

    # also test other remove functions with adding a task back
    # remove_all_by_function_name() with function and function_name
    sl.schedule_immediately(__name__, every_14_seconds, 14)
    sl.remove_all_by_function_name(every_14_seconds)
    sl.schedule_immediately(__name__, every_14_seconds, 14)
    sl.remove_all_by_function_name("every_14_seconds")
    # remove_all_by_module_name()
    sl.schedule_immediately(__name__, every_14_seconds, 14)
    sl.remove_all_by_module_name(__name__)

    expected = [0, 0, 0, 14, INITIAL_DEEP_SLEEP_DELAY, 28, 30, 42, 56]
    results = []

    index = 4
    while index < len(sl.rtc_memory_bytes):
        result = int.from_bytes(sl.rtc_memory_bytes[index - 4:index], 'big')
        results.append(result)
        index = index + 4

    failure = False
    if len(expected) == len(results):
        for i in range(len(expected)):
            if expected[i] != results[i]:
                failure = True
                print("TEST_ERROR wrong value at index '{}',' expected '{}', was '{}'".format(
                    i, expected[i], results[i]))
    else:
        print("TEST_ERROR Wrong amount of results. Expected '{}', was '{}'".format(
            len(expected), len(results)))
        failure = True

    if not failure:
        print("TEST_SUCCESS")


def every_30_seconds():
    print("every_30_seconds(), time: {}".format(utime.time()))
    store_current_time()


def every_14_seconds():
    print("every_14_seconds(), time: {}".format(utime.time()))
    store_current_time()


def store_current_time():
    bytes = utime.time().to_bytes(4, 'big')
    sl.rtc_memory_bytes = sl.rtc_memory_bytes + bytes
