shaft_insert_height = 4;
shaft_diameter = 12;

cruz_base_diameter = 15;
cruz_base_height = 10;

arm_length= 50;
arm_height = cruz_base_height - shaft_insert_height;
 
 module arm_base(){
     cube([arm_length, arm_height, arm_height], center=true);
     }
 
 module arm(){
     difference(){
         {arm_base();}
         translate([arm_length/2, 0, 0]) rotate([0, 0, 60]) scale(1.1) {arm_base();}
         translate([-arm_length/2, 0, 0]) rotate([0, 0, 60]) scale(1.1) {arm_base();}
         }
     }
     
translate([0, 0, arm_height/2]) arm();