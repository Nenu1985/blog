#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_project.settings')

    # # start new section
    # from django.conf import settings

    # if settings.DEBUG:
    #     if os.environ.get('RUN_MAIN') and os.environ.get('DEBUG_IN_CONTAINER'):
    #         # import ptvsd
    #         import debugpy
    #         debugpy.listen(('0.0.0.0', 5678))
    #         # Pause the program until a remote debugger is attached
    #         debugpy.wait_for_client()
    #         # ptvsd.enable_attach(address=('0.0.0.0', 5678))
    #         # debugpy.breakpoint()
    #         print('Attached!')
    # # end new section

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
