from generator import Author


def test_two_authors_with_same_username_are_equal():
    author1 = Author({"login": "testuser", "html_url": "https://github.com/testuser"})
    author2 = Author({"login": "testuser", "html_url": "https://github.com/testuser"})
    assert author1 == author2


def test_two_authors_with_different_username_are_not_equal():
    author1 = Author({"login": "testuser", "html_url": "https://github.com/testuser"})
    author2 = Author({"login": "testinguser", "html_url": "https://github.com/testuser"})
    assert author1 != author2
