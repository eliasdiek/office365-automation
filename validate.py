from validate_email import validate_email

try:
    is_valid = validate_email(
        email_address='office@unionsportssales.com',
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=False,
        smtp_timeout=30,
        smtp_helo_host=None,
        smtp_from_address=None,
        smtp_skip_tls=True,
        smtp_tls_context=None,
        smtp_debug=True
    )

    print('[is_valid]', is_valid)
except:
    print('[error]')