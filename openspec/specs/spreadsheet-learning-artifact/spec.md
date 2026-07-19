# Spreadsheet Learning Artifact Specification

## Purpose

Defines the MVP spreadsheet/Excel artifact for drawing a 16x16 pixel avatar and preparing frame data for Colab.

## Requirements

### Requirement: 16x16 Avatar Grid Contract

The spreadsheet artifact MUST provide a 16x16 editable grid per frame and SHOULD include labels that make row and column boundaries visible to learners.

#### Scenario: Learner completes a base avatar frame

- GIVEN the learner opens the spreadsheet template
- WHEN they fill all 16x16 cells for one frame
- THEN the artifact contains one complete avatar frame ready for export

#### Scenario: Learner leaves empty cells

- GIVEN a frame contains blank cells
- WHEN the frame is prepared for Colab
- THEN blank cells MUST be treated as transparent or documented background values

### Requirement: Color Input Compatibility

The spreadsheet artifact MUST support numeric color IDs, Hex values, and RGB values in v1.

#### Scenario: Learner uses Hex colors

- GIVEN cells contain values like `#FFCC00`
- WHEN Colab parses the exported sheet data
- THEN each Hex value maps to the intended pixel color

#### Scenario: Learner uses RGB colors

- GIVEN cells contain values like `255,204,0`
- WHEN Colab parses the exported sheet data
- THEN each RGB value maps to the intended pixel color

### Requirement: Frame Separation

The spreadsheet artifact MUST separate frames clearly enough for Colab to parse animation order.

#### Scenario: Multiple frames are exported

- GIVEN the spreadsheet contains frame 1 and frame 2
- WHEN the learner exports or copies the frame data
- THEN Colab can identify each frame and preserve ordering
