# Cloud-Functions

Scripts of system defined callbacks.

## How to register new callbacks

1. Create a file in this repo.
2. Add records in the `coinfer_event`, `coinfer_callback` and `coinfer_relation` table.
   The "coinfer_callback.code" field will be in format like this: `repo:vectorly-ai/cloud-functions:<the-file-path>`.
3. Add an event trigger somewhere.
