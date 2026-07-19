# CodePen Learning Artifact Specification

## Purpose

Defines the MVP CodePen workshop artifact where learners reference their generated avatar/GIF and customize it with separate HTML, CSS, and JS.

## Requirements

### Requirement: Separated CodePen Starter

The CodePen artifact MUST provide separate HTML, CSS, and JS panels with learner edit zones for safe customization.

#### Scenario: Learner opens the starter

- GIVEN the learner opens the CodePen starter
- WHEN they inspect the panels
- THEN HTML, CSS, and JS responsibilities are visibly separated

#### Scenario: Learner edits a safe zone

- GIVEN an edit zone is marked for customization
- WHEN the learner changes an accessory, style, or simple interaction
- THEN the workshop result updates without requiring app build tooling

### Requirement: Avatar Asset Handoff

The CodePen artifact MUST reference the learner avatar/GIF through a learner-pasted HTTPS asset URL. For MVP, the expected source is a repository-hosted exported asset generated from Colab. Direct CodePen asset hosting and embedded base64 assets MAY be documented as alternatives, but SHALL NOT be required for v1.

#### Scenario: Learner references a generated GIF

- GIVEN Colab produced a GIF and the learner has an HTTPS URL for it
- WHEN the learner pastes the URL into the CodePen starter
- THEN CodePen displays the generated avatar/GIF in the workshop

#### Scenario: Asset URL is missing or private

- GIVEN the asset URL is empty, local-only, or not publicly reachable
- WHEN CodePen attempts to display the avatar/GIF
- THEN the starter MUST show or document a clear fallback instruction

### Requirement: MVP Learner Flow

The artifact set MUST document the flow: spreadsheet data → Colab draft/avatar/GIF pipeline → CodePen workshop customization.

#### Scenario: Learner completes the MVP path

- GIVEN the learner has completed a spreadsheet avatar
- WHEN they process it in Colab and reference it from CodePen
- THEN they have a customized workshop artifact using their generated avatar/GIF

#### Scenario: Future platform ideas arise

- GIVEN a request involves collective spaces, invitations, routes, question gates, maze challenges, or community teacher editing
- WHEN MVP scope is reviewed
- THEN those ideas MUST remain non-goals for future phases
