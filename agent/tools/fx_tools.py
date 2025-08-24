from constants.miscellaneous_constants import FX_RATES
from utils.logger import get_logger
from typeguard import typechecked

logger = get_logger(__name__)

@typechecked
def fx_convert(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Convert an amount from one currency to another using predefined FX rates.

    Args:
        amount (float): The amount of money to convert.
        from_currency (str): The source currency (e.g., "USD").
        to_currency (str): The target currency (e.g., "EUR").

    Returns:
        float: The converted amount, rounded to 2 decimal places.
               Returns 0.0 if no exchange rate is found.

    Raises:
        Exception: For unexpected errors during conversion.
    """

    logger.info("Starting FX conversion: %s %s -> %s", amount, from_currency, to_currency)
    try:
        from_currency: str = from_currency.lower()
        to_currency: str = to_currency.lower()

        if from_currency == to_currency:
            logger.info("From and to currencies are the same. Returning amount: %s", amount)
            return round(amount, 2)

        key: str = f"{from_currency}_to_{to_currency}"
        inverse_key: str = f"{to_currency}_to_{from_currency}"

        if key in FX_RATES:
            rate: float = FX_RATES[key]
            logger.info("Using direct FX rate for %s: %s", key, rate)
        elif inverse_key in FX_RATES:
            rate = 1 / FX_RATES[inverse_key]
            logger.info("Using inverse FX rate for %s: %s", inverse_key, rate)
        else:
            logger.error("FX rate not found for %s -> %s. Returning 0.0", from_currency, to_currency)
            return 0.0

        result: float = round(amount * rate, 2)
        logger.info("FX conversion result: %s", result)
        return result

    except Exception:
        logger.error("Error during FX conversion for %s %s -> %s", amount, from_currency, to_currency, exc_info=True)
        raise
