class UnitKamar:
    def __init__(self, kd_unit, kd_kamar, status):
        self.kd_unit = kd_unit
        self.kd_kamar = kd_kamar
        self.status = status

    def __repr__(self):
        return f"UnitKamar(kd_unit={self.kd_unit}, kd_kamar={self.kd_kamar}, status={self.status})"
