from Simulation.Other.plate import Plate
class PlateManager:
    """
    用于管理所有 plate 的类
    包括但不限于初始化 plate, 记录所有的 plate 等
    单例模式
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        # 创建实例时检查是否已存在
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 确保初始化逻辑只执行一次
        if not self._initialized:
            # 使用简单递增 ID 初始化所有 plate
            # 暂时不考虑 ID 复用问题
            self.next_plate_id = 1
            # 存储所有板子 {plate_id: Plate实例}
            self.plates = {}
            self._initialized = True


    def create_new_plate(self):
        plate = Plate(self.next_plate_id)
        self.plates[self.next_plate_id] = plate
        self.next_plate_id = self.next_plate_id + 1
        return plate

    def get_plate_by_plate_id(self, plate_id):
        if plate_id in self.plates:
            return self.plates[plate_id]
        return None

    def delete_plate_by_id(self, plate_id):
        if plate_id in self.plates:
            # del 操作会直接删除, 和赋值为 None 的操作不一样
            del self.plates[plate_id]
            return True
        return False



