#!/usr/bin/env python3
"""
Email Link Validation Script for McKenzie Studios
Tests the mailto: links in index.html for proper formatting and functionality
"""

import re
from html.parser import HTMLParser

class EmailLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.email_links = []
        self.current_link = None
        self.in_link = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict and attrs_dict['href'].startswith('mailto:'):
                self.current_link = {
                    'href': attrs_dict['href'],
                    'class': attrs_dict.get('class', ''),
                    'text': '',
                    'line_num': self.getpos()[0]
                }
                self.in_link = True

    def handle_endtag(self, tag):
        if tag == 'a' and self.in_link:
            if self.current_link:
                self.email_links.append(self.current_link)
                self.current_link = None
            self.in_link = False

    def handle_data(self, data):
        if self.in_link and self.current_link:
            self.current_link['text'] += data.strip()

def validate_email_format(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def check_duplicate_tags(html_content):
    """Check for duplicate closing tags"""
    # Look for </a></a> pattern
    duplicate_pattern = r'</a>\s*</a>'
    matches = re.findall(duplicate_pattern, html_content)
    return matches

def main():
    print("=" * 60)
    print("McKenzie Studios - Email Link Validation Report")
    print("=" * 60)
    print()

    # Read the HTML file
    with open('/home/user/McKenzie_Studios_HQ/index.html', 'r') as f:
        html_content = f.read()

    # Parse email links
    parser = EmailLinkParser()
    parser.feed(html_content)

    print(f"📧 Found {len(parser.email_links)} email link(s)")
    print()

    all_tests_passed = True

    # Test each email link
    for i, link in enumerate(parser.email_links, 1):
        print(f"Link #{i}")
        print("-" * 40)
        print(f"Location: index.html:~{link['line_num']}")
        print(f"Href: {link['href']}")
        print(f"Class: {link['class']}")
        print(f"Link Text: {link['text']}")
        print()

        # Extract email from href
        email = link['href'].replace('mailto:', '')

        # Test 1: Valid email format
        is_valid = validate_email_format(email)
        status = "✓ PASS" if is_valid else "✗ FAIL"
        print(f"  {status} - Email format validation")
        if not is_valid:
            all_tests_passed = False

        # Test 2: Link text matches email
        text_matches = (link['text'] == email)
        status = "✓ PASS" if text_matches else "✗ FAIL"
        print(f"  {status} - Link text matches email address")
        if not text_matches:
            all_tests_passed = False
            print(f"           Expected: {email}, Got: {link['text']}")

        # Test 3: Has CSS class
        has_class = bool(link['class'])
        status = "✓ PASS" if has_class else "⚠ WARN"
        print(f"  {status} - Has CSS class for styling")

        # Test 4: Email domain check
        domain = email.split('@')[1] if '@' in email else ''
        is_mckenzie = 'mckenziestudios' in domain
        status = "✓ PASS" if is_mckenzie else "⚠ INFO"
        print(f"  {status} - Domain: {domain}")

        print()

    # Test 5: Check for duplicate closing tags
    print("Additional Validation")
    print("-" * 40)
    duplicate_tags = check_duplicate_tags(html_content)
    if duplicate_tags:
        print(f"  ✗ FAIL - Found {len(duplicate_tags)} duplicate closing tag(s): {duplicate_tags}")
        all_tests_passed = False
    else:
        print("  ✓ PASS - No duplicate closing tags found")

    # Test 6: Check for malformed mailto links
    malformed = re.findall(r'mailto:\s+[^\s]', html_content)
    if malformed:
        print(f"  ✗ FAIL - Found malformed mailto links with spaces")
        all_tests_passed = False
    else:
        print("  ✓ PASS - No malformed mailto links")

    print()
    print("=" * 60)
    if all_tests_passed:
        print("✓ All tests PASSED - Email links are properly configured")
    else:
        print("✗ Some tests FAILED - Please review issues above")
    print("=" * 60)
    print()

    # Instructions for manual testing
    print("Manual Testing Instructions:")
    print("1. Open index.html in a web browser")
    print("2. Navigate to the Contact section")
    print("3. Click the email link: chat@mckenziestudios.ai")
    print("4. Verify your email client opens with the correct recipient")
    print()
    print("Alternatively, open test_email_links.html for interactive testing")

if __name__ == '__main__':
    main()
