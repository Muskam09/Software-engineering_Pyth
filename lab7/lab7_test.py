import pytest

from lab7 import calculate_total_bytes

@pytest.mark.parametrize(
    "log_data, expected_bytes",
    [
        ("213.109.238.193 - - [07/May/2017:00:08:35 +0300] \"GET "
         "/question/edit.php?cmid=1&cat=1%2C18&qpage=0&category=7%2C131&qbshowtext=0&recurse=0&recurse=1&showhidden=0&showhidden=1 HTTP/1.0\""
         " 303 440 \"http://learn.topnode.if.ua/question/edit.php\" \"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0\"\n",
         440),

        ("213.109.238.193 - - [07/May/2017:00:08:35 +0300] \"GET "
         "/question/edit.php?cmid=1&cat=1%2C18&qpage=0&category=7%2C131&qbshowtext=0&recurse=0&recurse=1&showhidden=0&showhidden=1 HTTP/1.0\""
         " 303 440 \"http://learn.topnode.if.ua/question/edit.php\" \"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0\"\n"
         
         "213.109.238.193 - - [07/May/2017:00:08:35 +0300] \"GET /login/index.php HTTP/1.0\" 303 440 \"http://learn.topnode.if.ua/question/edit.php\""
         " \"Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0\"\n",
         880),

        ("", 0),

        ("213.109.238.193 - - [07/May/2017:00:08:35 +0300] \"GET /login/index.php HTTP/1.0\" some_word some_other_word\n", 0),
    ]
)
def test_calculate_total_bytes(log_data, expected_bytes, tmpdir):
    test_file = tmpdir.join("test_log.txt")
    test_file.write(log_data)

    result = calculate_total_bytes(str(test_file))
    assert result == expected_bytes
