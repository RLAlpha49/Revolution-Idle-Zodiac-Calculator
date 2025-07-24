import logging
import math
from typing import Dict, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/zodiac_calculator.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ZodiacCalculator:
    """
    Revolution Idle Zodiac Calculator

    Calculates various zodiac-related statistics and probabilities based on user inputs.
    All inputs are optional - calculations are performed based on available data.
    """

    def __init__(self) -> None:
        """Initialize calculator with optional input values."""
        self.zodiac_rarity: Optional[float] = None
        self.zodiac_quality: Optional[float] = None
        self.zodiac_level: Optional[float] = None
        self.luck: Optional[float] = None
        self.immo_number: Optional[float] = None
        logger.debug("ZodiacCalculator initialized")

    def get_user_input(self) -> bool:
        """
        Get optional input values from the user.
        Users can press Enter to skip any input, leaving it as None.

        Returns:
            bool: True if at least one input was provided, False if all inputs were skipped
        """
        print("=== Revolution Idle Zodiac Calculator ===")
        print("Note: All inputs are optional. Press Enter to skip any field.")
        print("")
        print(
            "DISCLAIMER: All calculations are approximate and based on formulas from:"
        )
        print("- https://revolutionidle.wiki.gg/wiki/Zodiacs")
        print("- https://revolutionidle.wiki.gg/wiki/Planet_Shop")
        print(
            "Results may not exactly match in-game values due to potential formula changes"
        )
        print("or undocumented game mechanics.")
        print("")

        inputs_provided = 0

        try:
            # Zodiac Rarity
            rarity_input = input(
                "Enter Zodiac Rarity (or press Enter to skip): "
            ).strip()
            if rarity_input:
                self.zodiac_rarity = float(rarity_input)
                inputs_provided += 1
                logger.debug("Zodiac rarity set to: %s", self.zodiac_rarity)

            # Zodiac Quality
            quality_input = input(
                "Enter Zodiac Quality (or press Enter to skip): "
            ).strip()
            if quality_input:
                self.zodiac_quality = float(quality_input)
                inputs_provided += 1
                logger.debug("Zodiac quality set to: %s", self.zodiac_quality)

            # Zodiac Level
            level_input = input("Enter Zodiac Level (or press Enter to skip): ").strip()
            if level_input:
                self.zodiac_level = float(level_input)
                inputs_provided += 1
                logger.debug("Zodiac level set to: %s", self.zodiac_level)

            # Luck
            luck_input = input("Enter Luck (or press Enter to skip): ").strip()
            if luck_input:
                self.luck = float(luck_input)
                inputs_provided += 1
                logger.debug("Luck set to: %s", self.luck)

            # Immo+ Number
            immo_input = input("Enter Immo+ Number (or press Enter to skip): ").strip()
            if immo_input:
                self.immo_number = float(immo_input)
                inputs_provided += 1
                logger.debug("Immo+ number set to: %s", self.immo_number)

        except ValueError as e:
            logger.error("Invalid input provided: %s", e)
            print("Error: Please enter valid numbers.")
            return False

        if inputs_provided == 0:
            logger.debug("No inputs provided by user")
            print(
                "No inputs provided. Please provide at least one value to perform calculations."
            )
            return False

        logger.debug("Successfully collected %d inputs", inputs_provided)
        return True

    def _format_number(self, number: float) -> str:
        """
        Format numbers for display, using scientific notation for large numbers.

        Args:
            number: The number to format

        Returns:
            str: Formatted number string
        """
        if math.isinf(number):
            return "∞ (Infinity)"
        elif math.isnan(number):
            return "NaN (Invalid)"
        elif abs(number) >= 1e6:
            return f"{number:.2e}"
        elif abs(number) >= 1000:
            return f"{number:.2f}"
        elif abs(number) >= 1:
            return f"{number:.6f}"
        else:
            return f"{number:.8f}"

    def _has_required_inputs(self, *required_fields: str) -> bool:
        """
        Check if required input fields are available.

        Args:
            *required_fields: Names of required fields

        Returns:
            bool: True if all required fields are available
        """
        for field in required_fields:
            if getattr(self, field) is None:
                return False
        return True

    def calculate_zodiac_sale_price(self) -> Optional[float]:
        """
        Calculate Zodiac Sale Price

        Returns:
            Optional[float]: Sale price if inputs are available, None otherwise
        """
        if not self._has_required_inputs(
            "zodiac_rarity", "zodiac_quality", "zodiac_level"
        ):
            logger.debug("Missing required inputs for zodiac sale price calculation")
            return None

        # Type assertions after validation
        assert self.zodiac_rarity is not None
        assert self.zodiac_quality is not None
        assert self.zodiac_level is not None

        try:
            # Conditional multipliers
            rarity_mult = 2 if self.zodiac_rarity > 8 else 1
            level_mult = (
                ((self.zodiac_level - 90) / 10) ** 2.5
                if self.zodiac_level >= 100
                else 1
            )

            # Main formula
            base_calc = (
                1.125**self.zodiac_rarity
                * self.zodiac_quality
                * (9 + self.zodiac_level**2)
                * rarity_mult
                * level_mult
            ) / 10

            sale_price = (base_calc**0.75) * (1.1**self.zodiac_rarity)
            logger.debug("Zodiac sale price calculated successfully")
            return sale_price
        except (ValueError, OverflowError) as e:
            logger.error("Error calculating zodiac sale price: %s", e)
            return None

    def calculate_zodiac_enhance_price(self) -> Optional[float]:
        """
        Calculate Zodiac Enhance Price

        Returns:
            Optional[float]: Enhance price if inputs are available, None otherwise
        """
        sell_cost = self.calculate_zodiac_sale_price()
        if sell_cost is None or not self._has_required_inputs("zodiac_quality"):
            logger.debug("Missing required inputs for zodiac enhance price calculation")
            return None

        # Type assertion after validation
        assert self.zodiac_quality is not None

        try:
            enhance_price = sell_cost * 2 * (1.3 ** math.log10(1 + self.zodiac_quality))
            logger.debug("Zodiac enhance price calculated successfully")
            return enhance_price
        except (ValueError, OverflowError) as e:
            logger.error("Error calculating zodiac enhance price: %s", e)
            return None

    def calculate_zodiac_enhance_chance(self) -> Optional[float]:
        """
        Calculate Zodiac Enhance Chance

        Returns:
            Optional[float]: Enhance chance if inputs are available, None otherwise
        """
        if not self._has_required_inputs("zodiac_quality"):
            logger.debug(
                "Missing required inputs for zodiac enhance chance calculation"
            )
            return None

        # Type assertion after validation
        assert self.zodiac_quality is not None

        try:
            chance = (0.9 ** (math.log10(1 + self.zodiac_quality) ** 2)) * 100
            logger.debug("Zodiac enhance chance calculated successfully")
            return chance
        except (ValueError, OverflowError) as e:
            logger.error("Error calculating zodiac enhance chance: %s", e)
            return None

    def calculate_zodiac_score(self) -> Optional[float]:
        """
        Calculate Zodiac Score

        Returns:
            Optional[float]: Zodiac score if inputs are available, None otherwise
        """
        if not self._has_required_inputs(
            "zodiac_rarity", "zodiac_quality", "zodiac_level"
        ):
            logger.debug("Missing required inputs for zodiac score calculation")
            return None

        # Type assertions after validation
        assert self.zodiac_rarity is not None
        assert self.zodiac_quality is not None
        assert self.zodiac_level is not None

        try:
            rarity_mult = 2 if self.zodiac_rarity > 8 else 1
            level_mult = (
                ((self.zodiac_level - 90) / 10) ** 2.5
                if self.zodiac_level >= 100
                else 1
            )

            score = (
                1.125**self.zodiac_rarity
                * self.zodiac_quality
                * (9 + self.zodiac_level**2)
                * rarity_mult
                * level_mult
            )
            logger.debug("Zodiac score calculated successfully")
            return score
        except (ValueError, OverflowError) as e:
            logger.error("Error calculating zodiac score: %s", e)
            return None

    def calculate_zodiac_luck(self) -> Optional[float]:
        """
        Calculate Zodiac Luck with soft cap

        Returns:
            Optional[float]: Zodiac luck if input is available, None otherwise
        """
        if not self._has_required_inputs("luck"):
            logger.debug("Missing required inputs for zodiac luck calculation")
            return None

        # Type assertion after validation
        assert self.luck is not None

        try:
            if self.luck < 18:
                result = self.luck
            else:
                result = (self.luck - 18) ** 0.3 * 18

            logger.debug("Zodiac luck calculated successfully")
            return result
        except (ValueError, OverflowError) as e:
            logger.error("Error calculating zodiac luck: %s", e)
            return None

    def calculate_rarity_weights(self, zodiac_luck: float) -> Dict[str, float]:
        """
        Calculate weights for all rarities

        Args:
            zodiac_luck: The calculated zodiac luck value

        Returns:
            Dict[str, float]: Dictionary of rarity weights
        """
        weights = {}

        try:
            # Garbage weight
            if 1 <= zodiac_luck < 2:
                weights["Garbage"] = 5 * (0.8 ** (zodiac_luck - 1))
            elif 2 <= zodiac_luck < 3:
                weights["Garbage"] = (
                    5 * (0.8 ** (zodiac_luck - 1)) * (0.4 ** (zodiac_luck - 2))
                )
            else:
                weights["Garbage"] = 0

            # Common weight
            if 1 <= zodiac_luck < 2:
                weights["Common"] = 15
            elif 2 <= zodiac_luck < 5:
                weights["Common"] = 15 * (0.45 ** (zodiac_luck - 2))
            else:
                weights["Common"] = 0

            # Uncommon weight
            if 1 <= zodiac_luck < 3:
                weights["Uncommon"] = 20 * (1.5 ** (zodiac_luck - 1)) - 12
            elif 3 <= zodiac_luck < 8:
                weights["Uncommon"] = (20 * (1.5 ** (zodiac_luck - 1)) - 12) * (
                    0.5 ** (zodiac_luck - 3)
                )
            else:
                weights["Uncommon"] = 0

            # Rare weight
            if 1 <= zodiac_luck < 5:
                weights["Rare"] = 30 * (1.45 ** (zodiac_luck - 1)) - 28
            elif 5 <= zodiac_luck < 12:
                weights["Rare"] = (30 * (1.45 ** (zodiac_luck - 1)) - 28) * (
                    0.55 ** (zodiac_luck - 5)
                )
            else:
                weights["Rare"] = 0

            # Epic weight
            if 1 <= zodiac_luck < 8:
                weights["Epic"] = max(0, 45 * (1.4 ** (zodiac_luck - 2)) - 50)
            elif 8 <= zodiac_luck < 20:
                weights["Epic"] = max(0, 45 * (1.4 ** (zodiac_luck - 2)) - 50) * (
                    0.6 ** (zodiac_luck - 8)
                )
            else:
                weights["Epic"] = 0

            # Legendary weight
            if 1 <= zodiac_luck < 12:
                weights["Legendary"] = max(0, 80 * (1.36 ** (zodiac_luck - 3)) - 100)
            elif 12 <= zodiac_luck < 30:
                weights["Legendary"] = max(
                    0, 80 * (1.36 ** (zodiac_luck - 3)) - 100
                ) * (0.64 ** (zodiac_luck - 12))
            else:
                weights["Legendary"] = 0

            # Mythic weight
            if 1 <= zodiac_luck < 20:
                weights["Mythic"] = max(0, 120 * (1.3 ** (zodiac_luck - 5)) - 140)
            elif 20 <= zodiac_luck < 50:
                weights["Mythic"] = max(0, 120 * (1.3 ** (zodiac_luck - 5)) - 140) * (
                    0.67 ** (zodiac_luck - 20)
                )
            else:
                weights["Mythic"] = 0

            # Godly weight
            if 1 <= zodiac_luck < 30:
                weights["Godly"] = max(0, 150 * (1.25 ** (zodiac_luck - 8)) - 200)
            elif 30 <= zodiac_luck < 60:
                weights["Godly"] = max(0, 150 * (1.25 ** (zodiac_luck - 8)) - 200) * (
                    0.7 ** (zodiac_luck - 30)
                )
            else:
                weights["Godly"] = 0

            # Divine weight
            if 1 <= zodiac_luck < 40:
                weights["Divine"] = max(0, 200 * (1.2 ** (zodiac_luck - 12)) - 300)
            elif 40 <= zodiac_luck < 50:
                weights["Divine"] = max(0, 200 * (1.2 ** (zodiac_luck - 12)) - 300) * (
                    0.92 ** (zodiac_luck - 40)
                )
            elif 50 <= zodiac_luck < 70:
                weights["Divine"] = (
                    max(0, 200 * (1.2 ** (zodiac_luck - 12)) - 300)
                    * (0.92 ** (zodiac_luck - 40))
                    * (0.75 ** (zodiac_luck - 50))
                )
            else:
                weights["Divine"] = 0

            # Immortal weight
            weights["Immortal"] = max(0, 300 * (1.1 ** (zodiac_luck - 20)) - 500)

            logger.debug("Rarity weights calculated successfully")
            return weights

        except (ValueError, OverflowError) as e:
            logger.error("Error calculating rarity weights: %s", e)
            return {
                rarity: 0.0
                for rarity in [
                    "Garbage",
                    "Common",
                    "Uncommon",
                    "Rare",
                    "Epic",
                    "Legendary",
                    "Mythic",
                    "Godly",
                    "Divine",
                    "Immortal",
                ]
            }

    def calculate_rarity_chances(self, weights: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate rarity chances from weights

        Args:
            weights: Dictionary of rarity weights

        Returns:
            Dict[str, float]: Dictionary of rarity chances as percentages
        """
        total_weight = sum(weights.values())
        if total_weight == 0:
            logger.warning("Total weight is zero, returning zero chances")
            return {rarity: 0 for rarity in weights}

        chances = {}
        for rarity, weight in weights.items():
            chances[rarity] = (weight / total_weight) * 100

        logger.debug("Rarity chances calculated successfully")
        return chances

    def display_results(self) -> None:
        """Display all calculation results based on available inputs"""
        print("\n" + "=" * 50)
        print("CALCULATION RESULTS")
        print("=" * 50)

        # Track what calculations were performed
        calculations_performed = False

        # Basic calculations
        sale_price = self.calculate_zodiac_sale_price()
        enhance_price = self.calculate_zodiac_enhance_price()
        enhance_chance = self.calculate_zodiac_enhance_chance()
        zodiac_score = self.calculate_zodiac_score()

        if any([sale_price, enhance_price, enhance_chance, zodiac_score]):
            print("\n--- Basic Zodiac Calculations ---")
            calculations_performed = True

            if sale_price is not None:
                print(f"Zodiac Sale Price: {self._format_number(sale_price)}")
                print(
                    "  Note: This is the base sale price, multiplied by the 'Wolf Skull' Relic"
                )
            if enhance_price is not None:
                print(f"Zodiac Enhance Price: {self._format_number(enhance_price)}")
            if enhance_chance is not None:
                print(f"Zodiac Enhance Chance: {enhance_chance:.2f}%")
            if zodiac_score is not None:
                print(f"Zodiac Score: {self._format_number(zodiac_score)}")

        # Rarity calculations
        zodiac_luck = self.calculate_zodiac_luck()
        if zodiac_luck is not None:
            weights = self.calculate_rarity_weights(zodiac_luck)
            chances = self.calculate_rarity_chances(weights)

            print("\n--- Rarity Analysis ---")
            calculations_performed = True
            print(f"Zodiac Luck: {self._format_number(zodiac_luck)}")

            print("\nRarity Weights:")
            for rarity, weight in weights.items():
                print(f"  {rarity}: {self._format_number(weight)}")

            print("\nRarity Chances:")
            for rarity, chance in chances.items():
                print(f"  {rarity}: {chance:.4f}%")

        if not calculations_performed:
            print("\nNo calculations could be performed with the provided inputs.")
            print(
                "Please provide the required inputs for the calculations you want to see:"
            )
            print("- Sale Price/Score: Requires rarity, quality, and level")
            print(
                "- Enhance Price/Chance: Requires quality (and rarity/level for price)"
            )
            print("- Rarity Analysis: Requires luck")

        logger.debug("Results displayed successfully")

    def run(self) -> None:
        """Main program loop with improved error handling"""
        logger.debug("Starting Revolution Idle Zodiac Calculator")

        while True:
            try:
                if self.get_user_input():
                    self.display_results()
                else:
                    print("Please try again with valid inputs.")

                print("\n" + "=" * 50)
                choice = input("Calculate again? (y/n): ").lower().strip()
                if choice not in ("y", "yes"):
                    break

                # Reset values for next calculation
                self.zodiac_rarity = None
                self.zodiac_quality = None
                self.zodiac_level = None
                self.luck = None
                self.immo_number = None

            except KeyboardInterrupt:
                logger.debug("Program interrupted by user")
                print("\nProgram interrupted by user.")
                break
            except (ValueError, TypeError, AttributeError) as e:
                logger.error("Input or calculation error in main loop: %s", e)
                print(f"An input or calculation error occurred: {e}")
                print("Please check your inputs and try again.")
            except Exception as e:  # pylint:disable=broad-except
                logger.error("Unexpected error in main loop: %s", e)
                print(f"An unexpected error occurred: {e}")
                # Re-raise if it's a critical system error
                if isinstance(e, (SystemExit, KeyboardInterrupt, SystemError)):
                    raise

        print("Thank you for using the Revolution Idle Zodiac Calculator!")
        logger.debug("Program ended successfully")


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    import os

    os.makedirs("logs", exist_ok=True)

    try:
        calculator = ZodiacCalculator()
        calculator.run()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user during startup")
        print("Program interrupted.")
    except (ImportError, ModuleNotFoundError) as e:
        logger.error("Missing dependencies: %s", e)
        print(f"Missing required dependencies: {e}")
        print("Please ensure all required modules are installed.")
    except Exception as e:  # pylint:disable=broad-except
        logger.error("Fatal error in main execution: %s", e)
        print(f"A fatal error occurred: {e}")
        print("Please check the logs for more information.")
        raise  # Re-raise for debugging
