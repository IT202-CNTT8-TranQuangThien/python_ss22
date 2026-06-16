import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


def get_discount_rate(tier: str, quantity: int) -> float:
    """Trả về tỷ lệ chiết khấu dựa trên hạng thành viên và số lượng"""
    logger.debug(f"Đang tính toán chiết khấu cho hạng {tier} với số lượng {quantity}")

    if quantity <= 0:
        logger.error("Số lượng sản phẩm không được nhỏ hơn hoặc bằng 0")
        raise ValueError("Quantity must be positive")

    # Xác định tỷ lệ chiết khấu cơ bản
    if tier == "silver":
        rate = 0.05
    elif tier == "gold":
        rate = 0.10
    elif tier == "diamond":
        rate = 0.15
    else:
        rate = 0.0


    if quantity >= 50:
        rate += 0.05

    return rate


def calculate_agency_total(price: float, quantity: int, tier: str) -> float:
    """Tính tổng tiền sau chiết khấu cho đại lý"""
    if price < 0:
        raise ValueError("Đơn giá không được âm")

    rate = get_discount_rate(tier, quantity)

    final_price = price * (1 - rate) * quantity

    logger.info(f"Kết quả: Tổng tiền = {final_price}")
    return final_price


if __name__ == "__main__":
    print("--- Chạy Case 1: Kiểm tra lỗi logic biên (Gold + 50pcs) ---")

    try:
        calculate_agency_total(100, 50, "gold")
    except Exception as e:
        logger.exception(f"Có lỗi xảy ra ở Case 1: {e}")

    print("\n--- Chạy Case 2: Kiểm tra lỗi dữ liệu đầu vào (Quantity <= 0) ---")

    try:
        calculate_agency_total(100, -5, "silver")
    except ValueError as e:
        logger.warning(f"Bắt được ngoại lệ đúng thiết kế: {e}")