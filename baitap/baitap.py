import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def show_devices(devices):
    if not devices:
        print("\nHệ thống hiện chưa có thiết bị giám sát nào!")
        return

    print("\n--- DANH SÁCH THIẾT BỊ GIÁM SÁT ---")
    print(f"{'MÃ TB':<6} | {'VỊ TRÍ PHÂN XƯỞNG':<20} | {'CHỈ SỐ CŨ':<10} | {'CHỈ SỐ MỚI':<10} | {'TRẠNG THÁI'}")
    print("-" * 65)

    for dev in devices:
        print(f"{dev['id']:<6} | {dev['location']:<20} | {dev['old_index']:<10} | {dev['new_index']:<10} | {dev['status']}")
    print("-" * 65)


def update_indices(devices):
    print("\n--- CẬP NHẬT CHỈ SỐ ĐIỆN ---")
    device_id = input("Nhập mã thiết bị: ").strip()

    found_device = None
    for dev in devices:
        if dev['id'] == device_id:
            found_device = dev
            break

    if not found_device:
        print(f"[Lỗi] (ERR-E01): Mã thiết bị này không tồn tại trong danh sách hệ thống")
        return

    while True:
        try:
            old_index = int(input("Nhập chỉ số cũ: "))
            new_index = int(input("Nhập chỉ số mới: "))

            if old_index < 0 or new_index < 0:
                print("[Lỗi]: Chỉ số điện phải là số lớn hơn hoặc bằng 0. Vui lòng nhập lại!")
                continue

            if new_index < old_index:
                print(f"[Lỗi] (ERR-E02): Chỉ số mới không được nhỏ hơn chỉ số cũ. Vui lòng nhập lại!")
                continue

            found_device['old_index'] = old_index
            found_device['new_index'] = new_index
            print(f"[Thành công]: Thiết bị {device_id} đã được cập nhật số liệu mới")
            break
        except ValueError:
            print("[Lỗi Ngoại lệ]: Chỉ số điện nhập vào phải là ký tự số hợp lệ!")


def activate_overload_alert(devices):
    print("\n--- KÍCH HOẠT TRẠNG THÁI CẢNH BÁO ---")
    device_id = input("Nhập mã thiết bị cần duyệt: ").strip()

    found_device = None
    for dev in devices:
        if dev['id'] == device_id:
            found_device = dev
            break

    if not found_device:
        print("[Lỗi] (ERR-E01): Mã thiết bị không tồn tại!")
        return

    if found_device['status'] == 'Overload':
        print(f"[Lỗi] (ERR-E04): Thao tác bị hủy! Thiết bị này đã được kích hoạt trạng thái OVERLOAD từ trước!")
        return

    consumption = found_device['new_index'] - found_device['old_index']
    print(f"Tìm thấy thiết bị tại: {found_device['location']} (Lượng tiêu thụ: {consumption} kWh)")

    if consumption > 5000:
        found_device['status'] = 'Overload'
        logging.warning(f"[Cảnh báo]: Thiết bị {device_id} đã vượt ngưỡng tiêu thụ an toàn, chuyển sang OVERLOAD!")
        print(f"[Thành công]: Thiết bị {device_id} đã được kích hoạt trạng thái OVERLOAD!")
    else:
        print("[Thông báo]: Thiết bị hoạt động dưới ngưỡng, chưa đạt điều kiện kích hoạt Overload.")


def calculate_energy_financials(devices):
    base_rate = 3000
    total_consumption = 0

    for dev in devices:
        total_consumption += (dev['new_index'] - dev['old_index'])

    if total_consumption >= 50000:
        discount_percentage = 3
    else:
        discount_percentage = 0

    total_cost_before_discount = total_consumption * base_rate
    discount_amount = total_cost_before_discount * (discount_percentage / 100)
    total_cost_after_discount = total_cost_before_discount - discount_amount

    return (total_consumption, discount_percentage, total_cost_after_discount)


def main():
    devices = [
        {'id': 'M01', 'location': 'Mechanical Shop A', 'old_index': 1200, 'new_index': 4500, 'status': 'Normal'},
        {'id': 'M02', 'location': 'Assembly Line B', 'old_index': 2300, 'new_index': 8500, 'status': 'Overload'}
    ]

    while True:
        print("\n==================================================")
        print("      SMART ENERGY MONITOR - PHÒNG CƠ ĐIỆN       ")
        print("==================================================")
        print("1. Xem danh sách thiết bị giám sát")
        print("2. Cập nhật chỉ số điện tiêu thụ (Check-in)")
        print("3. Kích hoạt trạng thái cảnh báo quá tải")
        print("4. Tính tổng lượng điện & Chi phí năng lượng")
        print("5. Thoát chương trình")
        print("==================================================")

        try:
            choice = int(input("Mời chọn chức năng (1-5): "))

            if choice == 1:
                show_devices(devices)
            elif choice == 2:
                update_indices(devices)
            elif choice == 3:
                activate_overload_alert(devices)
            elif choice == 4:
                total_con, discount, final_cost = calculate_energy_financials(devices)
                print("\n--- BÁO CÁO TÀI CHÍNH NĂNG LƯỢNG ---")
                print(f"+ Tổng lượng điện tiêu thụ thực tế: {total_con:,} kWh")
                print(f"+ Tỷ lệ chiết khấu áp dụng từ nhà nước: {discount}%")
                print(f"+ Tổng chi phí năng lượng phải trả sau chiết khấu: {final_cost:,.0f} VND")
            elif choice == 5:
                print("\nĐang thoát chương trình... Cảm ơn bạn đã sử dụng hệ thống!")
                break
            else:
                print("[Lỗi]: Vui lòng nhập số trong khoảng từ 1 đến 5!")
        except ValueError:
            print("[Lỗi Ngoại lệ]: Lựa chọn menu không hợp lệ! Vui lòng chỉ nhập các ký tự số (1-5).")


if __name__ == '__main__':
    main()