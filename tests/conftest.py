"""Shared test settings.

CI runs with HYPOTHESIS_PROFILE=ci: no per-example deadline, because shared runners are slower
and noisier than your Mac. On your Mac the default profile applies, and an example that takes
longer than 200 ms fails with DeadlineExceeded: a sign that something is slower than it should be.
"""

import os

from hypothesis import settings

settings.register_profile("ci", deadline=None, print_blob=True)
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))
