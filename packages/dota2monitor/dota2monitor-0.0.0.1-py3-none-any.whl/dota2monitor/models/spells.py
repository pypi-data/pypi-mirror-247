class Spells:
    def __init__(self, abilities):
        self.ability0 = Ability(abilities.get('ability0', {}))
        self.ability1 = Ability(abilities.get('ability1', {}))
        self.ability2 = Ability(abilities.get('ability2', {}))
        self.ability3 = Ability(abilities.get('ability3', {}))
        self.ability4 = Ability(abilities.get('ability4', {}))
        self.ability5 = Ability(abilities.get('ability5', {}))
        self.ability6 = Ability(abilities.get('ability6', {}))

class Ability:
    def __init__(self, ability_data):
        self.name = ability_data.get('name')
        self.level = ability_data.get('level')
        self.can_cast = ability_data.get('can_cast')
        self.passive = ability_data.get('passive')
        self.ability_active = ability_data.get('ability_active')
        self.cooldown = ability_data.get('cooldown')
        self.ultimate = ability_data.get('ultimate')