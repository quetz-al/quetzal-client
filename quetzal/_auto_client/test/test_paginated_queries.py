# coding: utf-8

"""
    Quetzalcoatl API

    Quetzal (short for Quetzalcoatl): an API to manage data files and their associated metadata.  # Overview  ...  ## Concepts  * File * Metadata   Versioning too * Families * Workspace   Description, workspace states, data_url, etc. * Workspace views * Queries  # Authentication  Authentication details  # Errors  Quetzal uses standard HTTP error codes to indicate success or failure of its operations. The body of the response follows [RFC-7807](https://tools.ietf.org/html/rfc7807) to provide details on an error. For example:  ``` {   \"type\": \"https://quetz.al/problems/some-name\",   \"title\": \"Bad request.\",   \"status\": 400,   \"detail\": \"Incorrect foo due to missing bar.\",   \"instance\": \"/some_path/some_id\" } ```  # Versioning  API version | Changes ------------|--------- 0.1.0       | [API changes](https://quetz.al/docs/changelog#v0-1-0)  # API reference   # noqa: E501

    OpenAPI spec version: 0.1.0
    Contact: support@quetz.al
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import quetzal._auto_client
from quetzal._auto_client.models.paginated_queries import PaginatedQueries  # noqa: E501
from quetzal._auto_client.rest import ApiException


class TestPaginatedQueries(unittest.TestCase):
    """PaginatedQueries unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPaginatedQueries(self):
        """Test PaginatedQueries"""
        # FIXME: construct object with mandatory attributes with example values
        # model = quetzal._auto_client.models.paginated_queries.PaginatedQueries()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()