shaft_insert_height = 4;
shaft_diameter = 12;

base_radius = 50+shaft_diameter/2;
base_height = 10;

shaft_insert_height = 4;
cruz_base_height = 10;
arm_height = cruz_base_height - shaft_insert_height;
a=0.95;
b=6.7;

 module cosito(){
     union(){
        rotate([0, 0, 0]) translate([0, base_radius*a/2, 0]) {cube([arm_height, base_radius*a, arm_height], center=true);}
        rotate([0, 0, 120]) translate([0, base_radius*a/2, 0]) {cube([arm_height, base_radius*a, arm_height], center=true);}
        rotate([0, 0, 240]) translate([0, base_radius*a/2, 0]) {cube([arm_height, base_radius*a, arm_height], center=true);}
        }
     }
 
 module base(){
     difference(){
         difference(){
             {cylinder(base_height, r=base_radius);}
             {cylinder(100, d=b*1.15);}
             translate([0, 0, 4]) {cylinder(base_height, d=shaft_diameter*1.2);}
           } 
         translate([0, 0, base_height-arm_height/2]) {cosito();}
         rotate([0, 0, 30]) translate([10+base_radius/2, 0, 0]) {cylinder(base_height, r=25, $fn=60);}
         rotate([0, 0, 120+30]) translate([10+base_radius/2, 0, 0]) {cylinder(base_height, r=25, $fn=60);}
         rotate([0, 0, 240+30]) translate([10+base_radius/2, 0, 0]) {cylinder(base_height, r=25, $fn=60);}
         }
     }
base();