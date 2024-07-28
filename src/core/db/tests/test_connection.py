from unittest.mock import patch

import pytest
from django.db import connections
from django.test import TestCase

from ....settings import DATABASE_CONNECTION_DEFAULT_NAME, DATABASE_CONNECTION_REPLICA_NAME

from ....tests.models import Book
from ..connection import (
    UnsafeWriterAccessError,
    allow_writer,
    allow_writer_in_context,
    log_writer_usage,
    restrict_writer,
)

class DBConnectionTestCase(TestCase):
    
    def test_allow_writer(self):
        default_connection = connections[DATABASE_CONNECTION_DEFAULT_NAME]
        assert not getattr(default_connection, "_allow_writer", False)

        with allow_writer():
            assert hasattr(default_connection, "_allow_writer")
            assert default_connection._allow_writer


    def test_allow_writer_yield_exception(self):
        default_connection = connections[DATABASE_CONNECTION_DEFAULT_NAME]

        def example_function():
            raise Exception()

        try:
            with allow_writer():
                example_function()
        except Exception:
            pass

        assert hasattr(default_connection, "_allow_writer")
        assert not default_connection._allow_writer


    def test_allow_writer_in_context_writer(self):
        with allow_writer_in_context():
            connection = connections[DATABASE_CONNECTION_DEFAULT_NAME]
            assert hasattr(connection, "_allow_writer")
            assert connection._allow_writer

    def test_restrict_writer_raises_error(self):
        connection = connections[DATABASE_CONNECTION_DEFAULT_NAME]

        with pytest.raises(UnsafeWriterAccessError):
            with connection.execute_wrapper(restrict_writer):
                Book.objects.first()


    def test_restrict_writer_in_allow_writer(self):
        connection = connections[DATABASE_CONNECTION_DEFAULT_NAME]

        with connection.execute_wrapper(restrict_writer):
            with allow_writer():
                Book.objects.first()


    # def test_log_writer_usage(self, settings, caplog):
    #     connection = connections[settings.DATABASE_CONNECTION_DEFAULT_NAME]

    #     with connection.execute_wrapper(log_writer_usage):
    #         Book.objects.first()

    #     assert caplog.records
    #     msg = caplog.records[0].getMessage()
    #     assert "Unsafe access to the writer DB detected" in msg
