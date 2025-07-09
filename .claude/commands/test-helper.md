---
allowed-tools: all
description: Write tests for the ./tests folder and do not touch other code
---

# 🚨🚨🚨 CRITICAL REQUIREMENT: FIX ALL ERRORS! 🚨🚨🚨

**THIS IS NOT A REPORTING TASK - THIS IS A FIXING TASK!**

When you run `/test-helper`, you are REQUIRED to:

1. **IDENTIFY** Go through the specification in `docs/specification.md` and all the code in `backend_marketplace/`
2. **WRITE** - Write new (or update) tests based on the request
3. **VERIFY** - Verify that new tests are failing and that old test are still passing due to refactor.

**FORBIDDEN BEHAVIORS:**

- ❌ "Here are the issues I found in the test code" → NO! FIX THEM!
- ❌ "The linter reports these problems in the test code" → NO! RESOLVE THEM!
- ❌ Stopping after listing issues → NO! KEEP WORKING!
- ❌ If the prompt does not contain details on why to write, do not write new tests, just make sure tests are passing and linting is clean

**YOU ARE NOT DONE UNTIL:**

- All linters pass with zero warnings by running `poetry run ruff check ./tests`
- Verify old tests still make sense, refactor them if they don't
