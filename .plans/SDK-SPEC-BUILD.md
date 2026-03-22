# AceDataCloud SDK Spec Build Plan

## Status

- Phase: 2
- Status: Implemented
- Scope: canonical spec pipeline, overlays, generation boundary,
  minimal POC structure

## Canonical Pipeline

Five layers: raw inventory, service mapping enrichment, overlay
application, canonical spec emission, language generation input.

## Generated Versus Handwritten Boundary

### Generated artifacts

- domain operation functions or methods
- request type definitions
- response type definitions

### Handwritten artifacts

- HTTP transport
- authentication injection
- retry logic
- timeout handling
- error mapping
- stream parsing
- task handle and poller abstractions
- upload helper behavior

### Hard rule

No handwritten logic may be placed inside generated output directories.
Generated directories must remain fully replaceable.
