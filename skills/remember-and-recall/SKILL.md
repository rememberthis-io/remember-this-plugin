---
name: remember-and-recall
description: Save information to Remember This, retrieve saved memories, and use remembered context when the user asks to remember, recall, or work with information from earlier conversations.
---

# Remember and recall

Use the connected Remember This MCP server. Follow its discovered tool descriptions and schemas; hosts may prefix the tool names.

## Recall

Use `remind_me` before guessing about the user's work, preferences, or earlier decisions when remembered context would help the current request. Search with a natural-language phrase describing what you need. An empty result means no relevant memory was found; do not invent one. Distinguish retrieved information from your own inferences, and prefer the user's current correction over an older memory.

## Save

Use `remember_this` when the user asks to remember information. Preserve the intended meaning and enough context to find it later. Split distinct thoughts into separate notes. When the user has authorized ongoing memory, save durable decisions, preferences, and constraints within that scope; avoid passing details that only matter in the current task. Confirm a save only after the tool reports success.

For photographs, use the original image bytes and a supported MIME type when available. Do not substitute an image description for the photograph or claim to have stored an attachment you could not access.

## Forget and correct

Use `forget_memory` only when the user asks to forget a specific memory. Obtain its ID from recall; clarify the target when several memories could match. Forgetting hides the memory from recall and does not permanently erase it. Saving a correction does not itself remove the earlier memory; do not silently forget the old entry.

## Connection

If tools are unavailable, explain that the user needs to connect Remember This at `https://remember-this.io/mcp` and complete OAuth in their browser. Never ask for their password or access token in chat. Do not claim a memory was saved, retrieved, or forgotten without a successful tool result.
