class Plate:
    def __init__(self, plate_id, name=None):
        self.id = f"Plate_{plate_id}"
        # has_lid 属性默认板子有盖子, 对于有盖子的板子, 如果在开关盖机器上打开了板子, 该属性会变为 False, 直到下一次关闭板子
        self.has_lid = True
        self.lid_id = f"lid_{plate_id}"  # 每个板子的盖子有唯一ID
        self.lid_location = None # 记录盖子的位置, 一般情况下和板子在一起, 开盖后在开关盖设备上

    def __str__(self):
        return f"{self.id}({'with lid' if self.has_lid else 'without lid'})"

    def open_lid(self, position_id):
        """打开盖子"""
        if not self.has_lid:
            raise RuntimeError(f"Plate {self.id} doesn't have a lid to remove")
        self.has_lid = False
        self.lid_location = position_id
        return self.lid_id

    def close_lid(self, lid_id, position_id):
        """关闭盖子"""
        if self.has_lid:
            raise RuntimeError(f"{self.id} already has a lid")
        if position_id != self.lid_location:
            raise RuntimeError(f"{lid_id} doesn't match plate {self.id}")
        self.has_lid = True
        self.lid_location = None
