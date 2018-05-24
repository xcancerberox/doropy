shaft_insert_height = 4;
shaft_diameter = 12;

cruz_base_diameter = 15;
cruz_base_height = 10;

arm_length= 150/2;
arm_height = cruz_base_height - shaft_insert_height;

module shaft_insert(){
    cylinder(shaft_insert_height, d=shaft_diameter, $fn=60);
}
module cruz_base(){
        difference(){
                {cylinder(cruz_base_height, d=cruz_base_diameter, $fn=60);}
                translate([0, 0, cruz_base_height - shaft_insert_height + 0.1]) {shaft_insert();}
            
        }
 }
 
 module arm(){
     translate([0, -arm_height/2, 0]) cube([arm_length, arm_height, arm_height]);
     }
 
 module cruz(){
     difference() {
         {cruz_base();}
         rotate([0, 0, 0]) {arm();}
         rotate([0, 0, 120]) {arm();}
         rotate([0, 0, 2400]) {arm();}
         }
 }
 
arm();