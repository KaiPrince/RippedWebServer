"""
 * Project Name: RippedWebServer
 * File Name: test_sharing_link.py
 * Programmer: Kai Prince
 * Date: Thu, Dec 03, 2020
 * Description: This file contains tests for creating links to share files.
"""


def test_sharing_link():
    """ Share a file for 1 hour. """
    # Arrange

    # Act

    # Assert
    assert sharing_link == public_disk_url + download_url + sharing_token
    assert files_repo_request.headers == {"Authorization": auth_token}
    assert files_repo_request.json == {
        "requester": "1",
        "file_path": "test.txt",
        "duration": str(60 * 60 * 60),
        "permissions": ["read: disk_storage"],
    }
