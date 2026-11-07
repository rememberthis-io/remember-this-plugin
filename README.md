# Remember This plugin

A memory that outlives a single conversation. Save information in one assistant and recall it in another using your [Remember This](https://remember-this.io) account.

This repository contains a shared skill and Claude/OpenAI plugin manifests. The MCP server is hosted separately at `https://remember-this.io/mcp`; no local server or API key is required. Each user connects their own account through OAuth.

## Install

Download a platform ZIP from [Releases](https://github.com/rememberthis-io/remember-this-plugin/releases). Platform availability and installation permissions depend on your plan and workspace settings.

### Claude Desktop, web, and Cowork

Upload `remember-this-claude-<version>.zip` using Claude's custom plugin upload. Connect Remember This and complete the browser authorization flow. Enable the plugin for your conversation.

See [Claude's plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

### Claude Code

Add the marketplace and install the plugin:

```sh
claude plugin marketplace add rememberthis-io/remember-this-plugin
claude plugin install remember-this@remember-this
```

For local development, clone this repository and load the plugin directly:

```sh
git clone https://github.com/rememberthis-io/remember-this-plugin.git
claude --plugin-dir ./remember-this-plugin
```

Use `/mcp` to connect and authorize Remember This. See [Claude's plugin documentation](https://code.claude.com/docs/en/plugins).

### ChatGPT and Codex

Use `remember-this-openai-<version>-submission.zip` in a host installation flow that accepts plugin packages. This repository is not a listing in the OpenAI plugin directory; directory publication requires a separate submission and review. See [OpenAI's plugin documentation](https://developers.openai.com/plugins).

You can also connect the MCP directly in ChatGPT through its custom remote MCP connection flow. For Codex:

```sh
codex mcp add remember-this --url https://remember-this.io/mcp
codex mcp login remember-this
```

A direct MCP connection provides the tools; it does not install the bundled skill. Install `skills/remember-and-recall` through your host's skill installation mechanism to use both.

### Other MCP clients

Add `https://remember-this.io/mcp` as a Streamable HTTP server with OAuth. Clients can use the MCP without supporting plugins or skills. The shared `SKILL.md` can be used in hosts that support agent skills.

## Try it

- “Remember that my spare key is in the blue kitchen drawer.”
- “Where did I leave my spare key?”
- “Forget the memory about my spare key.”

The tools are `memorize` (save), `recall` (search), and `forget` (hide from recall). Hosts may prefix their names. Forgetting does not permanently erase a memory. Retrieved information becomes available to the assistant in that conversation.

## Build

Requires Python 3.9 or later with no third-party dependencies:

```sh
python3 scripts/build.py
```

The build validates shared metadata and connection settings, then writes two ZIPs to `dist/`. Both include the same skill and branding. Claude uses `.claude-plugin/plugin.json` and `.mcp.json`; OpenAI uses root `plugin.json` and `mcp.json`. The package version lives in both manifests and must match.

The OpenAI submission package includes listing and publication metadata, five positive and three negative review cases, and a hosted demo URL. These cases are prepared expectations, not evidence that live integration tests passed. Reviewer credentials belong only in the secure submission dashboard. Tool annotations, reviewer access, developer verification, scans, and attestations still need checking before submission.

CI builds the packages on pushes and pull requests. Maintainers can attach the resulting ZIPs to a GitHub release. Test installation, OAuth, recall, save, and forget in each target host before declaring a version compatible; packaging validation alone does not establish host compatibility.

## Contribute

Open an [issue](https://github.com/rememberthis-io/remember-this-plugin/issues) or pull request for skill improvements or integration problems. Do not include access tokens or private memories in reports.

## License

MIT. The license covers the files in this repository. Using the hosted service requires a Remember This account and is governed by the service's terms.
