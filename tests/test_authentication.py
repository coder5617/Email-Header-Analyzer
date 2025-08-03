from email_header_analyzer.core.authentication import AuthenticationAnalyzer

def test_spf_pass():
    headers = {"Received-SPF": "pass"}
    res = AuthenticationAnalyzer().analyze(headers)
    assert res["spf"]["result"] == "pass"
