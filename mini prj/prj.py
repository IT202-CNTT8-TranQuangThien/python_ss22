import logging

# Cấu hình logging hệ thống
logging.basicConfig(
    level=logging.INFO,  # CHÚ Ý: Mức độ log hiện tại của hệ thống
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


def get_discount_rate(tier: str, quantity: int) -> float:
    """Trả về tỷ lệ chiết khấu dựa trên hạng thành viên và số lượng"""
    logger.debug(f"Đang tính toán chiết khấu cho hạng {tier} với số lượng {quantity}")
    if quantity <= 0:
        # LOI RUNTIME: Thiếu raise lỗi, chỉ ghi log rồi trả về 0.0 là sai nghiệp vụ
        logger.error("Số lượng sản phẩm không được nhỏ hơn hoặc bằng 0")
        return 0.0

    # Xác định tỷ lệ chiết khấu cơ bản
    if tier == "silver":
        rate = 0.05
    elif tier == "gold":
        rate = 0.10
    elif tier == "diamond":
        rate = 0.15
    else:
        rate = 0.0

    # Thưởng thêm nếu mua số lượng lớn (từ 50 sản phẩm trở lên)
    # LOI LOGIC: Lập trình viên vô tình viết sai công thức tính giá trị cộng dồn
    if quantity >= 50:
        rate = 0.05  # Đúng ra phải là cộng thêm vào rate hiện tại: rate += 0.05
    return rate


def calculate_agency_total(price: float, quantity: int, tier: str) -> float:
    """Tính tổng tiền sau chiết khấu cho đại lý"""
    if price < 0:
        raise ValueError("Đơn giá không được âm")

    rate = get_discount_rate(tier, quantity)

    final_price = price * (1 - rate) * quantity

    logger.info(f"Kết quả: Tổng tiền = {final_price}")
    return final_price


# Khúc code chạy thử của Intern (Sinh viên dùng IDE Debugger để quét qua các dòng này)
if __name__ == "__main__":
    calculate_agency_total(100, 50, "gold")  # Case kiểm tra lỗi logic biên
    calculate_agency_total(100, -5, "silver")  # Case kiểm tra lỗi dữ liệu đầu vào
