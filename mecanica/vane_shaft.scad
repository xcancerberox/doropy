shaft_diameter = 12;
vane_head_diameter = 20;

module head(){
    difference(){
            {cylinder(20, d=vane_head_diameter, $fn=60);}
            translate([0, 0, 10]) rotate([90, 0, 0]) translate([0, 0, -50]) {cylinder(100, d=5*1.15, $fn=60);}
     }
    }
module vane(){
    union(){
        {cylinder(100, d=shaft_diameter, $fn=60);}
        translate([0, 0, 100]) {head();}
        }
    }
    
 vane();