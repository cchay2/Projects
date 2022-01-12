""" Copyright (C) 2022  Christopher Chay

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. """

class Skin:
    def __init__( self, img_dict ):
        self.head_right = img_dict["head_right"]["img"]
        self.head_left = img_dict["head_left"]["img"]
        self.body = img_dict["body"]["img"]
        self.top_arm = img_dict["top_arm"]["img"]
        self.bot_arm = img_dict["bot_arm"]["img"]
        self.top_leg = img_dict["top_leg"]["img"]
        self.bot_leg = img_dict["bot_leg"]["img"]
        
        self.head_right_r = img_dict["head_right"]["img"]
        self.head_left_r = img_dict["head_left"]["img"]
        self.body_r = img_dict["body"]["img"]
        self.top_arm_r = img_dict["top_arm"]["img"]
        self.bot_arm_r = img_dict["bot_arm"]["img"]
        self.top_leg_r = img_dict["top_leg"]["img"]
        self.bot_leg_r = img_dict["bot_leg"]["img"]
        
        self.head_right_rect = img_dict["head_right"]["rect"]
        self.head_left_rect = img_dict["head_left"]["rect"]
        self.body_rect = img_dict["body"]["rect"]
        self.top_arm_rect = img_dict["top_arm"]["rect"]
        self.bot_arm_rect = img_dict["bot_arm"]["rect"]
        self.top_leg_rect = img_dict["top_leg"]["rect"]
        self.bot_leg_rect = img_dict["bot_leg"]["rect"]
        
        self.swing_leg = "up"
        
        self.head_margin = 0
        self.top_arm_margin = 0
        self.bot_arm_margin = 0
        self.top_leg_margin = 0
        self.bot_leg_margin = 0
        
        self.head_angle = 0
        self.body_angle = 0
        self.top_arm_angle = 0
        self.bot_arm_angle = 0
        self.top_leg_angle = 0
        self.bot_leg_angle = 0
        
        self.reset_angle = 0
    
    def getHeadRight( self ):
        return self.head_right
    
    def getHeadRightRect( self ):
        return self.head_right_rect
    
    def getHeadLeft( self ):
        return self.head_left
    
    def getHeadLeftRect( self ):
        return self.head_left_rect
    
    def getHeadAngle( self ):
        return self.head_angle

    def setHeadAngle( self, angle ):
        self.head_angle = angle
    
    
    def getBody( self ):
        return self.body

    def getBodyRect( self ):
        return self.body_rect
    

    def getTopArm( self ):
        return self.top_arm
    
    def getTopArmRect( self ):
        return self.top_arm_rect
    
    def getTopArmAngle( self ):
        return self.top_arm_angle

    def resetTopArmAngle( self ):
        self.top_arm_angle = self.reset_angle
    
    def changeTopArmAngle( self, angle ):
        self.top_arm_angle += angle
        
    
    def getBotArm( self ):
        return self.bot_arm
    
    def getBotArmRect( self ):
        return self.bot_arm_rect
    
    def getBotArmAngle( self ):
        return self.bot_arm_angle
    
    def resetBotArmAngle( self ):
        self.bot_arm_angle = self.reset_angle
    
    def changeBotArmAngle( self, angle ):
        self.bot_arm_angle += angle
        
    
    def getTopLeg( self ):
        return self.top_leg
    
    def getTopLegRect( self ):
        return self.top_leg_rect
    
    def getTopLegAngle( self ):
        return self.top_leg_angle
    
    def resetTopLegAngle( self ):
        self.top_leg_angle = self.reset_angle
    
    def changeTopLegAngle( self, angle ):
        self.top_leg_angle += angle
        
    
    def getBotLeg( self ):
        return self.bot_leg
    
    def getBotLegRect( self ):
        return self.bot_leg_rect
    
    def getBotLegAngle( self ):
        return self.bot_leg_angle

    def resetBotLegAngle( self ):
        self.bot_leg_angle = self.reset_angle
    
    def changeBotLegAngle( self, angle ):
        self.bot_leg_angle += angle