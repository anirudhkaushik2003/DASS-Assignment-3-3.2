from groups import barbarian_group,balloon_group

class Spell:
    def __init__(self, cooldown, factor):
        self.cooldown = cooldown
        self.factor = factor

    def effect(self):
        pass


class Rage_spell(Spell):
    def effect(self,king):
        for barbarian in barbarian_group.sprite_list:
            barbarian.speed *= self.factor
            barbarian.y_speed *= self.factor
            barbarian.attack *= self.factor
            if barbarian.y_speed >= barbarian.rect.height:
                barbarian.y_speed = barbarian.rect.height - 1
            if barbarian.speed >= barbarian.rect.width:
                barbarian.speed = barbarian.rect.width - 1
            barbarian.attack_range = barbarian.speed
            barbarian.y_attack_range = barbarian.y_speed

        for barbarian in balloon_group.sprite_list:
            barbarian.speed *= self.factor
            barbarian.y_speed *= self.factor
            barbarian.attack *= self.factor
            if barbarian.y_speed >= barbarian.rect.height:
                barbarian.y_speed = barbarian.rect.height - 1
            if barbarian.speed >= barbarian.rect.width:
                barbarian.speed = barbarian.rect.width - 1
            barbarian.attack_range = barbarian.speed
            barbarian.y_attack_range = barbarian.y_speed

        king.speed *= self.factor
        king.y_speed *= self.factor
        king.attack *= self.factor
        king.attack_range *= king.speed

class Heal_spell(Spell):
    def effect(self,king):
        for barbarian in barbarian_group.sprite_list:
            barbarian.hp *= self.factor
            barbarian.hp = int(barbarian.hp)
            if barbarian.hp >= barbarian.max_hp:
                barbarian.hp = barbarian.max_hp
        for barbarian in balloon_group.sprite_list:
            barbarian.hp *= self.factor
            barbarian.hp = int(barbarian.hp)
            if barbarian.hp >= barbarian.max_hp:
                barbarian.hp = barbarian.max_hp

        king.hp *= self.factor
        king.hp = int(king.hp)
        if king.hp > king.max_hp:
            king.hp = king.max_hp