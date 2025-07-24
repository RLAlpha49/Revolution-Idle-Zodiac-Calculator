# Revolution Idle Zodiac Calculator

A Python calculator for computing various zodiac-related statistics and probabilities in the game Revolution Idle.

## Overview

This calculator helps analyze zodiac performance by computing sale prices, enhance costs, rarity chances, and other key metrics based on zodiac properties. All calculations are based on formulas from the Revolution Idle wiki.

## Features

### Basic Zodiac Calculations

- **Zodiac Sale Price**: Base selling price (multiplied by Wolf Skull Relic)
- **Zodiac Enhance Price**: Cost to enhance the zodiac
- **Zodiac Enhance Chance**: Probability of successful enhancement
- **Zodiac Score**: Overall zodiac performance metric

### Rarity Analysis

- **Zodiac Luck**: Luck value with soft cap applied
- **Rarity Weights**: Raw probability weights for each rarity tier
- **Rarity Chances**: Percentage chance for each rarity (Garbage to Immortal)

## Requirements

- Python 3.7 or higher
- Standard library modules only (math, logging, typing)

## Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed
3. No additional packages required

## Usage

### Running the Calculator

```bash
python zodiac_calculator.py
```

### Input Options

All inputs are optional - simply press Enter to skip any field:

- **Zodiac Rarity**: Numeric rarity value of your zodiac
- **Zodiac Quality**: Quality multiplier of your zodiac  
- **Zodiac Level**: Current level of your zodiac
- **Luck**: Your current luck stat
- **Immo+ Number**: Immortality+ number (for future features)

### Required Inputs by Calculation

- **Sale Price/Score**: Requires rarity, quality, and level
- **Enhance Price/Chance**: Requires quality (and rarity/level for price)
- **Rarity Analysis**: Requires luck

### Example Session

```text
=== Revolution Idle Zodiac Calculator ===
Note: All inputs are optional. Press Enter to skip any field.

DISCLAIMER: All calculations are approximate and based on formulas from:
- https://revolutionidle.wiki.gg/wiki/Zodiacs
- https://revolutionidle.wiki.gg/wiki/Planet_Shop
Results may not exactly match in-game values due to potential formula changes
or undocumented game mechanics.

Enter Zodiac Rarity (or press Enter to skip): 10
Enter Zodiac Quality (or press Enter to skip): 1000
Enter Zodiac Level (or press Enter to skip): 50
Enter Luck (or press Enter to skip): 25
Enter Immo+ Number (or press Enter to skip):

==================================================
CALCULATION RESULTS
==================================================

--- Basic Zodiac Calculations ---
Zodiac Sale Price: 118295.65
  Note: This is the base sale price, multiplied by the 'Wolf Skull' Relic
Zodiac Enhance Price: 519850.27
Zodiac Enhance Chance: 38.73%
Zodiac Score: 1.63e+07

--- Rarity Analysis ---
Zodiac Luck: 32.270219

Rarity Weights:
  Garbage: 0.00000000
  Common: 0.00000000
  Uncommon: 0.00000000
  Rare: 0.00000000
  Epic: 0.00000000
  Legendary: 0.00000000
  Mythic: 1127.06
  Godly: 14923.65
  Divine: 7754.73
  Immortal: 466.092210

Rarity Chances:
  Garbage: 0.0000%
  Common: 0.0000%
  Uncommon: 0.0000%
  Rare: 0.0000%
  Epic: 0.0000%
  Legendary: 0.0000%
  Mythic: 4.6435%
  Godly: 61.4862%
  Divine: 31.9499%
  Immortal: 1.9203%

==================================================
Calculate again? (y/n): n
```

## Formulas and Sources

All calculations are based on formulas from the official Revolution Idle wiki:

- [Zodiacs Wiki Page](https://revolutionidle.wiki.gg/wiki/Zodiacs)
- [Planet Shop Wiki Page](https://revolutionidle.wiki.gg/wiki/Planet_Shop)

### Key Formulas

**Zodiac Score:**

```text
1.125^ZodiacRarity * ZodiacQuality * (9 + ZodiacLevel^2) * 
{8 < ZodiacRarity: 2, 1} * {ZodiacLevel >= 100: ((ZodiacLevel - 90) / 10)^2.5, 1}
```

**Zodiac Luck (with soft cap):**

```text
luck < 18 ? luck : (luck - 18)^0.3 * 18
```

## Output Format

- Large numbers are displayed in scientific notation (e.g., `1.23e+06`)
- Percentages are shown to 2-4 decimal places
- Infinity values are handled gracefully
- All calculations include appropriate error handling

## Logging

The script creates detailed logs in the `logs/` directory:

- `logs/zodiac_calculator.log`: Contains debug information and error details
- Console output shows INFO level and above

## Error Handling

The calculator includes robust error handling for:

- Invalid numeric inputs
- Missing required inputs for specific calculations
- Calculation overflow errors
- File system errors

## Disclaimer

**Important**: All calculations are approximate and based on publicly available formulas from the Revolution Idle wiki. Results may not exactly match in-game values due to:

- Potential formula changes in game updates
- Undocumented game mechanics
- Rounding differences
- Hidden soft caps or modifiers

## License
