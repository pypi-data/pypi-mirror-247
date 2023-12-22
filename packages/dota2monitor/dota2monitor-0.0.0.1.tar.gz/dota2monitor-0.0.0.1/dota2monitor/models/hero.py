from dota2monitor.models.event_managed import EventManaged
from dota2monitor.models.event_manager import EventManager, ListeningEvents


class Hero(EventManaged):
    def __init__(self, hero_data, event_manager: EventManager):
        super().__init__(event_manager)
        self.id = hero_data.get('id')
        self.name = hero_data.get('name')
        self.level = hero_data.get('level', 1)
        self.xp = hero_data.get('xp')
        self.alive = hero_data.get('alive')
        self.respawn_seconds = hero_data.get('respawn_seconds')
        self.buyback_cost = hero_data.get('buyback_cost')
        self.buyback_cooldown = hero_data.get('buyback_cooldown')
        self.health = hero_data.get('health')
        self.max_health = hero_data.get('max_health')
        self.health_percent = hero_data.get('health_percent')
        self.mana = hero_data.get('mana')
        self.max_mana = hero_data.get('max_mana')
        self.mana_percent = hero_data.get('mana_percent')
        self.silenced = hero_data.get('silenced')
        self.stunned = hero_data.get('stunned')
        self.disarmed = hero_data.get('disarmed')
        self.magicimmune = hero_data.get('magicimmune')
        self.hexed = hero_data.get('hexed')
        self.muted = hero_data.get('muted')
        self.break_ = hero_data.get('break')  # 'break' is a keyword, so using 'break_' instead
        self.xpos = hero_data.get('xpos')
        self.ypos = hero_data.get('ypos')
        self.aghanims_scepter = hero_data.get('aghanims_scepter')
        self.aghanims_shard = hero_data.get('aghanims_shard')
        self.smoked = hero_data.get('smoked')
        self.has_debuff = hero_data.get('has_debuff')
        self.talent_1 = hero_data.get('talent_1')
        self.talent_2 = hero_data.get('talent_2')
        self.talent_3 = hero_data.get('talent_3')
        self.talent_4 = hero_data.get('talent_4')
        self.talent_5 = hero_data.get('talent_5')
        self.talent_6 = hero_data.get('talent_6')
        self.talent_7 = hero_data.get('talent_7')
        self.talent_8 = hero_data.get('talent_8')
        self.attributes_level = hero_data.get('attributes_level')

    def update(self, hero_data):
        self.id = hero_data.get('id')
        self.name = hero_data.get('name')
        self.xp = hero_data.get('xp')
        self.alive = hero_data.get('alive')
        self.respawn_seconds = hero_data.get('respawn_seconds')
        self.buyback_cost = hero_data.get('buyback_cost')
        self.buyback_cooldown = hero_data.get('buyback_cooldown')
        self.health = hero_data.get('health')
        self.max_health = hero_data.get('max_health')
        self.health_percent = hero_data.get('health_percent')
        self.mana = hero_data.get('mana')
        self.max_mana = hero_data.get('max_mana')
        self.mana_percent = hero_data.get('mana_percent')
        self.silenced = hero_data.get('silenced')
        self.stunned = hero_data.get('stunned')
        self.disarmed = hero_data.get('disarmed')
        self.magicimmune = hero_data.get('magicimmune')
        self.hexed = hero_data.get('hexed')
        self.muted = hero_data.get('muted')
        self.break_ = hero_data.get('break')  # 'break' is a keyword, so using 'break_' instead
        self.xpos = hero_data.get('xpos')
        self.ypos = hero_data.get('ypos')
        self.aghanims_scepter = hero_data.get('aghanims_scepter')
        self.aghanims_shard = hero_data.get('aghanims_shard')
        self.has_debuff = hero_data.get('has_debuff')
        self.talent_1 = hero_data.get('talent_1')
        self.talent_2 = hero_data.get('talent_2')
        self.talent_3 = hero_data.get('talent_3')
        self.talent_4 = hero_data.get('talent_4')
        self.talent_5 = hero_data.get('talent_5')
        self.talent_6 = hero_data.get('talent_6')
        self.talent_7 = hero_data.get('talent_7')
        self.talent_8 = hero_data.get('talent_8')
        self.attributes_level = hero_data.get('attributes_level')
        
        if self.event_manager and self.level < hero_data.get('level', 1):
            self.trigger_event(ListeningEvents.LVL_UP)

        self.level = hero_data.get('level', 1)

        if self.event_manager and not self.smoked and  hero_data.get('smoked', False):
            self.trigger_event(ListeningEvents.SMOKED)

        self.smoked = hero_data.get('smoked', False)
        

