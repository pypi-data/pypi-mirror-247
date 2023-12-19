import traceback
import functools
from itertools import count
from datetime import datetime
from time import perf_counter_ns
from inspect import iscoroutinefunction
from .bug import Bug
from .utils import skip_test
from .traceback import format_traceback
from ..utils.string_color import str_color
from .exception import BugCreationException
from ..utils.logger import test_rest_api_logger
from ..assertion.exception import AssertException
from ..variable.exception import VariableException
from ..constant.exception import ConstantException
from ..utils.exception import TestRestApiException
from ..test_data.exception import TestDataException
from ..environment.exception import EnvironmentException
from ..reporting.report import ReportTestResult, TestStatus, ErrorType
from ..rest_api.exception import RestApiCreationException, RestApiSendException

# Iter for creating id for testcase name
iter_test_name = count(start=1)
# Initialise report object as None
report = None
# color mapper for test status
test_status_colors = {TestStatus.PASS: '#4bc0c0',
                      TestStatus.FAIL: '#ff6384',
                      TestStatus.ERROR: '#ffcd56'}
# icon mapper for test status
test_status_icons = {TestStatus.PASS: 'bi bi-check-circle-fill',
                     TestStatus.FAIL: 'bi bi-bug-fill',
                     TestStatus.ERROR: 'bi bi-x-octagon-fill'}


def test(*, name="", desc="", enabled=True, tags=[], is_async=True, execution_order='z'):
    def testcase_decorator(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            # Get the test file path
            testsuite: str = func.__module__ if func.__module__ else 'root file'
            # Create the test name & also add unique id at the end (Users can provide same name for multiple testcases)
            testcase_name: str = f'{name} ({testsuite})' if name else f'{func.__name__} ({testsuite})' + f' [{next(iter_test_name)}]'
            # Initialise variables required for reporting
            start = end = bug_priority = error_type = logs_end = ''
            duration, logs = '0 seconds', 'No data to display'
            # Set Skip details
            status, details = TestStatus.SKIP, 'Testcase is skipped'
            # Skip the test if execution #tags not present in test #tags
            if not skip_test(tags=tags):
                # Set Disable details
                status, details = TestStatus.DISABLE, 'Testcase is disabled'
                # Only execute enabled testcases
                if enabled:
                    print(
                        f'<br id="logs-start-{testcase_name.replace(" ", "-").replace("(", "").replace(")", "").replace("[", "").replace("]", "")}"></br><br></br><span style="font-weight: bolder">{testcase_name} <span class="badge" style="background-color: #212529bf"><i class="bi bi-rocket-takeoff-fill"></i>&nbsp;<b>START</b></span></span><br></br><br></br>')
                    try:
                        # Start the stopwatch / counter
                        timer_start = perf_counter_ns()
                        # Get the start date time of the test
                        start = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                        # Call the async test function
                        await func(*args, **kwargs)
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.passed(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = ''
                        # Update the test status and details
                        status, details = TestStatus.PASS, 'Success'
                    except RestApiCreationException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.REST_API
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except RestApiSendException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.REST_API
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except BugCreationException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.BUG
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except EnvironmentException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.ENVIRONMENT
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except TestDataException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.TEST_DATA
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except VariableException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.VARIABLE
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except ConstantException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.CONSTANT
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.test_rest_api_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except Bug as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.failed(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the bug priority for reporting
                        bug_priority = exc.priority
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.bug_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.FAIL, traceback_data
                    except AssertException as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))  # Get the code traceback details
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the error type for reporting
                        error_type = ErrorType.ASSERTION
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.assert_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except AssertionError as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.failed(testcase_name))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = str(exc)
                        # Update the bug priority for reporting
                        bug_priority = exc.args[0].priority if exc.args and isinstance(exc.args[0],
                                                                                       Bug) else Bug.PRIORITY.LOW
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.assert_error(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.FAIL, traceback_data
                    except AttributeError as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Format the exc str to report format
                        test_rest_api_exc = TestRestApiException(msg=str(exc))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = test_rest_api_exc.msg
                        # Provide a tip for error caused due to await keyword missing scenarios
                        if "'coroutine' object has no attribute" in logs_end:
                            logs_end += f'\n\n{"Tip: This may be due to not using await keyword in async Rest api send function calls"}'
                        # Update the error type for reporting
                        error_type = ErrorType.UNEXPECTED
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.unexpected_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    except Exception as exc:
                        # Log the result to the console
                        test_rest_api_logger.info(str_color.error(testcase_name))
                        # Format the exc str to report format
                        test_rest_api_exc = TestRestApiException(msg=str(exc))
                        # Update the logs, which has to be added after stdout (eg: error, bug etc)
                        logs_end = test_rest_api_exc.msg
                        # Update the error type for reporting
                        error_type = ErrorType.UNEXPECTED
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback data to remove unwanted info
                        traceback_data = format_traceback.unexpected_exc(traceback=traceback_data)
                        # Update the test status and details
                        status, details = TestStatus.ERROR, traceback_data
                    finally:
                        # Set the end time of the test
                        end = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                        # Stop the stopwatch / counter
                        timer_stop = perf_counter_ns()
                        # Calculate the time duration of the test in seconds (note: duration is in nanoseconds)
                        duration = f'{(timer_stop - timer_start) / 1000000000} seconds'
                        # Format logs_end
                        logs_end = f'<span style="color: {test_status_colors[status]}; font-weight: bolder">{logs_end}</span><span style="font-weight: bolder; color: #000000">{testcase_name} </span><span class="badge" style="background-color: {test_status_colors[status]}" ><i class="{test_status_icons[status]}"></i>&nbsp;<b>{status.upper()}</b></span>'
                        # Update the console output logs
                        print(
                            f'<br id="logs-end-{testcase_name.replace(" ", "-").replace("(", "").replace(")", "").replace("[", "").replace("]", "")}"></br><br></br>{logs_end}\n')
                        # Default message in html report with start and end navigation buttons
                        logs = f'Click to view <a href="#logs-start-{testcase_name.replace(" ", "-").replace("(", "").replace(")", "").replace("[", "").replace("]", "")}" class="badge" style="background-color: #36a2eb;text-decoration: none"><i class="bi bi-file-text-fill"></i>&nbsp;<b>START</b></a>&nbsp;<a href="#logs-end-{testcase_name.replace(" ", "-").replace("(", "").replace(")", "").replace("[", "").replace("]", "")}" class="badge" style="background-color: #36a2eb;text-decoration: none"><i class="bi bi-file-text-fill"></i>&nbsp;<b>END</b></a>'

            # Create Report test result object instance
            test_result = ReportTestResult(name=testcase_name,
                                           desc=desc,
                                           is_async=is_async,
                                           testsuite=testsuite,
                                           status=status,
                                           details=details,
                                           logs=logs,
                                           tags=tags,
                                           start=start,
                                           end=end,
                                           duration=duration,
                                           bug_priority=bug_priority,
                                           error_type=error_type)
            # Add the test result to the report
            report.add_test_result(test_result)

        # Only async functions can be decorated with @test
        inner.is_testcase = True if iscoroutinefunction(func) else False
        inner.is_async_testcase = is_async
        # For ordering sequential testcases
        inner.execution_order = execution_order
        return inner

    return testcase_decorator
