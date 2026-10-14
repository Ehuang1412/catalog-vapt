

Within each finding, you'll have subsections like:

Description: What the vulnerability is.
CVSS Score: Your risk calculation.
Evidence: Your annotated screenshots from both static and dynamic tools.
Remediation: The specific code change you made to fix it.
Verification: Your "after" screenshots showing the fix is effective.

### Static Analysis: Remediation and Evidence
Technologies: Semgrep (SAST), gitleaks

The remediation for findings from static analysis (SAST) tools like Semgrep is modifying the source code itself.

The Remediation: Code Changes
For a VAPT project, the primary remediation for a SAST finding like SQL Injection is to replace the vulnerable code with a secure pattern.

Vulnerable Code: sql = f"SELECT * FROM items WHERE name LIKE '%{query}%'"
Remediated Code: sql = "SELECT * FROM items WHERE name LIKE ?" followed by conn.execute(sql, (f"%{query}%",)).fetchall().

How to Show the Result: Evidence is Everything
Yes, you absolutely take screenshots. In a professional report, a finding is just a claim until you provide proof. For a static analysis finding, your evidence should include:

A "Before" Screenshot: An image of the Semgrep scan output showing the vulnerable code and the finding.
A "Before" Code Snippet: The exact vulnerable lines of code.
An "After" Screenshot: A new Semgrep scan showing the finding is resolved.
An "After" Code Snippet: The corrected, secure code.
The Fix: A brief explanation of the code change you made and why.
You can place these screenshots directly in your Markdown report or in a dedicated /evidence folder in your project.


 Dynamic Analysis: Remediation and Evidence

The remediation for dynamic analysis (DAST) findings depends on the root cause that the scan reveals. DAST tools don't see your code; they see behavior.

The Remediation: Behavior Changes
A DAST finding like "Authentication Bypass" or "Missing Authorization" often points to a flaw in your application's logic, not just a simple code string.

For a DAST finding of SQL Injection: The remediation is the same code-level fix as the static analysis finding above.
For a DAST finding of Missing Authorization: The remediation would be adding a check in your code to ensure the user is allowed to perform that action. For example, adding if not session.get("admin"): return "Unauthorized", 401 to your /admin/add route.
For a DAST finding of Missing CSRF Protection: The remediation would be implementing CSRF tokens in your forms.
How to Show the Result: The Proof of Concept
For DAST findings, your evidence needs to demonstrate the exploit and then its resolution.

For the Exploit (Vulnerability Assessment): Capture a screenshot of OWASP ZAP or Burp Suite showing the alert and the malicious request/response. Also, capture a screenshot of the application's user interface showing the impact, such as your search bar returning all items or the admin page being accessed without authorization.
For the Fix (Verification): After you've applied the code change and reloaded your app, re-run the scan. A screenshot of the DAST tool reporting zero findings for that vulnerability is powerful evidence. Also, a final screenshot of the UI showing the exploit payload no longer works.
