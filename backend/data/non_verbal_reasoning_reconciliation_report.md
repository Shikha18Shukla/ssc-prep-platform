# CH-17 Canonical / Live Reconciliation

Chapter ID: `746c8d03-3645-4454-a875-7cd9109e133a`

## Result

Difficulty-only updates applied: **22**.
Final classifications: `{"exact_match": 33}`.
Canonical/live row counts: 33 / 33.

The stable import key is the local image path (`nvr-001.svg` … `nvr-033.svg`), paired with the ledger `question_id`. Matching also requires exact question text, four options, correct option, explanation, CH-17 chapter, active status, and Normal status. No fuzzy similarity authorized a write.

## Root cause

The live rows were created at 2026-11-03 16:29 local time; the canonical batch and ledger were rewritten at 16:38. The current builder assigns the intended balanced per-family levels in round-robin order (one Easy, Medium, Hard item per family). The rewrite changed 22 difficulty labels while leaving the question content unchanged. The answer ledger records the final intended levels; content/answer verification is separate from difficulty assignment.

## Per-question comparison

| Key | Live question UUID | Initial class | Initial difficulty | Canonical difficulty | Content/options/answer/explanation | Final class |
|---|---|---|---|---|---|---|
| `nvr-001` | `3e22f442-d8da-42f5-ba2e-8546fdae010e` | exact_match | EASY | EASY | exact | exact_match |
| `nvr-002` | `e19926db-350c-4631-9752-5a5ea5e77175` | same_question_answer_difficulty_mismatch | EASY | MEDIUM | exact | exact_match |
| `nvr-003` | `5423a2c7-c44a-44be-a687-f09a26b1d7a7` | same_question_answer_difficulty_mismatch | EASY | HARD | exact | exact_match |
| `nvr-004` | `dbdf725b-61ee-4e2c-8652-23dcdb0136cf` | exact_match | EASY | EASY | exact | exact_match |
| `nvr-005` | `5abe1534-6b16-4434-99b7-e6d5e30b16e7` | same_question_answer_difficulty_mismatch | EASY | MEDIUM | exact | exact_match |
| `nvr-006` | `79ba1550-6424-4404-8c5a-b1603b3c1b9b` | same_question_answer_difficulty_mismatch | EASY | HARD | exact | exact_match |
| `nvr-007` | `3810e955-bdd4-42ce-85d9-fc96c87389de` | exact_match | EASY | EASY | exact | exact_match |
| `nvr-008` | `d802193c-599f-4fd9-80cc-6b3564c2cd1f` | same_question_answer_difficulty_mismatch | EASY | MEDIUM | exact | exact_match |
| `nvr-009` | `2d4f09ee-bee3-49b4-802f-c01d10efed4c` | same_question_answer_difficulty_mismatch | EASY | HARD | exact | exact_match |
| `nvr-010` | `0846c4b8-855e-45dd-a8af-640071a4909a` | exact_match | EASY | EASY | exact | exact_match |
| `nvr-011` | `48dd4f96-8f42-4988-b4a9-6140f570cad6` | same_question_answer_difficulty_mismatch | EASY | MEDIUM | exact | exact_match |
| `nvr-012` | `9a0d7547-f76c-42be-91f1-28a347bac07a` | same_question_answer_difficulty_mismatch | MEDIUM | HARD | exact | exact_match |
| `nvr-013` | `784c0c53-9d46-45a5-9587-9023badd3e22` | same_question_answer_difficulty_mismatch | MEDIUM | EASY | exact | exact_match |
| `nvr-014` | `2b4cf64f-dd7d-431f-a793-3950c08b944a` | exact_match | MEDIUM | MEDIUM | exact | exact_match |
| `nvr-015` | `5c45af2e-6560-4ebf-96a3-22930be60005` | same_question_answer_difficulty_mismatch | MEDIUM | HARD | exact | exact_match |
| `nvr-016` | `00db5987-b488-40c5-ac9a-29aaf442085d` | same_question_answer_difficulty_mismatch | MEDIUM | EASY | exact | exact_match |
| `nvr-017` | `587caa82-d065-45b0-9cc7-5cf8e40ad7c8` | exact_match | MEDIUM | MEDIUM | exact | exact_match |
| `nvr-018` | `630d84cd-35a2-4ce8-91e9-ab4745371aa9` | same_question_answer_difficulty_mismatch | MEDIUM | HARD | exact | exact_match |
| `nvr-019` | `2b6251aa-97e3-432e-b7ec-a5af55707eb4` | same_question_answer_difficulty_mismatch | MEDIUM | EASY | exact | exact_match |
| `nvr-020` | `f5e1d06a-2e2f-426b-b98d-08ec1ecc65c3` | exact_match | MEDIUM | MEDIUM | exact | exact_match |
| `nvr-021` | `9c8ad52c-bb81-4a34-87c3-3bbaa8cf352a` | same_question_answer_difficulty_mismatch | MEDIUM | HARD | exact | exact_match |
| `nvr-022` | `406c487c-3cee-434b-88f1-f9c200ff63b2` | same_question_answer_difficulty_mismatch | MEDIUM | EASY | exact | exact_match |
| `nvr-023` | `19547011-4ec4-4fad-bb3f-5bfed59b4947` | same_question_answer_difficulty_mismatch | HARD | MEDIUM | exact | exact_match |
| `nvr-024` | `d2b73a5e-b7c4-4ffd-89f7-78c997cd9b35` | exact_match | HARD | HARD | exact | exact_match |
| `nvr-025` | `635ab55c-c2db-40cf-aaa6-1c64528c940e` | same_question_answer_difficulty_mismatch | HARD | EASY | exact | exact_match |
| `nvr-026` | `63d4b79d-ef9c-4e5d-b6de-fc58e1964776` | same_question_answer_difficulty_mismatch | HARD | MEDIUM | exact | exact_match |
| `nvr-027` | `56d2c9b0-783b-40a9-bea7-59428519f1e4` | exact_match | HARD | HARD | exact | exact_match |
| `nvr-028` | `1ce2d36a-1dc7-4ff0-a101-129838c1b51d` | same_question_answer_difficulty_mismatch | HARD | EASY | exact | exact_match |
| `nvr-029` | `1076d11c-627f-4469-849a-6abec97bdafa` | same_question_answer_difficulty_mismatch | HARD | MEDIUM | exact | exact_match |
| `nvr-030` | `20d1dd4e-1d07-44be-b089-7dc618ab6caf` | exact_match | HARD | HARD | exact | exact_match |
| `nvr-031` | `3fb9aecc-5fb4-4beb-86fa-097495a6e6b1` | same_question_answer_difficulty_mismatch | HARD | EASY | exact | exact_match |
| `nvr-032` | `b756eac5-311f-4d05-89ff-d76600afeb8c` | same_question_answer_difficulty_mismatch | HARD | MEDIUM | exact | exact_match |
| `nvr-033` | `97b0fad8-bec7-47e3-b172-b211a39fcfc4` | exact_match | HARD | HARD | exact | exact_match |

## Rejected source material / scope

The 55 marked source candidates remain rejected. They were not promoted to source-derived questions. The 33 retained questions remain designated Original.
