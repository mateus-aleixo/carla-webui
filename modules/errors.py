import traceback
import sys

exception_records = []


def format_traceback(tb):
    return [
        [f"{x.filename}, line {x.lineno}, {x.name}", x.line]
        for x in traceback.extract_tb(tb)
    ]


def format_exception(e, tb):
    return {"exception": e, "traceback": format_traceback(tb)}


def record_exception():
    _, e, tb = sys.exc_info()

    if e is None:
        return

    if exception_records and exception_records[-1] == e:
        return

    exception_records.append(format_exception(e, tb))

    if len(exception_records) > 5:
        exception_records.pop(0)


def print_error_explanation(message):
    record_exception()

    lines = message.strip().split("\n")
    max_len = max([len(x) for x in lines])

    print("=" * max_len, file=sys.stderr)

    for line in lines:
        print(line, file=sys.stderr)

    print("=" * max_len, file=sys.stderr)
