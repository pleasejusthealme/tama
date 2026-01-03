from datetime import datetime, timedelta

class Tamago:

    zero_since = None
    MAX_HUNGER = 10
    MAX_HAPPINESS = 10
    MAX_ENERGY = 10
    MAX_DIRTY = 10
    TEST_SECONDS = 30


    def __init__(self, name: str, look: str):
        self.name = name
        self.look = look
        self.hunger = Tamago.MAX_HUNGER
        self.happiness = Tamago.MAX_HAPPINESS
        self.energy = Tamago.MAX_ENERGY
        self.is_sleeping = False
        self.dirty = 0
        self.is_alive = True
        self.last_update = datetime.utcnow()
        self.zero_since = None

    def lazy_update(self):
        if not self.is_alive:
            return

        now = datetime.utcnow()
        elapsed = (now - self.last_update).total_seconds()

        hunger_decrease = int(elapsed // 10)
        self.hunger = max(self.hunger - hunger_decrease, 0)

        happiness_decrease = int(elapsed // 10)
        self.happiness = max(self.happiness - happiness_decrease, 0)

        dirty_increase = int(elapsed // 10)
        self.dirty = min(self.dirty + dirty_increase, Tamago.MAX_DIRTY)

        if self.hunger == 0 and self.happiness == 0:
            if self.zero_since is None:
                self.zero_since = now
            elif now - self.zero_since >= timedelta(seconds=Tamago.TEST_SECONDS):
                self.is_alive = False
            else:
                self.zero_since = None

        if self.is_sleeping:
            energy_gain = int(elapsed // 5)
            self.energy = min(self.energy + energy_gain, Tamago.MAX_ENERGY)

        if self.energy >= Tamago.MAX_ENERGY:
            self.is_sleeping = False

        self.last_update = now

    def feed(self, amount: int = 1):
        self.hunger = min(Tamago.MAX_HUNGER, self.hunger + amount)

    def play(self, amount: int = 1):
        if self.energy <= 0:
            self.sleep()
            return False
        
        self.energy = max(self.energy - amount, 0 )
        self.happiness = min(Tamago.MAX_HAPPINESS, self.happiness + amount)
        return True

    def sleep(self):
        self.is_sleeping = True
    
    def wake_up(self):
        self.is_sleeping = False
        self.energy = Tamago.MAX_ENERGY

    def clean(self):
        self.dirty = 0

    def to_dict(self):
        return {
            "name": self.name,
            "look": self.look,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "dirty": self.dirty,
            "energy": self.energy,
            "is_sleeping": self.is_sleeping,
            "is_alive": self.is_alive,
            "last_update": self.last_update.isoformat(),  # сохраняем как float
            "zero_since": self.zero_since.isoformat() if self.zero_since else None
        }
    
    @staticmethod
    def from_dict(data: dict):
        pet = Tamago(
            name=data.get("name", "Питомец"),
            look=data.get("look", "🐾")
        )
        pet.hunger = data.get("hunger", Tamago.MAX_HUNGER)
        pet.happiness = data.get("happiness", Tamago.MAX_HAPPINESS)
        pet.dirty = data.get("dirty", 0)
        pet.energy = data.get("energy", Tamago.MAX_ENERGY)
        pet.is_sleeping = data.get("is_sleeping", False)
        pet.is_alive = data.get("is_alive", True)
        last_update = data.get("last_update")
        pet.last_update = datetime.fromisoformat(last_update) if last_update else datetime.utcnow()
        zero_since = data.get("zero_since")
        pet.zero_since = datetime.fromisoformat(zero_since) if zero_since else None

        return pet
    
    def die(self):
        self.is_alive = False