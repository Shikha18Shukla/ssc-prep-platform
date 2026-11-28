# Banking Maths Set 9 - Build and Test Report

## Static checks

- `python -m py_compile` passed for all 13 Set 9 scripts and the seven
  `backend/maths_set9/` builder modules.
- Stale-constant scan found no Set 8 counts/keys in the Set 9 importer,
  snapshotter, validator, or check scripts. The only matches were explanatory
  text stating the correct Set 9 totals (1,680 questions, 6,720 options).
- `git diff --check` exited 0. The only tracked diff is the 19-line frontend
  mapping addition in `frontend/src/pages/BankingPage.tsx`.

## Frontend production build

`npm run build` from `frontend/` completed successfully:

```
> tsc -b && vite build
✓ 57 modules transformed.
✓ built in 25.55s
```

## Backend tests

A targeted relevant suite was run with the clean temporary environment at
`C:\Users\shikh\AppData\Local\Temp\opencode\set7_testenv` (the project `backend/.env`
has a pre-existing UTF-8 BOM that prevents direct pytest startup). It covered
catalog, question bank, test sessions, banking three-section behavior, banking
PDF import, production controls, and the pipe/trains/boats/probability/data-
interpretation importer and verified-batch tests:

```
165 passed, 2 warnings in 289.56s (0:04:49)
```

The full suite was also run:

```
1 failed, 484 passed, 2 warnings in 1088.35s (0:18:08)
```

The single failure was
`test_google_auth.py::test_id_token_verification_rejects_bad_nonce_email_issuer_and_audience`,
an unrelated Google OAuth test that does not touch Banking Maths or Set 9 code.
The isolated rerun of that exact test passed:

```
1 passed, 2 warnings in 1.36s
```

`git diff --quiet -- backend/tests/test_google_auth.py backend/app/services/google_auth_service.py`
confirmed both auth files are unmodified from HEAD. The failure is therefore a
pre-existing/flaky OAuth fixture issue, not a Set 9 regression.

## Result

All Set 9-relevant build and test checks passed.
