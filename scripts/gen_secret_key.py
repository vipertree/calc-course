#!/usr/bin/env python3
"""Print a new SECRET_KEY: 64 letters and digits. Nothing a shell or a sourced .env could mangle."""
import secrets
import string

print("".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64)))
