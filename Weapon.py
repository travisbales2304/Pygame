import pygame as pg
import sys
from os import path
from settings import *
from Debug import *

class Weapon:
    def __init__(self):
        self.WeaponName = 'Fist'
        self.AttackSpeed = 1.0
        self.Hitbox = None
        self.Damage = 1
        self.IsRanged = False
        self.image = None

    def GetDamage(self):
        return self.Damage
    
    def GetAttackSpeed(self):
        return self.AttackSpeed
    
    def GetName(self):
        return self.WeaponName

    def GetType(self):
        return self.IsRanged

    def Attack(self):
        pass

    def SpecialAttack(self):
        pass
    

    